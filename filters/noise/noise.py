from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIntValidator
from ..filter import Filter
import numpy as np


class Noise(Filter):

    def __init__(self, update_callback):
        super().__init__()

        self.update_callback = update_callback
        self.density = 0.05
        # multiplicado por 100 porque despues divido por 100 para tener doubles value
        self.SLIDER_MAXIMUM_VALUE = 100
      

    def setupUI(self):
       
        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.density_label = QtWidgets.QLabel(self.groupBox)
        self.density_label.setText("Noise density")
        self.density_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.density_label.setAlignment(QtCore.Qt.AlignCenter)
        self.density_label.setObjectName("density_label")
        self.horizontalLayout.addWidget(self.density_label)

        self.slider = QtWidgets.QSlider(self.groupBox)
        self.slider.setMaximum(self.SLIDER_MAXIMUM_VALUE)
        self.slider.setTracking(True)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")

        self.horizontalLayout.addWidget(self.slider)

        self.density_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.density_line_edit.setObjectName("density_line_edit")
        self.density_line_edit.returnPressed.connect(
            lambda: self.changeDensitySlider(self.density_line_edit.text()))
        self.density_line_edit.setValidator(QIntValidator())

        self.slider.valueChanged.connect(self.changeDensityText)

        self.horizontalLayout.addWidget(self.density_line_edit)
        spacerItem1 = QtWidgets.QSpacerItem(
            69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.btn_apply.setObjectName("btn_apply")
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.horizontalLayout.addWidget(self.btn_apply)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.slider.setValue(self.density)
        self.changeDensityText(self.density*100)

    def changeDensitySlider(self, value):
        print(f"CHANGE SLIDER: {value}")
        self.density = float(value)
        self.slider.setValue(int(value)*100)

    def changeDensityText(self, value):
        fvalue = float(value)
        self.density = fvalue/100
        self.density_line_edit.setText(str(fvalue/100))

    def apply(self, img):

        pass

 

    def generateRandomCoords(self, w, h, quantity):

        random_arr = np.random.default_rng().choice(
            w*h, size=quantity, replace=False)
        x = np.floor_divide(random_arr, w)
        y = random_arr - x*w
        return x, y