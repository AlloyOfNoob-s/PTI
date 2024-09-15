import argparse
import concurrent.futures
import contextlib
import functools
import glob
import json
import os
import shutil
import tempfile

from io import BytesIO
from typing import NamedTuple
from typing import Sequence
from zipfile import ZipFile

from requests import Session
from requests import HTTPError

SEP = "-"
TARGET_BASE_URL = "https://thunderstore.io/package/download"
MOD_DIR_IGNORE = ("readme.md", "icon.png", "manifest.json", "changelog.md", "license")
BEPINEX_PACKAGE_NAME = "BepInExPack"
BEPINEX = "BepInEx"
BEPINEX_PLUGINS_DIR = "plugins"
BEPINEX_PATCHERS_DIR = "patchers"
BEPINEX_CONFIG_DIR = "config"


class Mod(NamedTuple):
    by: str
    name: str
    version: str
    out_dir: str = ""

    @property
    def package_name(self) -> str:
        return f"{self.by}{SEP}{self.name}{SEP}{self.version}"

    @property
    def download_path(
        self,
    ) -> str:
        return os.path.abspath(os.path.join(self.out_dir, self.package_name))

    @property
    def url(self) -> str:
        return f"{TARGET_BASE_URL}/{self.by}/{self.name}/{self.version}"

    @property
    def exists(self) -> bool:
        return os.path.exists(self.download_path)

    @property
    def manifest_file(self) -> str:
        return os.path.join(self.download_path, "manifest.json")

    @property
    def is_bepinex(self) -> bool:
        return self.name.casefold() == BEPINEX_PACKAGE_NAME.casefold()

    @property
    def bepinex_dir(self) -> str:
        return os.path.join(self.download_path, BEPINEX)

    @property
    def depends_on_bepinex(self) -> bool:
        for _, dirs, _ in os.walk(self.download_path):
            for dir in dirs:
                if BEPINEX in dir:
                    return True
        with open(self.manifest_file, encoding="utf-8-sig") as f:
            data = json.load(f)
        return any(BEPINEX in dep for dep in data["dependencies"])

    def __repr__(self) -> str:
        return f"{self.name} {self.version}"


def _is_bepinex_installed(game_dir: str) -> bool:
    return os.path.exists(os.path.join(game_dir, BEPINEX))


def _read_mods(mods_file: str) -> tuple[set[Mod], Mod | None]:
    with open(mods_file) as f:
        lines = f.readlines()
    mods = {Mod(*mod.rstrip().split(SEP)) for mod in lines}
    bepinex_mods = {m for m in mods if m.is_bepinex}

    if len(bepinex_mods) > 1:
        raise ValueError(
            f"Multiple {BEPINEX_PACKAGE_NAME} entries in '{mods_file}' [{bepinex_mods}]"
        )

    try:
        bepinex_mod = bepinex_mods.pop()
        mods.remove(bepinex_mod)
    except KeyError:
        bepinex_mod = None

    return mods, bepinex_mod


def _download(mod: Mod, session: Session) -> int:
    if mod.exists:
        return 0
    response = session.get(mod.url)
    response.raise_for_status()
    z = ZipFile(BytesIO(response.content))
    z.extractall(mod.download_path)
    return 1


def _get_file_install_path(game_dir: str, file: str, is_bepinex: bool) -> str:
    if is_bepinex:
        file = file.replace(f"{BEPINEX_PACKAGE_NAME}{os.sep}", "")
        return os.path.join(game_dir, file)

    # Clean up some crappy file paths
    file = file.replace("\\", os.sep).replace(f"{BEPINEX}{os.sep}", "")

    try:
        _sub_dir = file[: file.index(os.sep)]
    except ValueError:
        file = os.path.join(BEPINEX_PLUGINS_DIR, file)
    else:
        if _sub_dir not in (
            BEPINEX_PLUGINS_DIR,
            BEPINEX_PATCHERS_DIR,
            BEPINEX_CONFIG_DIR,
        ):
            file = os.path.join(BEPINEX_PLUGINS_DIR, file)
    return os.path.join(game_dir, BEPINEX, file)


def _install(mod: Mod, game_dir: str) -> int:
    if not mod.depends_on_bepinex and not mod.is_bepinex:
        print(f"Unable to install {mod} as it doesn't depend on {BEPINEX}")
        return 0

    downloaded_files = tuple(
        f
        for f in glob.glob("**", root_dir=mod.download_path, recursive=True)
        if os.path.basename(f).lower() not in MOD_DIR_IGNORE
        and not os.path.isdir(os.path.join(mod.download_path, f))
    )
    installed = False
    for file in downloaded_files:
        file_install_path = _get_file_install_path(game_dir, file, mod.is_bepinex)
        if os.path.exists(file_install_path):
            continue
        os.makedirs(os.path.dirname(file_install_path), exist_ok=True)
        downloaded_file_path = os.path.join(mod.download_path, file)
        shutil.copy(downloaded_file_path, file_install_path)
        installed = True
    print(f"Installed {mod}" if installed else f"Skipping {mod} (already installed)")
    return 1 if installed else 0


def _download_and_install_mod(
    mod: Mod,
    game_dir: str,
    session: Session,
) -> tuple[int, int, int]:
    try:
        ret_dl = _download(mod, session)
    except HTTPError as e:
        print(f"Failed to download {mod}: {e}")
        return 0, 0, 1
    else:
        return ret_dl, _install(mod, game_dir), 0


def _download_and_install_mods(mods: set[Mod], game_dir: str, session: Session) -> None:
    _func = functools.partial(
        _download_and_install_mod, game_dir=game_dir, session=session
    )
    with concurrent.futures.ThreadPoolExecutor() as ex:
        results = ex.map(_func, mods)
    downloaded, installed, errs = map(sum, zip(*results))
    tot = len(mods)
    print(f"Downloaded {downloaded}/{tot}. Installed {installed}/{tot}. Errors: {errs}")


def main(argv: Sequence | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Thunderstore.io BepInEx mod downloader and installer."
    )
    parser.add_argument(
        "game_dir",
        help="Path to the directory of the game you wish to install mods for.",
    )
    parser.add_argument(
        "--mods-file",
        "-f",
        default="mods.txt",
        help=f"File to read mods from (by{SEP}name{SEP}version format). Default is %(default)s.",
    )
    parser.add_argument(
        "--out-dir", "-o", help="Save the downloaded mods to the given directory."
    )

    args = parser.parse_args(argv)

    if not os.path.isdir(args.game_dir):
        print(f"Game directory '{args.game_dir}' does not exist.")
        return 1
    if args.out_dir and not os.path.isdir(args.out_dir):
        print(f"Out directory '{args.out_dir}' does not exist.")
        return 1

    mods, bepinex_mod = _read_mods(args.mods_file)

    with (
        Session() as sess,
        contextlib.ExitStack() as ctx,
    ):
        Mod.out_dir = args.out_dir or ctx.enter_context(tempfile.TemporaryDirectory())
        if not _is_bepinex_installed(args.game_dir):
            if bepinex_mod is not None:
                # Install BepInEx first
                _, _, err = _download_and_install_mod(bepinex_mod, args.game_dir, sess)
                if err == 1:
                    # Failed to download/install. return Error
                    return 1
            else:
                print(f"{BEPINEX_PACKAGE_NAME} is not installed.")
                print(f"Add it to '{args.mods_file}' or install it manually.")
                print("See https://thunderstore.io/package/bbepis/BepInExPack")
                return 1
        elif bepinex_mod is not None:
            print(f"Skipping {bepinex_mod} (already installed)")

        _download_and_install_mods(mods, args.game_dir, sess)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
