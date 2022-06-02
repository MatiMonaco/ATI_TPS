from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets


class ModifyPixelDialog(QtWidgets.QDialog):
    def __init__(self, max_width, max_height, parent=None):
        super().__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.gridLayout = QtWidgets.QGridLayout()

        self.R_line_edit = QtWidgets.QLineEdit(self)

        self.gridLayout.addWidget(self.R_line_edit, 1, 1, 1, 1)
        self.B_label = QtWidgets.QLabel(self)
        self.B_label.setText("B")
        self.gridLayout.addWidget(self.B_label, 1, 4, 1, 1)
        self.y_label = QtWidgets.QLabel(self)
        self.y_label.setText("Y")

        self.gridLayout.addWidget(self.y_label, 0, 2, 1, 1)
        self.G_label = QtWidgets.QLabel(self)
        self.G_label.setText("G")
        self.gridLayout.addWidget(self.G_label, 1, 2, 1, 1)
        self.x_label = QtWidgets.QLabel(self)
        self.x_label.setText("X")

        self.gridLayout.addWidget(self.x_label, 0, 0, 1, 1)
        self.x_line_edit = QtWidgets.QLineEdit(self)

        self.gridLayout.addWidget(self.x_line_edit, 0, 1, 1, 1)
        self.R_label = QtWidgets.QLabel(self)
        self.R_label.setText("R")
        self.gridLayout.addWidget(self.R_label, 1, 0, 1, 1)
        self.y_line_edit = QtWidgets.QLineEdit(self)

        self.gridLayout.addWidget(self.y_line_edit, 0, 3, 1, 1)
        self.G_line_edit = QtWidgets.QLineEdit(self)

        self.gridLayout.addWidget(self.G_line_edit, 1, 3, 1, 1)
        self.B_line_edit = QtWidgets.QLineEdit(self)

        self.gridLayout.addWidget(self.B_line_edit, 1, 5, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

        width_validator = QIntValidator(0, max_width)
        height_validator = QIntValidator(0, max_height)
        color_validator = QIntValidator(0, 255)

        self.x_line_edit.setValidator(width_validator)
        self.y_line_edit.setValidator(height_validator)
        self.R_line_edit.setValidator(color_validator)
        self.G_line_edit.setValidator(color_validator)
        self.B_line_edit.setValidator(color_validator)

        self.x_line_edit.setStyleSheet("font-weight: bold")
        self.y_line_edit.setStyleSheet("font-weight: bold")
        self.R_line_edit.setStyleSheet("font-weight: bold")
        self.G_line_edit.setStyleSheet("font-weight: bold")
        self.B_line_edit.setStyleSheet("font-weight: bold")

    def getInputs(self):
        x = int(self.x_line_edit.text())
        y = int(self.y_line_edit.text())
        r = int(self.R_line_edit.text())
        g = int(self.G_line_edit.text())
        b = int(self.B_line_edit.text())
        return x, y, r, g, b
