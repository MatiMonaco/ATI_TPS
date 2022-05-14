from dis import dis
import numpy as np
import matplotlib.pyplot as plt
from filters.filter import Filter
from PyQt5 import QtWidgets, QtCore

from filters.advanced_edge_detection.canny import Canny
from PyQt5.QtGui import QDoubleValidator


class CannyRGB(Canny):

    def __init__(self, update_callback):
        super().__init__(update_callback,False)
        self.setupUI()


    ###########################################################################################
    
    def setT1_r(self, text):
        if text != '':
            self.t1[0] = int(text)
            print("T1 R changed to ", self.t1)

    def setT2_r(self, text):
        if text != '':
            self.t2[0] = int(text)
            print("T2 R changed to ", self.t2)

    def setT1_g(self, text):
        if text != '':
            self.t1[1] = int(text)
            print("T1 G changed to ", self.t1)

    def setT2_g(self, text):
        if text != '':
            self.t2[1] = int(text)
            print("T2 G changed to ", self.t2)
    
    def setT1_b(self, text):
        if text != '':
            self.t1[2] = int(text)
            print("T1 B changed to ", self.t1)

    def setT2_b(self, text):
        if text != '':
            self.t2[2] = int(text)
            print("T2 B changed to ", self.t2)
    
    def setupUI(self):

        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gradient_filter_label = QtWidgets.QLabel(self.groupBox)
        self.gradient_filter_label.setText(
            "<html><head/><body><span><p>&Delta;I algorithm</></span></body></html>")
        self.gradient_filter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gradient_filter_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.horizontalLayout.addWidget(self.gradient_filter_label)

        self.alg_cb = QtWidgets.QComboBox()
        self.alg_cb.addItems(["Sobel", "Prewitt"])
        self.alg_cb.currentIndexChanged.connect(self.algorithmChange)
        self.horizontalLayout.addWidget(self.alg_cb)

        line = QtWidgets.QFrame(self.groupBox)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line)

        self.conection_cb = QtWidgets.QComboBox()
        self.conection_cb.addItems(["4-connected", "8-connected"])
        self.conection_cb.currentIndexChanged.connect(self.connectionChange)
        self.horizontalLayout.addWidget(self.conection_cb)

        line2 = QtWidgets.QFrame(self.groupBox)
        line2.setFrameShape(QtWidgets.QFrame.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout.addWidget(line2)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)

        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.horizontalLayout.addWidget(self.btn_apply)

        ###################### R ###################
        self.R_horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.R_horizontalLayout)

       

        onlyDouble = QDoubleValidator()
        onlyDouble.setBottom(0)

        self.R_t1_label = QtWidgets.QLabel(self.groupBox)
        self.R_t1_label.setText("t1")
        self.R_t1_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.R_t1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.R_horizontalLayout.addWidget(self.R_t1_label)

        self.R_t1_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.R_t1_line_edit.setStyleSheet("font-weight:bold;")
        self.R_t1_line_edit.setValidator(onlyDouble)
        self.R_horizontalLayout.addWidget(self.R_t1_line_edit)

        self.R_t2_label = QtWidgets.QLabel(self.groupBox)
        self.R_t2_label.setText("t2")
        self.R_t2_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.R_t2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.R_horizontalLayout.addWidget(self.R_t2_label)

        self.R_t2_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.R_t2_line_edit.setStyleSheet("font-weight:bold;")
        self.R_t2_line_edit.setValidator(onlyDouble)
        self.R_horizontalLayout.addWidget(self.R_t2_line_edit)

        line2 = QtWidgets.QFrame(self.groupBox)
        line2.setFrameShape(QtWidgets.QFrame.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.R_horizontalLayout.addWidget(line2)
     

        self.R_t1_line_edit.textChanged.connect(self.setT1_r)
        self.R_t2_line_edit.textChanged.connect(self.setT2_r)

        #################### G #######################
        self.G_horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.G_horizontalLayout)

        onlyDouble = QDoubleValidator()
        onlyDouble.setBottom(0)

        self.G_t1_label = QtWidgets.QLabel(self.groupBox)
        self.G_t1_label.setText("t1")
        self.G_t1_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.G_t1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.G_horizontalLayout.addWidget(self.G_t1_label)

        self.G_t1_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.G_t1_line_edit.setStyleSheet("font-weight:bold;")
        self.G_t1_line_edit.setValidator(onlyDouble)
        self.G_horizontalLayout.addWidget(self.G_t1_line_edit)

        self.G_t2_label = QtWidgets.QLabel(self.groupBox)
        self.G_t2_label.setText("t2")
        self.G_t2_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.G_t2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.G_horizontalLayout.addWidget(self.G_t2_label)

        self.G_t2_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.G_t2_line_edit.setStyleSheet("font-weight:bold;")
        self.G_t2_line_edit.setValidator(onlyDouble)
        self.G_horizontalLayout.addWidget(self.G_t2_line_edit)

        line2 = QtWidgets.QFrame(self.groupBox)
        line2.setFrameShape(QtWidgets.QFrame.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.G_horizontalLayout.addWidget(line2)

        self.G_t1_line_edit.textChanged.connect(self.setT1_g)
        self.G_t2_line_edit.textChanged.connect(self.setT2_g)

        ################## B ##################
        self.B_horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.B_horizontalLayout)

        onlyDouble = QDoubleValidator()
        onlyDouble.setBottom(0)

        self.B_t1_label = QtWidgets.QLabel(self.groupBox)
        self.B_t1_label.setText("t1")
        self.B_t1_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.B_t1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.B_horizontalLayout.addWidget(self.B_t1_label)

        self.B_t1_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.B_t1_line_edit.setStyleSheet("font-weight:bold;")
        self.B_t1_line_edit.setValidator(onlyDouble)
        self.B_horizontalLayout.addWidget(self.B_t1_line_edit)

        self.B_t2_label = QtWidgets.QLabel(self.groupBox)
        self.B_t2_label.setText("t2")
        self.B_t2_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.B_t2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.B_horizontalLayout.addWidget(self.B_t2_label)

        self.B_t2_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.B_t2_line_edit.setStyleSheet("font-weight:bold;")
        self.B_t2_line_edit.setValidator(onlyDouble)
        self.B_horizontalLayout.addWidget(self.B_t2_line_edit)

        line2 = QtWidgets.QFrame(self.groupBox)
        line2.setFrameShape(QtWidgets.QFrame.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.B_horizontalLayout.addWidget(line2)

        self.B_t1_line_edit.textChanged.connect(self.setT1_b)
        self.B_t2_line_edit.textChanged.connect(self.setT2_b)

        self.R_t1_line_edit.setText(str(self.t1[0]))
        self.R_t2_line_edit.setText(str(self.t2[0]))
        self.G_t1_line_edit.setText(str(self.t1[1]))
        self.G_t2_line_edit.setText(str(self.t2[1]))
        self.B_t1_line_edit.setText(str(self.t1[2]))
        self.B_t2_line_edit.setText(str(self.t2[2]))