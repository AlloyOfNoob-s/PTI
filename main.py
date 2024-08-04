import sys
import PyQt6
import ListManage
import QtUtility
from uipy import home,add_change
from PyQt6 import uic
import PyQt6.QtWidgets
alist =ListManage.acclist()
glist =ListManage.gamelist()
curid = 0
name,directory,lo = "","",""
def getselect(tar:str):
    for item in glist.list:
        if(str(item["id"])+" "+item["name"]==tar):
            return item
class add(PyQt6.QtWidgets.QDialog,add_change.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.yes)
    def yes(self):
        global name
        global directory
        global lo
        name = self.t3.toPlainText()
        directory = self.t2.toPlainText()
        lo = self.t1.toPlainText()
        print(name)
        print(directory)
        print(lo)
        home.add()
class change(PyQt6.QtWidgets.QDialog,add_change.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.yes)
    def afterinit(self):
        self.cur = getselect(home.listWidget.selectedItems()[0].text())
        self.t2.setPlainText(self.cur["weblink"])
        self.t3.setPlainText(self.cur["name"])
    def yes(self):
        global name
        global directory
        global lo
        name = self.t3.toPlainText()
        directory = self.t2.toPlainText()
        lo = self.t1.toPlainText()
        print(name)
        print(directory)
        print(lo)
        home.change()        
class Home(PyQt6.QtWidgets.QMainWindow,home.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.afterinit()
        self.pushButton.pressed.connect(self.click1)
        self.pushButton_3.pressed.connect(self.click2)
    def afterinit(self):
        self.listWidget.clear()
        for item in glist.list:
            self.listWidget.addItem(str(item["id"])+" "+item["name"])
    def click1(self):
        box1.show()
    def click2(self):
        box2.afterinit()
        box2.show()
    def add(self):
            glist.add(ListManage.game(len(glist.list),name,directory))
            self.listWidget.addItem(str(len(glist.list)-1)+" "+name)
    def change(self):
        glist.edit(getselect(home.listWidget.selectedItems()[0].text()),name=name)

class Login(PyQt6.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi("ui/login.ui",self)
        self.press0.clicked.connect(self.click0)
        self.press1.clicked.connect(self.click1)
    def click0(self):
        if (self.p0.text()):
            if(alist.login(self.n0.text(),self.p0.text())):
                QtUtility.change(self,home)
            else:
                QtUtility.mesc("Wrong Password or user don't exist","error")
        else:
            QtUtility.mesc("Please enter password","error")
    def click1(self):
        QtUtility.change(self,signup)
class Signup(PyQt6.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi("ui/signup.ui",self)
        self.press0.clicked.connect(self.click0)
        self.press1.clicked.connect(self.click1)        
    def click0(self):
        if(self.n0.text() and self.p0.text() and self.p1.text()):
            if(self.p0.text()==self.p1.text()):
                tar = ListManage.acc(len(alist.list),self.n0.text(),self.p0.text())
                alist.add(tar)
                QtUtility.mesc("Signup complete","message from systemx")
            else:
                QtUtility.mesc("Password don't match","error")
        else:
            QtUtility.mesc("Please enter something","error")
    def click1(self):
        QtUtility.change(self,login)
class Bot(PyQt6.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi("ui/Bot.ui",self)
class Admin(PyQt6.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi("ui/Admin.ui",self)
app = PyQt6.QtWidgets.QApplication(sys.argv)
home = Home()
login = Login()
signup = Signup()
bot = Bot()
admin = Admin()
box1 = add()
box2 = change()
login.show()
app.exec()