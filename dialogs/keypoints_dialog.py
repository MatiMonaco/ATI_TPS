from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets


class KeypointsDialog(QtWidgets.QDialog):
    def __init__(self, detector_name, keypoints1,keypoints2,matched,matched_percentage,acceptable, parent=None):
        super().__init__(parent)

        self.detector_name = detector_name

        self.keypoints1_label = QtWidgets.QLabel(self)
        self.keypoints1_label.setText(str(keypoints1))

        self.keypoints2_label = QtWidgets.QLabel(self)
        self.keypoints2_label.setText(str(keypoints2))

        self.matched_label = QtWidgets.QLabel(self)
        self.matched_label.setText(str(matched))

        self.acceptable_label = QtWidgets.QLabel(self)
        self.acceptable_label.setText(str(matched_percentage))
        self.acceptable_label.setStyleSheet(f"color: {'rgb(255,0,0)' if not acceptable else 'rgb(0,0,255)'}")

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok, self)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Keypoints in 1º image:", self.keypoints1_label)
        layout.addRow("Keypoints in 2º image:", self.keypoints2_label)
        layout.addRow("Matches found:", self.matched_label)
        layout.addRow("Match %:", self.acceptable_label)
   
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.rejected)

        pixmapi = getattr(QtWidgets.QStyle, 'SP_DirOpenIcon')
        icon = self.style().standardIcon(pixmapi)
        self.setWindowIcon(icon)

        self.setWindowTitle(f"{detector_name} result")


