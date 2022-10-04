import sys
import json

from dialogBoxes import MultipleInputDialog
from databaseManager import DBManager

from Resources.design import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem

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
        inputBox = MultipleInputDialog(parent=self, labelArr=["Name:", "Debt:", "Date:"])
        inputBox.exec()
        newEntryData = inputBox.getResult()
        if len(newEntryData) > 0:
            name, debt, date = newEntryData
            dbManager = DBManager()
            dbManager.addRow("debtUser1toUser2", name, debt, date)
            self.loadTables()
            self.calculateDebt("debtUser1toUser2")

    def action_btnChangeUser1Name(self):
        oldName = self.uiManager.labelUser1_1.text()
        inputBox = MultipleInputDialog(parent=self, labelArr=[f"Change {oldName} to "])
        inputBox.exec()
        newName = inputBox.getResult()
        if not newName:
            pass
        else:
            with open("Data/texts.json") as file:
                texts = json.load(file)
            texts["user1"] = newName
            with open("Data/texts.json", "w") as file:
                json.dump(texts, file)

            self.initTexts()

    def action_btnChangeUser2Name(self):
        oldName = self.uiManager.labelUser2_1.text()
        inputBox = MultipleInputDialog(parent=self, labelArr=[f"Change {oldName} to "])
        inputBox.exec()
        newName = inputBox.getResult()
        if not newName:
            pass
        else:
            with open("Data/texts.json") as file:
                texts = json.load(file)
            texts["user2"] = newName
            with open("Data/texts.json", "w") as file:
                json.dump(texts, file)

            self.initTexts()

def runApp():
    myApp = QtWidgets.QApplication(sys.argv)
    myWindow = DebtCalculator()
    myWindow.show()
    myApp.exec()

runApp()