from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QIntValidator
from ..filter import Filter
import qimage2ndarray
from time import process_time_ns
import numpy as np


class GrayThresholdingFilter(Filter):

    def __init__(self, update_callback):
        super().__init__()

        self.update_callback = update_callback
        self.threshold = 127
       

        self.applyThreshold = np.vectorize(
            lambda x: 0 if(x < self.threshold) else self.L-1)
     
        self.setupUI()
    
    def name(self):
        return "Gray Thresholding Filter"
        
    def setupUI(self):

        self.groupBox = QtWidgets.QGroupBox()
        self.layout().addWidget(self.groupBox)
        self.groupBox.setTitle("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.threshold_label = QtWidgets.QLabel(self.groupBox)
        self.threshold_label.setText("Threshold")
        self.threshold_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.threshold_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.threshold_label)

        self.slider = QtWidgets.QSlider(self.groupBox)
        self.slider.setMaximum(255)
        self.slider.setTracking(True)
        self.slider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalLayout.addWidget(self.slider)

        self.threshold_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.threshold_line_edit.editingFinished.connect(
            lambda: self.changeSlider(self.threshold_line_edit.text()))
        self.threshold_line_edit.setValidator(QIntValidator())

        self.slider.valueChanged.connect(self.changeThresholdText)

        self.horizontalLayout.addWidget(self.threshold_line_edit)
        spacerItem1 = QtWidgets.QSpacerItem(
            69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.btn_apply.setObjectName("btn_apply")
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Update")
        self.horizontalLayout.addWidget(self.btn_apply)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.slider.setValue(self.threshold)

    def changeSlider(self, value):

        self.threshold = int(value)
        self.slider.setValue(int(value))

    def changeThresholdText(self, value):
        self.threshold = value
        self.threshold_line_edit.setText(str(value))

    def apply(self, img_arr):

        res_arr = self.applyThreshold(img_arr)
        return res_arr
