import sys

from dialogBoxes import MultipleInputDialog

from Resources.design import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtGui import QIcon

class DebtCalculator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.uiManager = Ui_MainWindow()
        self.uiManager.setupUi(self)
        self.setWindowTitle("Debt Calculator")
        self.setWindowIcon(QIcon("Resources/iconDebt.png"))
        self.initActions()

    def initActions(self):
        self.uiManager.btnAddEntryUser1.clicked.connect(self.action_btnAddEntryUser1)

    def action_btnAddEntryUser1(self):
        inputBox = MultipleInputDialog(parent=self, labelArr=["Name:", "Debt:", "Date:"])
        inputBox.exec()
        newEntryData = inputBox.getResult()
        if len(newEntryData) > 0:




def runApp():
    myApp = QtWidgets.QApplication(sys.argv)
    myWindow = DebtCalculator()
    myWindow.show()
    myApp.exec()

runApp()