from pathlib import Path
import sys
import PyQt6
import ListManage
import QtUtility
from uipy import home,add_change,selection,mod
from PyQt6 import uic
import PyQt6.QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtWidgets,QtGui
import os
alist =ListManage.acclist()
glist =ListManage.gamelist()
curid = 0
name,directory,lo = "","",""
def getselect(tar:str):
    for item in glist.list:
        if(str(item["id"])+" "+item["name"]==tar):
            return item
class panel(QtWidgets.QWidget):
    def __init__(self,tar):
        super().__init__()
        self.setParent(tar)
        self.setMinimumSize(QtCore.QSize(200, 500))
        self.setMaximumSize(QtCore.QSize(200, 500))
        self.setStyleSheet("background-color: rgb(170, 255, 255);")
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
        self.t1.setPlainText(self.cur["moddir"])
        self.t2.setPlainText(self.cur["exedir"])
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
        self.pushButton_2.pressed.connect(self.click3)
        self.pushButton_4.pressed.connect(self.click4)
        self.lineEdit.textEdited.connect(self.Tsearch)
        self.b0.pressed.connect(self.se)
    def afterinit(self):
        self.listWidget.clear()
        for item in glist.list:
            self.listWidget.addItem(str(item["id"])+" "+item["name"])
            print("loaded")
    def click1(self):
            box1.show()
    def click2(self):
        if(self.listWidget.selectedItems()):
            box2.afterinit()
            box2.show()
        else:
            QtUtility.mesc("error: please select","error")
    def click3(self):
        if(self.listWidget.selectedItems()):
            glist.delete(id=getselect(home.listWidget.selectedItems()[0].text())["id"])
            self.afterinit()
        else:
            QtUtility.mesc("error: please select","error")
    def click4(self):
        self.listWidget.clear()
        for item in glist.sort():
            self.listWidget.addItem(str(item["id"])+" "+item["name"])
    def Tsearch(self):
        self.listWidget.clear()
        for item in glist.search(self.lineEdit.text()):
            self.listWidget.addItem(str(item["id"])+" "+item["name"])
    def se(self):
        QtUtility.change(self,Selection)
    def add(self):
            glist.add(ListManage.game(int(glist.list[len(glist.list)-1]["id"])+1,name,directory,lo))
            self.afterinit()
    def change(self):
        glist.edit(id=getselect(home.listWidget.selectedItems()[0].text())["id"],tar=ListManage.game(getselect(home.listWidget.selectedItems()[0].text())["id"],name,directory,lo).__dict__)
        self.afterinit()
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
class selections(PyQt6.QtWidgets.QMainWindow,selection.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.b2.pressed.connect(self.click2)
        self.sor.pressed.connect(lambda: self.load("sort"))
        self.load("normal")
        self.search.textChanged.connect(lambda: self.load("search"))
    def load(self,mode):
        for i in reversed(range(self.horizontalLayout.count())): 
            w=self.horizontalLayout.itemAt(i).widget()
            self.horizontalLayout.removeWidget(w)
            w.setParent(None) 
        if(mode=="normal"):
            for item in glist.list:
                parentdir = Path(item["exedir"])
                parentdir = str(parentdir.parent.absolute())
                self.newwidget_3 = QtWidgets.QWidget(parent=self.scrollAreaWidgetContents)
                self.newwidget_3.setMinimumSize(QtCore.QSize(200, 500))
                self.newwidget_3.setMaximumSize(QtCore.QSize(200, 500))
                self.newwidget_3.setStyleSheet("background-color: rgb(170, 255, 255);")
                self.newwidget_3.setObjectName("widget_3")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.newwidget_3)
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.img = QtWidgets.QLabel(parent=self.newwidget_3)
                self.img.setText("")
                if(os.path.isfile(parentdir+"/icon.png")):
                    self.img.setPixmap(QtGui.QPixmap(parentdir+"/icon.png"))
                else:
                    self.img.setPixmap(QtGui.QPixmap("img/null.png"))
                self.img.setScaledContents(True)
                self.img.setObjectName("img")
                self.verticalLayout_2.addWidget(self.img)
                self.n = QtWidgets.QLabel(parent=self.newwidget_3)
                self.n.setMinimumSize(QtCore.QSize(0, 20))
                self.n.setMaximumSize(QtCore.QSize(16777215, 90))
                self.n.setStyleSheet("border-radius:5px;\n"
        "border-color: rgb(255, 255, 255);\n"
        "background-color: rgb(255, 255, 255);")
                self.n.setObjectName("n")
                self.verticalLayout_2.addWidget(self.n)
                self.dir = QtWidgets.QLabel(parent=self.newwidget_3)
                self.dir.setMinimumSize(QtCore.QSize(0, 20))
                self.dir.setMaximumSize(QtCore.QSize(16777215, 90))
                self.dir.setStyleSheet("border-radius:5px;\n"
        "border-color: rgb(255, 255, 255);\n"
        "background-color: rgb(255, 255, 255);")
                self.dir.setWordWrap(True)
                self.dir.setObjectName("dir")
                self.verticalLayout_2.addWidget(self.dir)
                self.pushButton = QtWidgets.QPushButton(parent=self.widget_3)
                self.pushButton.setObjectName("pushButton")
                self.verticalLayout_2.addWidget(self.pushButton)
                self.n.setText(item["name"])
                self.dir.setText(item["exedir"])
                self.pushButton.setText("run")
                self.horizontalLayout.addWidget(self.newwidget_3)
                if(os.path.isfile(item["exedir"])):
                    print("run")
                    self.pushButton.clicked.connect(lambda: self.run(item["exedir"]))
        elif(mode=="sort"):
            for item in glist.sort():
                parentdir = Path(item["exedir"])
                parentdir = str(parentdir.parent.absolute())
                self.newwidget_3 = QtWidgets.QWidget(parent=self.scrollAreaWidgetContents)
                self.newwidget_3.setMinimumSize(QtCore.QSize(200, 500))
                self.newwidget_3.setMaximumSize(QtCore.QSize(200, 500))
                self.newwidget_3.setStyleSheet("background-color: rgb(170, 255, 255);")
                self.newwidget_3.setObjectName("widget_3")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.newwidget_3)
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.img = QtWidgets.QLabel(parent=self.newwidget_3)
                self.img.setText("")
                if(os.path.isfile(parentdir+"/icon.png")):
                    self.img.setPixmap(QtGui.QPixmap(parentdir+"/icon.png"))
                else:
                    self.img.setPixmap(QtGui.QPixmap("img/null.png"))
                self.img.setScaledContents(True)
                self.img.setObjectName("img")
                self.verticalLayout_2.addWidget(self.img)
                self.n = QtWidgets.QLabel(parent=self.newwidget_3)
                self.n.setMinimumSize(QtCore.QSize(0, 20))
                self.n.setMaximumSize(QtCore.QSize(16777215, 90))
                self.n.setStyleSheet("border-radius:5px;\n"
        "border-color: rgb(255, 255, 255);\n"
        "background-color: rgb(255, 255, 255);")
                self.n.setObjectName("n")
                self.verticalLayout_2.addWidget(self.n)
                self.dir = QtWidgets.QLabel(parent=self.newwidget_3)
                self.dir.setMinimumSize(QtCore.QSize(0, 20))
                self.dir.setMaximumSize(QtCore.QSize(16777215, 90))
                self.dir.setStyleSheet("border-radius:5px;\n"
        "border-color: rgb(255, 255, 255);\n"
        "background-color: rgb(255, 255, 255);")
                self.dir.setWordWrap(True)
                self.dir.setObjectName("dir")
                self.verticalLayout_2.addWidget(self.dir)
                self.pushButton = QtWidgets.QPushButton(parent=self.widget_3)
                self.pushButton.setObjectName("pushButton")
                self.verticalLayout_2.addWidget(self.pushButton)
                self.n.setText(item["name"])
                self.dir.setText(item["exedir"])
                self.pushButton.setText("run")
                self.horizontalLayout.addWidget(self.newwidget_3)
                if(os.path.isfile(item["exedir"])):
                    print("run")
                    self.pushButton.clicked.connect(lambda: self.run(item["exedir"]))
        elif(mode=="search"):
            for item in glist.search(self.search.text()):
                parentdir = Path(item["exedir"])
                parentdir = str(parentdir.parent.absolute())
                self.newwidget_3 = QtWidgets.QWidget(parent=self.scrollAreaWidgetContents)
                self.newwidget_3.setMinimumSize(QtCore.QSize(200, 500))
                self.newwidget_3.setMaximumSize(QtCore.QSize(200, 500))
                self.newwidget_3.setStyleSheet("background-color: rgb(170, 255, 255);")
                self.newwidget_3.setObjectName("widget_3")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.newwidget_3)
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.img = QtWidgets.QLabel(parent=self.newwidget_3)
                self.img.setText("")
                if(os.path.isfile(parentdir+"/icon.png")):
                    self.img.setPixmap(QtGui.QPixmap(parentdir+"/icon.png"))
                else:
                    self.img.setPixmap(QtGui.QPixmap("img/null.png"))
                self.img.setScaledContents(True)
                self.img.setObjectName("img")
                self.verticalLayout_2.addWidget(self.img)
                self.n = QtWidgets.QLabel(parent=self.newwidget_3)
                self.n.setMinimumSize(QtCore.QSize(0, 20))
                self.n.setMaximumSize(QtCore.QSize(16777215, 90))
                self.n.setStyleSheet("border-radius:5px;\n"
        "border-color: rgb(255, 255, 255);\n"
        "background-color: rgb(255, 255, 255);")
                self.n.setObjectName("n")
                self.verticalLayout_2.addWidget(self.n)
                self.dir = QtWidgets.QLabel(parent=self.newwidget_3)
                self.dir.setMinimumSize(QtCore.QSize(0, 20))
                self.dir.setMaximumSize(QtCore.QSize(16777215, 90))
                self.dir.setStyleSheet("border-radius:5px;\n"
        "border-color: rgb(255, 255, 255);\n"
        "background-color: rgb(255, 255, 255);")
                self.dir.setWordWrap(True)
                self.dir.setObjectName("dir")
                self.verticalLayout_2.addWidget(self.dir)
                self.pushButton = QtWidgets.QPushButton(parent=self.widget_3)
                self.pushButton.setObjectName("pushButton")
                self.verticalLayout_2.addWidget(self.pushButton)
                self.n.setText(item["name"])
                self.dir.setText(item["exedir"])
                self.pushButton.setText("run")
                self.horizontalLayout.addWidget(self.newwidget_3)
                if(os.path.isfile(item["exedir"])):
                    print("run")
                    self.pushButton.clicked.connect(lambda: self.run(item["exedir"]))            
    def click2(self):
        QtUtility.change(self,home)
    def run(self,dir:str):
        try:
            os.startfile(dir)
        except:
            pass
class Mod(mod.Ui_MainWindow,PyQt6.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def loadgame(self):
        self.listWidget.clear()
        for item in glist.list:
            self.listWidget.addItem(str(item["id"])+" "+item["name"])
    def loadfolder(self,dir):
        self.listWidget_2.clear()
        for item in os.listdir(dir):
            self.listWidget_2.addItem(item)
    def loaditem(self,dir):
        self.listWidget_3.clear()
        for item in os.listdir(dir):
            self.listWidget_3.addItem(item)
app = PyQt6.QtWidgets.QApplication(sys.argv)
home = Home()
login = Login()
signup = Signup()
Selection = selections()
mod = Mod()
box1 = add()
box2 = change()
login.show()
app.exec()