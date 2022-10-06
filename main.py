import sys
import json

from dialogBoxes import MultipleInputDialog
from databaseManager import DBManager

from Resources.design import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox

class DebtCalculator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uiManager = Ui_MainWindow()
        self.uiManager.setupUi(self)

        # Attributes
        # *************
        self.user1Name = None
        self.user2Name = None
        # *************

        self.setWindowTitle("Debt Calculator")
        self.setWindowIcon(QIcon("Resources/iconDebt.png"))

        self.initTexts()
        self.calculateDebt("debtUser1toUser2")
        # self.calculateDebt("debtUser2toUser1")
        self.initActions()

        self.loadTables()

    def initActions(self):
        self.uiManager.btnAddEntryUser1.clicked.connect(self.action_btnAddEntryUser1)
        self.uiManager.btnChangeUser1Name.clicked.connect(self.action_btnChangeUser1Name)
        self.uiManager.btnChangeUser2Name.clicked.connect(self.action_btnChangeUser2Name)
        self.uiManager.btnDeleteEntryUser1.clicked.connect(self.action_btnDeleteEntryUser1)
        self.uiManager.tableUser1toUser2.cellDoubleClicked.connect(self.action_tableUser1toUser2CellDoubleClicked)

    def initTexts(self):
        with open("Data/texts.json") as file:
            texts = json.load(file)
        self.user1Name = texts["user1"]
        self.user2Name = texts["user2"]

        self.uiManager.labelUser1_1.setText(self.user1Name)
        self.uiManager.labelUser2_1.setText(self.user2Name)

        self.uiManager.btnChangeUser1Name.setText(texts["btnRename"].format(self.user1Name))
        self.uiManager.btnChangeUser2Name.setText(texts["btnRename"].format(self.user2Name))

    def loadTables(self):
        dbManager = DBManager()
        dataList = dbManager.getRows("debtUser1toUser2")

        self.uiManager.tableUser1toUser2.setRowCount(len(dataList))
        for ix, data in enumerate(dataList):
            self.uiManager.tableUser1toUser2.setItem(ix, 0, QTableWidgetItem(data[0]))
            self.uiManager.tableUser1toUser2.setItem(ix, 1, QTableWidgetItem(str(data[1])))
            self.uiManager.tableUser1toUser2.setItem(ix, 2, QTableWidgetItem(data[2]))

    def calculateDebt(self, tableName: str):
        dbManager = DBManager()
        debts = dbManager.getRows(tableName=tableName, columns=["Debt"])
        totalDebt = 0
        for debt in debts:
            totalDebt += float(debt[0])
        self.uiManager.labelTotalUser1.setText(f"Total: {totalDebt}")

    def action_btnAddEntryUser1(self):
        inputBox = MultipleInputDialog(parent=self, windowTitle="New Entry", labelArr=["Name:", "Debt:", "Date:"])
        response = inputBox.exec()
        if response == 1:
            newEntryData = inputBox.getResult()
            if newEntryData[0] == '' or newEntryData[1] == '' or newEntryData[2] == '':
                msgBox = QMessageBox(parent=self)

                msgBox.setWindowTitle("Alert!")
                msgBox.setText("You must fill all the blanks.")
                msgBox.setStandardButtons(QMessageBox.Ok)

                msgBox.exec()
            else:
                name, debt, date = newEntryData
                if not debt.isnumeric():
                    msgBox = QMessageBox(parent=self)

                    msgBox.setWindowTitle("Alert!")
                    msgBox.setText("Debt must be numerical.")
                    msgBox.setStandardButtons(QMessageBox.Ok)

                    msgBox.exec()
                    return
                dbManager = DBManager()
                dbManager.addRow("debtUser1toUser2", name, debt, date)
                self.loadTables()
                self.calculateDebt("debtUser1toUser2")

    def action_btnChangeUser1Name(self):
        oldName = self.uiManager.labelUser1_1.text()
        inputBox = MultipleInputDialog(parent=self, windowTitle="Rename", labelArr=[f"Change {oldName} to "])
        inputBox.exec()
        newName = inputBox.getResult()
        if newName:
            with open("Data/texts.json") as file:
                texts = json.load(file)
            texts["user1"] = newName
            with open("Data/texts.json", "w") as file:
                json.dump(texts, file)

            self.initTexts()

    def action_btnChangeUser2Name(self):
        oldName = self.uiManager.labelUser2_1.text()
        inputBox = MultipleInputDialog(parent=self, windowTitle="Rename", labelArr=[f"Change {oldName} to "])
        inputBox.exec()
        newName = inputBox.getResult()
        if newName:
            with open("Data/texts.json") as file:
                texts = json.load(file)
            texts["user2"] = newName
            with open("Data/texts.json", "w") as file:
                json.dump(texts, file)

            self.initTexts()

    def action_btnDeleteEntryUser1(self):
        table = self.uiManager.tableUser1toUser2
        selectedItems = table.selectedItems()
        if not selectedItems:
            alertBox = QMessageBox(parent=self)

            alertBox.setText("There is no selected item.")
            alertBox.setWindowTitle("Alert")
            alertBox.setStandardButtons(QMessageBox.Ok)

            alertBox.exec()
            return
        selectedItem = selectedItems[0]
        selectedItemRow = selectedItem.row()
        rowValues = [table.item(selectedItemRow, 0), table.item(selectedItemRow, 1), table.item(selectedItemRow, 2)]

        messageBox = QMessageBox(parent=self)

        messageBox.setWindowTitle("Deleting Item")
        text = f"Are you sure want to delete this entry ?\nName: {rowValues[0].text()}\nDebt: {rowValues[1].text()}\nDate: {rowValues[2].text()}"
        messageBox.setText(text)
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = messageBox.exec()
        if response == QMessageBox.Yes:
            dbManager = DBManager()
            dbManager.deleteRow("debtUser1toUser2", rowValues[0].text(), rowValues[1].text(), rowValues[2].text())

            self.uiManager.tableUser1toUser2.removeRow(selectedItemRow)
            self.calculateDebt("debtUser1toUser2")

    def action_tableUser1toUser2CellDoubleClicked(self):
        table = self.uiManager.tableUser1toUser2
        selectedItems = table.selectedItems()
        selectedItemsRow = selectedItems[0].row()

        inputBox = MultipleInputDialog(parent=self, windowTitle="Editing an entry", labelArr=["Name:", "Debt:", "Date:"])
        inputBox.lineEdits[0].setText(selectedItems[0].text())
        inputBox.lineEdits[1].setText(selectedItems[1].text())
        inputBox.lineEdits[2].setText(selectedItems[2].text())
        inputBox.exec()
        response = inputBox.getResult()
        if response:
            dbManager = DBManager()
            dbManager.editRow("debtUser1toUser2", selectedItems[0].text(), selectedItems[1].text(), selectedItems[2].text(), [response[0], response[1], response[2]])
            table.setItem(selectedItemsRow, 0, QTableWidgetItem(response[0]))
            table.setItem(selectedItemsRow, 1, QTableWidgetItem(response[1]))
            table.setItem(selectedItemsRow, 2, QTableWidgetItem(response[2]))
            self.calculateDebt("debtUser1toUser2")

def runApp():
    myApp = QtWidgets.QApplication(sys.argv)
    myWindow = DebtCalculator()
    myWindow.show()
    myApp.exec()

runApp()