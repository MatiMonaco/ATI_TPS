from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets


class RawSizeInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.onlyInt = QIntValidator()
        self.onlyInt.setBottom(0)
        self.first = QtWidgets.QLineEdit(self)
        self.first.setValidator(self.onlyInt)
        self.second = QtWidgets.QLineEdit(self)
        self.second.setValidator(self.onlyInt)
        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok, self)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Width", self.first)
        layout.addRow("Height", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.rejected)

        pixmapi = getattr(QtWidgets.QStyle, 'SP_DirOpenIcon')
        icon = self.style().standardIcon(pixmapi)
        self.setWindowIcon(icon)

        self.setWindowTitle("Enter RAW Image Dimensions")

    def getInputs(self):
        w = self.first.text()
        h = self.second.text()
        if w == '' or h == '':
            return 0, 0
        return int(w), int(h)
