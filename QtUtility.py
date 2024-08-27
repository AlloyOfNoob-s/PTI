import PyQt6
import PyQt6.QtWidgets
def mesc(Text,Title):
    box = PyQt6.QtWidgets.QMessageBox()
    box.setWindowTitle(Title)
    box.setText(Text)
    box.exec()
def change(cur,tar):
    cur.close()
    tar.show()