# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addEntryUi.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(383, 233)
        Dialog.setStyleSheet("background-color:rgb(189, 209, 255)")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 180, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit_Description = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Description.setGeometry(QtCore.QRect(52, 70, 281, 20))
        self.lineEdit_Description.setObjectName("lineEdit_Description")
        self.lineEdit_Password = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Password.setGeometry(QtCore.QRect(52, 110, 281, 20))
        self.lineEdit_Password.setObjectName("lineEdit_Password")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Entry"))
        self.lineEdit_Description.setPlaceholderText(_translate("Dialog", "Description"))
        self.lineEdit_Password.setPlaceholderText(_translate("Dialog", "Password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
