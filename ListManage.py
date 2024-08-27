import webbrowser
import json
class acclist():
    def __init__(self):
        self.list = []
        self.loadacc()
    def loadacc(self):
        with open("data/acc.json","r") as file:
            self.list = json.load(file)
    def show(self):
        for i in self.list:
            print(i)
            print("")
    def change(self,id,oldpass,newpass):
        for i in self.list:
            if(id==i["id"]):
                while True:
                    if(oldpass == i["password"]):
                        i["password"] = newpass
                        self.saveuser()
                        break
                    else:
                        break
                break
    def saveuser(self):
        with open("data/acc.json","w") as file:
            json.dump(self.list,file,indent=3)
    def add(self,tar):
        self.list.append(tar.__dict__)
        self.saveuser()
    def login(self,name,password):
        for i in self.list:
            if(i["name"]==name):
                if(i["password"]==password):
                    return True
                else:
                    return False
        return False
class gamelist():
    def __init__(self):
        self.list = []
        self.loadgame()
    def loadgame(self):
        with open("data/game.json","r") as file:
            self.list = json.load(file)
    def show(self):
        for i in self.list:
            print(i)
            print("")
    def savegame(self):
        with open("data/game.json","w") as file:
            json.dump(self.list,file,indent=4) 
    def add(self,tar):
        self.list.append(tar.__dict__)
        self.savegame()
    def openweb(self,id):
        for i in self.list:
            if(id==i["id"]):
                i.open()
    def delete(self,id:int=None,name:str=None):
        if id:
            for game in self.list:
                if(game["id"]==id):
                    self.list.remove(game)
                    self.savegame()
                    break
        elif name:
            for game in self.list:
                if(game["name"]==name):
                    self.list.remove(game)
                    self.savegame()
                    break
    def edit(self,tar:dict,id:int=None,name:str=None):
        if id:
            for game in self.list:
                if(game["id"]==id):
                    game["name"] = tar["name"]
                    game["exedir"] = tar["exedir"]
                    game["moddir"] = tar["moddir"]
                    self.savegame()
        elif name:
            for game in self.list:
                if(game["name"]==name):
                    game["name"] = tar["name"]
                    game["exedir"] = tar["exedir"]
                    game["moddir"] = tar["moddir"]
                    self.savegame()
    def search(self,name):
        done = []
        for game in self.list:
            if(name in game["name"]):
                done.append(game)
        return done
    def sort(self):
        done = self.list
        Nc = True
        while Nc:
            Nc = False
            for i in done:
                if(done.index(i)+1!=len(done)):
                    if(i["name"][0]>done[done.index(i)+1]["name"][0]):
                        i["name"],done[done.index(i)+1]["name"] = done[done.index(i)+1]["name"],i["name"]
                        Nc = True
        return done
class game():
    def __init__(self,id:int,name,weblink,moddir):
        self.id = id
        self.name = name
        self.exedir = weblink
        self.moddir = moddir
    def open(self):
        webbrowser.open(self.weblink)
class acc():
    def __init__(self,id,name,password):
        self.id = id
        self.name = name
        self.password = password
    def changepass(self,x):
        self.password = x
l = gamelist()
print(l.list)