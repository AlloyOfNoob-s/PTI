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
            json.dump(self.list,file,indent=3)  
    def add(self,tar):
        self.list.append(tar.__dict__)
        self.savegame()
    def openweb(self,id):
        for i in self.list:
            if(id==i["id"]):
                i.open()  
class game():
    def __init__(self,id,name,weblink):
        self.id = id
        self.name = name
        self.weblink = weblink
    def open(self):
        webbrowser.open(self.weblink)
class acc():
    def __init__(self,id,name,password):
        self.id = id
        self.name = name
        self.password = password
    def changepass(self,x):
        self.password = x
