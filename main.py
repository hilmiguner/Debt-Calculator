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
        with open("Data/texts.json") as file:
            self.textDict = json.load(file)
        self.user1Name = self.textDict["user1"]
        self.user2Name = self.textDict["user2"]
        # *************

        self.setWindowTitle("Debt Calculator")
        self.setWindowIcon(QIcon("Resources/iconDebt.png"))
        self.uiManager.tableUser1toUser2.setColumnHidden(0, True)

        self.initTexts()
        self.calculateDebt("user1", self.textDict['debtFromUser1ToUser2'])
        # self.calculateDebt("user2", self.textDict['debtFromUser2ToUser1'])
        self.initActions()

        self.loadTables()

    def initActions(self):
        self.uiManager.btnAddEntryUser1.clicked.connect(self.action_btnAddEntryUser1)
        self.uiManager.btnChangeUser1Name.clicked.connect(self.action_btnChangeUser1Name)
        self.uiManager.btnChangeUser2Name.clicked.connect(self.action_btnChangeUser2Name)
        self.uiManager.btnDeleteEntryUser1.clicked.connect(self.action_btnDeleteEntryUser1)
        self.uiManager.tableUser1toUser2.cellDoubleClicked.connect(self.action_tableUser1toUser2CellDoubleClicked)

    def initTexts(self):
        self.user1Name = self.textDict["user1"]
        self.user2Name = self.textDict["user2"]

        self.uiManager.labelUser1_1.setText(self.user1Name)
        self.uiManager.labelUser2_1.setText(self.user2Name)
        # self.uiManager.labelUser1_2.setText(self.user1Name)
        # self.uiManager.labelUser2_2.setText(self.user2Name)

        self.uiManager.btnChangeUser1Name.setText("Rename '{}'".format(self.user1Name))
        self.uiManager.btnChangeUser2Name.setText("Rename '{}'".format(self.user2Name))

    def loadTables(self):
        dbManager = DBManager()
        dataList = dbManager.getRows("debtUser1toUser2")

        self.uiManager.tableUser1toUser2.setRowCount(len(dataList))
        for ix, data in enumerate(dataList):
            self.uiManager.tableUser1toUser2.setItem(ix, 0, QTableWidgetItem(data[0]))
            self.uiManager.tableUser1toUser2.setItem(ix, 1, QTableWidgetItem(data[1]))
            self.uiManager.tableUser1toUser2.setItem(ix, 2, QTableWidgetItem(str(data[2])))
            self.uiManager.tableUser1toUser2.setItem(ix, 3, QTableWidgetItem(data[3]))

        # dataList = dbManager.getRows("debtUser2toUser1")
        #
        # self.uiManager.tableUser2toUser1.setRowCount(len(dataList))
        # for ix, data in enumerate(dataList):
        #     self.uiManager.tableUser2toUser1.setItem(ix, 0, QTableWidgetItem(data[0]))
        #     self.uiManager.tableUser2toUser1.setItem(ix, 1, QTableWidgetItem(data[1]))
        #     self.uiManager.tableUser2toUser1.setItem(ix, 2, QTableWidgetItem(str(data[2])))
        #     self.uiManager.tableUser2toUser1.setItem(ix, 3, QTableWidgetItem(data[3]))

    def calculateDebt(self, whichUser: str, value: float):
        if whichUser == "user1":
            self.textDict["debtFromUser1ToUser2"] += value
            with open("Data/texts.json", "w") as file:
                json.dump(self.textDict, file)
            self.uiManager.labelTotalUser1.setText(f"Total: {self.textDict['debtFromUser1ToUser2']}")
        elif whichUser == "user2":
            self.textDict["debtFromUser2ToUser1"] += value
            with open("Data/texts.json", "w") as file:
                json.dump(self.textDict, file)
            # self.uiManager.labelTotalUser2.setText(f"Total: {self.textDict['debtFromUser2ToUser1']}")

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
                self.calculateDebt("user1", debt)

    def action_btnAddEntryUser2(self):
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
                dbManager.addRow("debtUser2toUser1", name, debt, date)
                self.loadTables()
                self.calculateDebt("user2", debt)

    def action_btnChangeUser1Name(self):
        oldName = self.user1Name
        inputBox = MultipleInputDialog(parent=self, windowTitle="Rename", labelArr=[f"Change {oldName} to "])
        inputBox.exec()
        newName = inputBox.getResult()
        if newName:
            self.textDict["user1"] = newName
            with open("Data/texts.json", "w") as file:
                json.dump(self.textDict, file)

            self.initTexts()

    def action_btnChangeUser2Name(self):
        oldName = self.user2Name
        inputBox = MultipleInputDialog(parent=self, windowTitle="Rename", labelArr=[f"Change {oldName} to "])
        inputBox.exec()
        newName = inputBox.getResult()
        if newName:
            self.textDict["user2"] = newName
            with open("Data/texts.json", "w") as file:
                json.dump(self.textDict, file)

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
        selectedItemRow = selectedItems[0].row()
        rowValues = [table.item(selectedItemRow, 0), table.item(selectedItemRow, 1), table.item(selectedItemRow, 2), table.item(selectedItemRow, 3)]

        messageBox = QMessageBox(parent=self)

        messageBox.setWindowTitle("Deleting Item")
        text = f"Are you sure want to delete this entry ?\nName: {rowValues[1].text()}\nDebt: {rowValues[2].text()}\nDate: {rowValues[3].text()}"
        messageBox.setText(text)
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = messageBox.exec()
        if response == QMessageBox.Yes:
            dbManager = DBManager()
            dbManager.deleteRow("debtUser1toUser2", rowValues[0].text())

            self.uiManager.tableUser1toUser2.removeRow(selectedItemRow)
            self.calculateDebt("user1", -rowValues[2])

    # def action_btnDeleteEntryUser2(self):
    #     table = self.uiManager.tableUser2toUser1
    #     selectedItems = table.selectedItems()
    #     if not selectedItems:
    #         alertBox = QMessageBox(parent=self)
    #
    #         alertBox.setText("There is no selected item.")
    #         alertBox.setWindowTitle("Alert")
    #         alertBox.setStandardButtons(QMessageBox.Ok)
    #
    #         alertBox.exec()
    #         return
    #     selectedItemRow = selectedItems[0].row()
    #     rowValues = [table.item(selectedItemRow, 0), table.item(selectedItemRow, 1), table.item(selectedItemRow, 2), table.item(selectedItemRow, 3)]
    #
    #     messageBox = QMessageBox(parent=self)
    #
    #     messageBox.setWindowTitle("Deleting Item")
    #     text = f"Are you sure want to delete this entry ?\nName: {rowValues[1].text()}\nDebt: {rowValues[2].text()}\nDate: {rowValues[3].text()}"
    #     messageBox.setText(text)
    #     messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    #
    #     response = messageBox.exec()
    #     if response == QMessageBox.Yes:
    #         dbManager = DBManager()
    #         dbManager.deleteRow("debtUser2toUser1", rowValues[0].text())
    #
    #         self.uiManager.tableUser2toUser1.removeRow(selectedItemRow)
    #         self.calculateDebt("user2", -rowValues[2])

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
            ID = table.item(selectedItemsRow, 0)

            dbManager = DBManager()
            dbManager.editRow("debtUser1toUser2", ID, [response[0], response[1], response[2]])
            table.setItem(selectedItemsRow, 1, QTableWidgetItem(response[0]))
            table.setItem(selectedItemsRow, 2, QTableWidgetItem(response[1]))
            table.setItem(selectedItemsRow, 3, QTableWidgetItem(response[2]))
            self.calculateDebt("user1", response[1])

    # def action_tableUser2toUser1CellDoubleClicked(self):
    #     table = self.uiManager.tableUser2toUser1
    #     selectedItems = table.selectedItems()
    #     selectedItemsRow = selectedItems[0].row()
    #
    #     inputBox = MultipleInputDialog(parent=self, windowTitle="Editing an entry", labelArr=["Name:", "Debt:", "Date:"])
    #     inputBox.lineEdits[0].setText(selectedItems[0].text())
    #     inputBox.lineEdits[1].setText(selectedItems[1].text())
    #     inputBox.lineEdits[2].setText(selectedItems[2].text())
    #     inputBox.exec()
    #     response = inputBox.getResult()
    #     if response:
    #         ID = table.item(selectedItemsRow, 0)
    #
    #         dbManager = DBManager()
    #         dbManager.editRow("debtUser2toUser1", ID, [response[0], response[1], response[2]])
    #         table.setItem(selectedItemsRow, 1, QTableWidgetItem(response[0]))
    #         table.setItem(selectedItemsRow, 2, QTableWidgetItem(response[1]))
    #         table.setItem(selectedItemsRow, 3, QTableWidgetItem(response[2]))
    #         self.calculateDebt("user2", response[1])

def runApp():
    myApp = QtWidgets.QApplication(sys.argv)
    myWindow = DebtCalculator()
    myWindow.show()
    myApp.exec()

runApp()