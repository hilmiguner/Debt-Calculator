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
        self.setFixedSize(self.width(), self.height())
        self.uiManager.tableUser1toUser2.hideColumn(0)
        self.uiManager.tableUser2toUser1.hideColumn(0)

        self.initTexts()
        self.calculateDebt("user1", 0)
        self.calculateDebt("user2", 0)
        self.initActions()

        self.loadTables()

    def initActions(self):
        self.uiManager.btnAddEntryUser1.clicked.connect(self.action_btnAddEntryUser1)
        self.uiManager.btnAddEntryUser2.clicked.connect(self.action_btnAddEntryUser2)

        self.uiManager.btnChangeUser1Name.clicked.connect(self.action_btnChangeUser1Name)
        self.uiManager.btnChangeUser2Name.clicked.connect(self.action_btnChangeUser2Name)

        self.uiManager.btnDeleteEntryUser1.clicked.connect(self.action_btnDeleteEntryUser1)
        self.uiManager.btnDeleteEntryUser2.clicked.connect(self.action_btnDeleteEntryUser2)

        self.uiManager.tableUser1toUser2.cellDoubleClicked.connect(self.action_tableUser1toUser2CellDoubleClicked)
        self.uiManager.tableUser2toUser1.cellDoubleClicked.connect(self.action_tableUser2toUser1CellDoubleClicked)

        self.uiManager.btnClearTable1.clicked.connect(self.action_btnClearTable1)
        self.uiManager.btnClearTable2.clicked.connect(self.action_btnClearTable2)

    def initTexts(self):
        self.user1Name = self.textDict["user1"]
        self.user2Name = self.textDict["user2"]

        self.uiManager.labelUser1_1.setText(self.user1Name)
        self.uiManager.labelUser2_1.setText(self.user2Name)
        self.uiManager.labelUser1_2.setText(self.user1Name)
        self.uiManager.labelUser2_2.setText(self.user2Name)

        self.uiManager.btnChangeUser1Name.setText("Rename '{}'".format(self.user1Name))
        self.uiManager.btnChangeUser2Name.setText("Rename '{}'".format(self.user2Name))

    def loadTables(self):
        dbManager = DBManager()
        dataList = dbManager.getRows("debtUser1toUser2")

        self.uiManager.tableUser1toUser2.setRowCount(len(dataList))
        for ix, data in enumerate(dataList):
            self.uiManager.tableUser1toUser2.setItem(ix, 0, QTableWidgetItem(str(data[0])))
            self.uiManager.tableUser1toUser2.setItem(ix, 1, QTableWidgetItem(data[1]))
            self.uiManager.tableUser1toUser2.setItem(ix, 2, QTableWidgetItem(str(data[2])))
            self.uiManager.tableUser1toUser2.setItem(ix, 3, QTableWidgetItem(data[3]))

        dataList = dbManager.getRows("debtUser2toUser1")

        self.uiManager.tableUser2toUser1.setRowCount(len(dataList))
        for ix, data in enumerate(dataList):
            self.uiManager.tableUser2toUser1.setItem(ix, 0, QTableWidgetItem(str(data[0])))
            self.uiManager.tableUser2toUser1.setItem(ix, 1, QTableWidgetItem(data[1]))
            self.uiManager.tableUser2toUser1.setItem(ix, 2, QTableWidgetItem(str(data[2])))
            self.uiManager.tableUser2toUser1.setItem(ix, 3, QTableWidgetItem(data[3]))

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
            self.uiManager.labelTotalUser2.setText(f"Total: {self.textDict['debtFromUser2ToUser1']}")
        self.netDebt()

    def netDebt(self):
        u1_to_u2 = self.textDict["debtFromUser1ToUser2"]
        u2_to_u1 = self.textDict["debtFromUser2ToUser1"]
        text = ""
        if u2_to_u1 == u1_to_u2:
            text = "Net debt is zero."
        elif u1_to_u2 > u2_to_u1:
            debt = u1_to_u2 - u2_to_u1
            if len(str(debt).split(".")[1]) > 3:
                debt = float(str(debt)[:-(len(str(debt).split(".")[1]) - 3)])
            text = f"{self.user1Name}\nowes {debt} to\n{self.user2Name}"
        elif u2_to_u1 > u1_to_u2:
            debt = u2_to_u1 - u1_to_u2
            if len(str(debt).split(".")[1]) > 3:
                debt = float(str(debt)[:-(len(str(debt).split(".")[1]) - 3)])
            text = f"{self.user2Name}\nowes {debt} to\n{self.user1Name}"
        self.uiManager.labelNetDebt.setText(text)

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
                try:
                    debt = float(debt)
                except Exception as err:
                    print("Error Message -> ", err)
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
                try:
                    debt = float(debt)
                except Exception as err:
                    print("Error Message -> ", err)
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
            self.netDebt()

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
            self.netDebt()

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

            self.calculateDebt("user1", -float(rowValues[2].text()))
            self.uiManager.tableUser1toUser2.removeRow(selectedItemRow)

    def action_btnDeleteEntryUser2(self):
        table = self.uiManager.tableUser2toUser1
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
            dbManager.deleteRow("debtUser2toUser1", rowValues[0].text())

            self.calculateDebt("user2", -float(rowValues[2].text()))
            self.uiManager.tableUser2toUser1.removeRow(selectedItemRow)

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
        if len(response) == 3 and (response[0] == '' or response[1] == '' or response[2] == ''):
            msgBox = QMessageBox(parent=self)

            msgBox.setWindowTitle("Alert!")
            msgBox.setText("You must fill all the blanks.")
            msgBox.setStandardButtons(QMessageBox.Ok)

            msgBox.exec()
            return
        elif response:
            try:
                response[1] = float(response[1])
                response[1] = str(response[1])
            except Exception as err:
                print("Error Message -> ", err)
                msgBox = QMessageBox(parent=self)

                msgBox.setWindowTitle("Alert!")
                msgBox.setText("Debt must be numerical.")
                msgBox.setStandardButtons(QMessageBox.Ok)

                msgBox.exec()
                return
            ID = table.item(selectedItemsRow, 0).text()
            debtDiff = float(response[1]) - float(selectedItems[1].text())

            dbManager = DBManager()
            dbManager.editRow("debtUser1toUser2", ID, [response[0], response[1], response[2]])
            table.setItem(selectedItemsRow, 1, QTableWidgetItem(response[0]))
            table.setItem(selectedItemsRow, 2, QTableWidgetItem(response[1]))
            table.setItem(selectedItemsRow, 3, QTableWidgetItem(response[2]))
            self.calculateDebt("user1", debtDiff)

    def action_tableUser2toUser1CellDoubleClicked(self):
        table = self.uiManager.tableUser2toUser1
        selectedItems = table.selectedItems()
        selectedItemsRow = selectedItems[0].row()

        inputBox = MultipleInputDialog(parent=self, windowTitle="Editing an entry", labelArr=["Name:", "Debt:", "Date:"])
        inputBox.lineEdits[0].setText(selectedItems[0].text())
        inputBox.lineEdits[1].setText(selectedItems[1].text())
        inputBox.lineEdits[2].setText(selectedItems[2].text())
        inputBox.exec()
        response = inputBox.getResult()
        if len(response) == 3 and (response[0] == '' or response[1] == '' or response[2] == ''):
            msgBox = QMessageBox(parent=self)

            msgBox.setWindowTitle("Alert!")
            msgBox.setText("You must fill all the blanks.")
            msgBox.setStandardButtons(QMessageBox.Ok)

            msgBox.exec()
            return
        elif response:
            try:
                response[1] = float(response[1])
                response[1] = str(response[1])
            except Exception as err:
                print("Error Message -> ", err)
                msgBox = QMessageBox(parent=self)

                msgBox.setWindowTitle("Alert!")
                msgBox.setText("Debt must be numerical.")
                msgBox.setStandardButtons(QMessageBox.Ok)

                msgBox.exec()
                return
            ID = table.item(selectedItemsRow, 0).text()

            debtDiff = float(response[1]) - float(selectedItems[1].text())

            dbManager = DBManager()
            dbManager.editRow("debtUser2toUser1", ID, [response[0], response[1], response[2]])
            table.setItem(selectedItemsRow, 1, QTableWidgetItem(response[0]))
            table.setItem(selectedItemsRow, 2, QTableWidgetItem(response[1]))
            table.setItem(selectedItemsRow, 3, QTableWidgetItem(response[2]))
            self.calculateDebt("user2", debtDiff)

    def action_btnClearTable1(self):
        if self.uiManager.tableUser1toUser2.rowCount() == 0:
            QMessageBox.warning(
                self,
                "No Data to Clear",
                "There is no data to clear in table 1",
                QMessageBox.Ok,
                QMessageBox.Ok
            )
            return
        else:
            alertBox = QMessageBox.warning(
                self,
                "ALERT !!",
                "ARE YOU SURE TO DELETE ALL THE DATA FROM TABLE 1 ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if alertBox == QMessageBox.Yes:
                dbManager = DBManager()
                dbManager.deleteRow("debtUser1ToUser2")
                self.loadTables()
                self.calculateDebt("user1", -(self.textDict["debtFromUser1ToUser2"]))

    def action_btnClearTable2(self):
        if self.uiManager.tableUser2toUser1.rowCount() == 0:
            QMessageBox.warning(
                self,
                "No Data to Clear",
                "There is no data to clear in table 2",
                QMessageBox.Ok,
                QMessageBox.Ok
            )
            return
        else:
            alertBox = QMessageBox.warning(
                self,
                "ALERT !!",
                "ARE YOU SURE TO DELETE ALL THE DATA FROM TABLE 2 ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if alertBox == QMessageBox.Yes:
                dbManager = DBManager()
                dbManager.deleteRow("debtUser2ToUser1")
                self.loadTables()
                self.calculateDebt("user2", -(self.textDict["debtFromUser2ToUser1"]))

def runApp():
    myApp = QtWidgets.QApplication(sys.argv)
    myWindow = DebtCalculator()
    myWindow.show()
    myApp.exec()

runApp()