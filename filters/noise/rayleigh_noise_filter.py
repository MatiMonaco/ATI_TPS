from filters.noise.multiplicative_noise import MultiplicativeNoise
import numpy as np
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore, QtWidgets


class RayleighNoiseFilter(MultiplicativeNoise):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.epsilon = 1
        self.setupUI()

    def setupUI(self):

        super().setupUI()
        self.rayleigh_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.rayleigh_groupBox)
        self.rayleigh_groupBox.setTitle("")
        self.rayleigh_groupBox.setObjectName("rayleigh_groupBox")
        self.rayleigh_horizontalLayout = QtWidgets.QHBoxLayout(
            self.rayleigh_groupBox)
        self.rayleigh_horizontalLayout.setObjectName(
            "rayleigh_horizontalLayout")
        self.epsilon_label = QtWidgets.QLabel(self.rayleigh_groupBox)
        self.epsilon_label.setStyleSheet("font-weight:bold;")
        self.epsilon_label.setScaledContents(False)
        self.epsilon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.epsilon_label.setObjectName("epsilon")
        
        self.epsilon_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.epsilon_line_edit.setObjectName("epsilon_line_edit")
        self.rayleigh_horizontalLayout.addWidget(self.epsilon_line_edit)
        #spacerItem = QtWidgets.QSpacerItem(380, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.rayleigh_horizontalLayout.addWidget(self.epsilon_label)
    
        self.rayleigh_horizontalLayout.addWidget(self.epsilon_line_edit)
        #self.rayleigh_horizontalLayout.addItem(spacerItem)
        self.rayleigh_horizontalLayout.setStretch(0, 1)
        self.rayleigh_horizontalLayout.setStretch(1, 9)
       # self.rayleigh_horizontalLayout.setStretch(2, 5)
  

        self.epsilon_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&epsilon;</></span></pre></body></html>")
       

        self.onlyDouble = QDoubleValidator()
        self.onlyDouble.setBottom(0)
        self.epsilon_line_edit.setValidator(self.onlyDouble)
        self.epsilon_line_edit.textChanged.connect(self.setEpsilon) 
        self.epsilon_line_edit.setText(str(self.epsilon))
    

    def setEpsilon(self, text):
        if text != '':
            self.epsilon = float(text)


    def generateNoise(self, size):
        return np.random.default_rng().rayleigh(scale=self.epsilon, size=size)
