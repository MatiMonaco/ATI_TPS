from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QColor, QRgba64, QIntValidator
from ..filter import Filter
import qimage2ndarray
from time import process_time_ns
import numpy as np


class RGBThresholdingFilter(Filter):

    def __init__(self, update_callback):
        super().__init__()

        self.update_callback = update_callback
        self.R_threshold = 127
        self.G_threshold = 127
        self.B_threshold = 127
        self.updated_band = "R"
        self.applyRThreshold = np.vectorize(
            lambda x: 0 if(x < self.R_threshold) else self.L-1)
        self.applyGThreshold = np.vectorize(
            lambda x: 0 if(x < self.G_threshold) else self.L-1)
        self.applyBThreshold = np.vectorize(
            lambda x: 0 if(x < self.B_threshold) else self.L-1)
        
        self.setupUI()

    def setupUI(self):

        self.groupBox = QtWidgets.QGroupBox()
        self.layout().addWidget(self.groupBox)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)

        # R TRESHOLD LAYOUT
        self.R_horizontalLayout = QtWidgets.QHBoxLayout()
        self.R_horizontalLayout.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout.addLayout(self.R_horizontalLayout)

        self.R_threshold_label = QtWidgets.QLabel()
        self.R_threshold_label.setText("R Threshold")
        self.R_threshold_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.R_threshold_label.setAlignment(QtCore.Qt.AlignCenter)
        self.R_horizontalLayout.addWidget(self.R_threshold_label)

        self.R_slider = QtWidgets.QSlider()
        self.R_slider.setMaximum(255)
        self.R_slider.setTracking(True)
        self.R_slider.setOrientation(QtCore.Qt.Horizontal)

        self.R_horizontalLayout.addWidget(self.R_slider)

        self.R_threshold_line_edit = QtWidgets.QLineEdit()
        self.R_threshold_line_edit.setObjectName("threshold_line_edit")
        self.R_threshold_line_edit.editingFinished.connect(
            lambda: self.changeSlider("R",self.R_threshold_line_edit.text()))
        self.R_threshold_line_edit.setValidator(QIntValidator())

        self.R_slider.valueChanged.connect(
            lambda value: self.changeThresholdText("R", value))

        self.R_horizontalLayout.addWidget(self.R_threshold_line_edit)
        self.R_horizontalLayout.addItem(QtWidgets.QSpacerItem(
            69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.R_btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.R_btn_apply.clicked.connect(self.updateBandR)
        self.R_btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.R_btn_apply.setText("Update R")
        self.R_btn_apply.setObjectName("R_btn_apply")
        self.R_horizontalLayout.addWidget(self.R_btn_apply)

        self.R_horizontalLayout.setStretch(0, 1)
        self.R_horizontalLayout.setStretch(1, 3)
        self.R_horizontalLayout.setStretch(2, 1)
        self.R_horizontalLayout.setStretch(4, 1)

        self.R_slider.setValue(self.R_threshold)

        #######################################
        # G THRESHOLD LAYOUT
        self.G_horizontalLayout = QtWidgets.QHBoxLayout()
        self.G_horizontalLayout.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout.addLayout(self.G_horizontalLayout)

        self.G_threshold_label = QtWidgets.QLabel()
        self.G_threshold_label.setText("G Threshold")
        self.G_threshold_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.G_threshold_label.setAlignment(QtCore.Qt.AlignCenter)
        self.G_horizontalLayout.addWidget(self.G_threshold_label)

        self.G_slider = QtWidgets.QSlider()
        self.G_slider.setMaximum(255)
        self.G_slider.setTracking(True)
        self.G_slider.setOrientation(QtCore.Qt.Horizontal)

        self.G_horizontalLayout.addWidget(self.G_slider)

        self.G_threshold_line_edit = QtWidgets.QLineEdit()
        self.G_threshold_line_edit.setObjectName("threshold_line_edit")
        self.G_threshold_line_edit.editingFinished.connect(
            lambda: self.changeSlider("G",self.G_threshold_line_edit.text()))
        self.G_threshold_line_edit.setValidator(QIntValidator())

        self.G_slider.valueChanged.connect(
            lambda value: self.changeThresholdText("G", value))

        self.G_horizontalLayout.addWidget(self.G_threshold_line_edit)
        self.G_horizontalLayout.addItem(QtWidgets.QSpacerItem(
            69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.G_btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.G_btn_apply.clicked.connect(self.updateBandG)
        self.G_btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.G_btn_apply.setText("Update G")
        self.G_btn_apply.setObjectName("G_btn_apply")
        self.G_horizontalLayout.addWidget(self.G_btn_apply)
        self.G_horizontalLayout.setStretch(0, 1)
        self.G_horizontalLayout.setStretch(1, 3)
        self.G_horizontalLayout.setStretch(2, 1)
        self.G_horizontalLayout.setStretch(4, 1)

        self.G_slider.setValue(self.G_threshold)
        #######################################
        # B THRESHOLD LAYOUT
        self.B_horizontalLayout = QtWidgets.QHBoxLayout()
        self.B_horizontalLayout.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout.addLayout(self.B_horizontalLayout)

        self.B_threshold_label = QtWidgets.QLabel()
        self.B_threshold_label.setText("B Threshold")
        self.B_threshold_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.B_threshold_label.setAlignment(QtCore.Qt.AlignCenter)
        self.B_horizontalLayout.addWidget(self.B_threshold_label)

        self.B_slider = QtWidgets.QSlider()
        self.B_slider.setMaximum(255)
        self.B_slider.setTracking(True)
        self.B_slider.setOrientation(QtCore.Qt.Horizontal)

        self.B_horizontalLayout.addWidget(self.B_slider)

        self.B_threshold_line_edit = QtWidgets.QLineEdit()
        self.B_threshold_line_edit.setObjectName("threshold_line_edit")
        self.B_threshold_line_edit.editingFinished.connect(
            lambda: self.changeSlider("B",self.B_threshold_line_edit.text()))
        self.B_threshold_line_edit.setValidator(QIntValidator())

        self.B_slider.valueChanged.connect(lambda value: self.changeThresholdText("B",value))

        self.B_horizontalLayout.addWidget(self.B_threshold_line_edit)
        self.B_horizontalLayout.addItem(QtWidgets.QSpacerItem(
            69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.B_btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.B_btn_apply.clicked.connect(self.updateBandB)
        self.B_btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.B_btn_apply.setText("Update B")
        self.B_btn_apply.setObjectName("B_btn_apply")
        self.B_horizontalLayout.addWidget(self.B_btn_apply)
        self.B_horizontalLayout.setStretch(0, 1)
        self.B_horizontalLayout.setStretch(1, 3)
        self.B_horizontalLayout.setStretch(2, 1)
        self.B_horizontalLayout.setStretch(4, 1)
        self.B_slider.setValue(self.B_threshold)

    def updateBandR(self):
        self.updated_band = "R"
        self.G_btn_apply.setEnabled(False)
        self.B_btn_apply.setEnabled(False)
        self.update_callback()
    def updateBandG(self):
        self.updated_band = "G"
        self.B_btn_apply.setEnabled(False)
        self.R_btn_apply.setEnabled(False)
        self.update_callback()
    def updateBandB(self):
        self.updated_band = "B"
        self.G_btn_apply.setEnabled(False)
        self.R_btn_apply.setEnabled(False)
        self.update_callback()

    def changeSlider(self, band, value):

        if band == "R":
            self.R_threshold = int(value)
            self.R_slider.setValue(int(value))
        elif band == "G":
            self.G_threshold = int(value)
            self.G_slider.setValue(int(value))
        else:
            self.B_threshold = int(value)
            self.B_slider.setValue(int(value))

    def changeThresholdText(self, band, value):
        if band == "R":
            self.R_threshold = value
            self.R_threshold_line_edit.setText(str(value))
        elif band == "G":
            self.G_threshold = value
            self.G_threshold_line_edit.setText(str(value))
        else:
            self.B_threshold = value
            self.B_threshold_line_edit.setText(str(value))

    def before(self, isGrayScale):
        print("isgrayscale: ", isGrayScale)

    def apply(self, img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
        print("apply: udpate: ",self.updated_band)
        print(f"R: {self.R_threshold}, G: {self.G_threshold}, B. {self.B_threshold}")
        if self.updated_band == "R":
            img_arr[:, :, 0] = self.applyRThreshold(img_arr[:, :, 0])
            
        elif self.updated_band == "G":
            img_arr[:, :, 1] = self.applyGThreshold(img_arr[:, :, 1])
        else:
            img_arr[:, :, 2] = self.applyBThreshold(img_arr[:, :, 2])

       
        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

    def after(self):
        if self.updated_band == "R":
            self.G_btn_apply.setEnabled(True)
            self.B_btn_apply.setEnabled(True)

        elif self.updated_band == "G":
            self.B_btn_apply.setEnabled(True)
            self.R_btn_apply.setEnabled(True)
        else:
            self.G_btn_apply.setEnabled(True)
            self.R_btn_apply.setEnabled(True)
