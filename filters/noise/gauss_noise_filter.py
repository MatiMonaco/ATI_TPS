from filters.noise.additive_noise import AdditiveNoise
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QDoubleValidator
import numpy as np


class GaussNoiseFilter(AdditiveNoise):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.mu = 50
        self.sigma = 0.5
      
        self.setupUI()

    def name(self):
        return "Gauss Noise Filter"
        
    def setupUI(self):
       
        super().setupUI()
        self.gauss_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.gauss_groupBox)
        self.gauss_groupBox.setTitle("")
        self.gauss_groupBox.setObjectName("gauss_groupBox")
        self.gauss_horizontalLayout = QtWidgets.QHBoxLayout(
            self.gauss_groupBox)
        self.gauss_horizontalLayout.setObjectName("gauss_horizontalLayout")
        self.mu_label = QtWidgets.QLabel(self.gauss_groupBox)
        self.mu_label.setStyleSheet("font-weight:bold;")
        self.mu_label.setScaledContents(False)
        self.mu_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mu_label.setObjectName("mu")
        self.gauss_horizontalLayout.addWidget(self.mu_label)
        self.mu_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.mu_line_edit.setObjectName("mu_line_edit")
        self.gauss_horizontalLayout.addWidget(self.mu_line_edit)
        spacerItem = QtWidgets.QSpacerItem(
            72, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gauss_horizontalLayout.addItem(spacerItem)
        self.sigma_label = QtWidgets.QLabel(self.groupBox)
        self.sigma_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.sigma_label.setScaledContents(False)
        self.sigma_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sigma_label.setObjectName("sigma")
        self.gauss_horizontalLayout.addWidget(self.sigma_label)
        self.sigma_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.sigma_line_edit.setObjectName("sigma_line_edit")
        self.gauss_horizontalLayout.addWidget(self.sigma_line_edit)
        self.gauss_horizontalLayout.setStretch(0, 1)
        self.gauss_horizontalLayout.setStretch(1, 3)
        self.gauss_horizontalLayout.setStretch(2, 1)
        self.gauss_horizontalLayout.setStretch(3, 1)
        self.gauss_horizontalLayout.setStretch(4, 3)


        self.mu_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&mu;</></span></pre></body></html>")
        self.sigma_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&sigma;</></span></pre></body></html>")

        self.onlyDouble = QDoubleValidator()
        self.onlyDouble.setBottom(0)
        self.mu_line_edit.setValidator(self.onlyDouble)
        self.sigma_line_edit.setValidator(self.onlyDouble)
        self.mu_line_edit.textChanged.connect(self.setMu)
        self.sigma_line_edit.textChanged.connect(self.setSigma)
        self.mu_line_edit.setText(str(self.mu))
        self.sigma_line_edit.setText(str(self.sigma))

    def setMu(self,text):
        if text != '':
            self.mu = float(text)

    def setSigma(self, text):
        if text != '':
            self.sigma = float(text)
        

    def generateNoise(self, size):
        return np.random.default_rng().normal(loc=self.mu, scale=self.sigma, size=size)
