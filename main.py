import sys
import PyQt6
import ListManage
import QtUtility
from uipy import home
from PyQt6 import uic
import PyQt6.QtWidgets
alist =ListManage.acclist()
glist =ListManage.gamelist()
class Home(PyQt6.QtWidgets.QMainWindow,home.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.afterinit()
    def afterinit(self):
        for item in glist.list:
            self.listWidget.addItem(str(item["id"])+" "+item["name"])

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
login.show()
app.exec()
#change