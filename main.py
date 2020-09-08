import sys
from PyQt5 import QtCore, QtWidgets, QtSql
from MainUi import Ui_MainWindow
from DataBaseUi import Ui_Form
from createDBUI import Ui_Dialog
import addEntryUi
import os



class main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.checkDatabase()
        self.ui.delcreate.clicked.connect(self.newDB)
        self.ui.enter.clicked.connect(lambda: self.enter(self.ui.master.text()))

        self.show()

    def checkDatabase(self):
        if not os.path.isfile("./passwords.db"):
            self.diag = QtWidgets.QDialog()
            ui = Ui_Dialog()
            ui.setupUi(self.diag)
            ui.pushButton.clicked.connect(lambda: self.apply(ui.lineEdit.text()))

            self.diag.exec_()

        else:
            self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName("passwords.db")
            self.db.open()


    def apply(self, master):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName("passwords.db")
        self.db.open()
        query = QtSql.QSqlQuery()
        query.exec_(
            """
            CREATE TABLE IF NOT EXISTS passlist (description TEXT, password TEXT );
            """
        )
        query.prepare("INSERT INTO passlist values (:mass,:pass)")
        query.bindValue(":pass", master)
        query.bindValue(":mass", "Master")
        query.exec_()
        self.diag.close()

    def newDB(self):
        r = QtWidgets.QMessageBox.question(self, "New Database", "Create a new Safe? Previous one will be deleted!", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if r == QtWidgets.QMessageBox.Yes:
            self.db.close()
            del self.db
            QtSql.QSqlDatabase.removeDatabase("passwords")
            #os.remove("./passwords.db")
            self.checkDatabase()

    def enter(self,data):
        query = QtSql.QSqlQuery()
        query.exec_("SELECT *  FROM passlist")
        query.next() #goes to first row
        if query.value(1) == data:    # index indicates columns
            self.second = QtWidgets.QWidget()
            self.secondUI = Ui_Form()
            self.secondUI.setupUi(self.second)
            self.secondUI.addEntry.clicked.connect(self. openEntry)
            self.secondUI.showSelected.clicked.connect(self.display)
            self.secondUI.removeSelected.clicked.connect(self.remove)
            self.secondUI.editSelected.clicked.connect(self.edit)
            self.showList()
            self.second.show()
        else:
            QtWidgets.QMessageBox.critical(self,"Incorrect password", "Password is not correct, Please try again!")

    def openEntry(self):
        add = QtWidgets.QDialog()
        addUi = addEntryUi.Ui_Dialog()
        addUi.setupUi(add)
        addUi.buttonBox.accepted.connect(lambda: self.addData(addUi.lineEdit_Description.text(), addUi.lineEdit_Password.text()))

        add.exec_()

    def addData(self,dis,password):
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO passlist values(?,?)")
        query.addBindValue(dis)
        query.addBindValue(password)
        query.exec_()
        self.model.select()

    def showList(self):
        self.model = QtSql.QSqlTableModel()
        self.model.setTable("passlist")
        self.secondUI.listView.setModel(self.model)
        self.secondUI.listView.setSelectionMode(QtWidgets.QListView.SingleSelection)
        #self.secondUI.listView.setEditTriggers(QtWidgets.QListView.NoEditTriggers)
        self.model.select()

    def display(self):
        indexes = self.secondUI.listView.selectedIndexes()
        if indexes:
            index = indexes[0].row()
            password = self.model.record(index).value("password")
            QtWidgets.QMessageBox.information(self.second, "Password", password)
        else:
            QtWidgets.QMessageBox.critical(self.second,"Error", "You must select an item first")

    def remove(self):
        indexes = self.secondUI.listView.selectedIndexes()
        if indexes:
            r = QtWidgets.QMessageBox.question(self.second, 'Remove', "Are you sure to remove the selected entry",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if r == QtWidgets.QMessageBox.Yes:
                index = indexes[0].row()
                if index ==0:
                    QtWidgets.QMessageBox.critical(self.second, "Error", "Can not delete master password")
                else:
                    self.model.removeRow(index)
                    self.model.select()
        else:
            QtWidgets.QMessageBox.critical(self.second, "Error", "You must select an item first")

    def edit(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self.second, "Edit Password", "Enter new password:", QtWidgets.QLineEdit.Normal, "")
        indexes = self.secondUI.listView.selectedIndexes()
        if indexes:
            if okPressed:
                index = indexes[0].row()
                record = self.model.record()
                des =self.model.record(index).value("description")
                record.setValue(0,des)
                record.setValue(1,text)
                self.model.setRecord(index, record)
                self.model.select()
        else:
            QtWidgets.QMessageBox.critical(self.second, "Error", "You must select an item first")

    def closeEvent(self,e):
        self.db.close()

app = QtWidgets.QApplication(sys.argv)
ex = main()
sys.exit(app.exec_())
