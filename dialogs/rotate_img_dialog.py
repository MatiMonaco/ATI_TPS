from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets


class RotateImgDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.gridLayout = QtWidgets.QGridLayout()
        self.deg_label = QtWidgets.QLabel(self)
        self.deg_label.setText("Degrees")

        self.gridLayout.addWidget(self.deg_label, 0, 0, 1, 1)
        self.deg_line_edit = QtWidgets.QLineEdit(self)

        self.gridLayout.addWidget(self.deg_line_edit, 0, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

        deg_validator = QDoubleValidator()

        self.deg_line_edit.setValidator(deg_validator)

        self.deg_line_edit.setStyleSheet("font-weight: bold")

    def getInput(self):
        return float(self.deg_line_edit.text())
