from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialogButtonBox
import datetime

class MultipleInputDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, labelArr=None):
        super().__init__(parent)
        self.setWindowTitle("New Entry")
        self.lineEdits = []
        self.resultList = []

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        if labelArr is None:
            labelArr = ["Input"]

        for i in range(len(labelArr)):
            self.lineEdits.append(QtWidgets.QLineEdit(parent=self))

        layout = QtWidgets.QFormLayout(self)
        for ix, inp in enumerate(labelArr):
            if inp == "Date:":
                now = datetime.datetime.now()
                now = now.date()
                self.lineEdits[ix].setText(str(now))
            layout.addRow(inp, self.lineEdits[ix])

        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.action_btnOk)
        buttonBox.rejected.connect(self.reject)

    def action_btnOk(self):
        for lineEdit in self.lineEdits:
            self.resultList.append(lineEdit.text())
        self.accept()

    def getResult(self):
        return self.resultList
