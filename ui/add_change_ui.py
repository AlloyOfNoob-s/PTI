# Form implementation generated from reading ui file 'c:\Users\Acer\Desktop\PTI\ui\add_change.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(457, 332)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.t3 = QtWidgets.QPlainTextEdit(parent=Dialog)
        self.t3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.t3.setObjectName("t3")
        self.verticalLayout.addWidget(self.t3)
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.t2 = QtWidgets.QPlainTextEdit(parent=Dialog)
        self.t2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.t2.setObjectName("t2")
        self.verticalLayout.addWidget(self.t2)
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.t1 = QtWidgets.QPlainTextEdit(parent=Dialog)
        self.t1.setMaximumSize(QtCore.QSize(16777215, 50))
        self.t1.setObjectName("t1")
        self.verticalLayout.addWidget(self.t1)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Name"))
        self.label_2.setText(_translate("Dialog", ".exe directory"))
        self.label_3.setText(_translate("Dialog", "Mod folder (gamefolder/mod or gamefolder/modloader/mod)"))
