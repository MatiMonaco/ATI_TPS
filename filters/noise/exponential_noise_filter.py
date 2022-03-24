from filters.noise.multiplicative_noise import MultiplicativeNoise
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QDoubleValidator

class ExponentialNoiseFilter(MultiplicativeNoise):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.lambda_ = 8
        self.setupUI()

    def setupUI(self):
        super().setupUI()
        self.exponential_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.exponential_groupBox)
        self.exponential_groupBox.setTitle("")
        self.exponential_groupBox.setObjectName("exponential_groupBox")
        self.exponential_horizontalLayout = QtWidgets.QHBoxLayout(
            self.exponential_groupBox)
        self.exponential_horizontalLayout.setObjectName(
            "exponential_horizontalLayout")
        self.lambda_label = QtWidgets.QLabel(self.exponential_groupBox)
        self.lambda_label.setStyleSheet("font-weight:bold;")
        self.lambda_label.setScaledContents(False)
        self.lambda_label.setAlignment(QtCore.Qt.AlignCenter)
        self.lambda_label.setObjectName("epsilon")
        
        self.lamda_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.lamda_line_edit.setObjectName("epsilon_line_edit")
        self.exponential_horizontalLayout.addWidget(self.lamda_line_edit)
        #spacerItem = QtWidgets.QSpacerItem(380, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.exponential_horizontalLayout.addWidget(self.lambda_label)
    
        self.exponential_horizontalLayout.addWidget(self.lamda_line_edit)
        #self.rayleigh_horizontalLayout.addItem(spacerItem)
        self.exponential_horizontalLayout.setStretch(0, 1)
        self.exponential_horizontalLayout.setStretch(1, 9)
       # self.rayleigh_horizontalLayout.setStretch(2, 5)
  

        self.lambda_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&lambda;</></span></pre></body></html>")
       

        self.onlyDouble = QDoubleValidator()
        self.onlyDouble.setBottom(0.000001)
        self.lamda_line_edit.setValidator(self.onlyDouble)
        self.lamda_line_edit.textChanged.connect(self.setLamda)
        self.lamda_line_edit.setText(str(self.lambda_))
    

    def setLamda(self, text):
        if text != '':
            self.lambda_ = float(text)


    def generateNoise(self, size):
        return np.random.default_rng().exponential(scale=1/self.lambda_, size=size)
