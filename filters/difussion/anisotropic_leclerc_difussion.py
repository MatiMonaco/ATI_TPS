import numpy as np
from filters.difussion.difussion import Difussion
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QDoubleValidator


class AnisotropicLeclercFilter(Difussion):

    def __init__(self):
        super().__init__()
       

    def setupUI(self):
        super().setupUI()
        
        self.anisotropic_horizontalLayout = QtWidgets.QHBoxLayout(
            self.difussion_groupBox)
        self.diffusion_verticalLayout.addWidget(self.difussion_groupBox)
        self.sigma_label = QtWidgets.QLabel(self.anisotropic_horizontalLayout)
        self.sigma_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.sigma_label.setScaledContents(False)
        self.sigma_label.setAlignment(QtCore.Qt.AlignCenter)
      
        self.anisotropic_horizontalLayout.addWidget(self.sigma_label)
        self.sigma_line_edit = QtWidgets.QLineEdit(self.difussion_groupBox)

        self.anisotropic_horizontalLayout.addWidget(self.sigma_line_edit)       
        self.anisotropic_horizontalLayout.setStretch(0, 1)
        self.anisotropic_horizontalLayout.setStretch(1, 8)
       
        self.sigma_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&sigma;</></span></pre></body></html>")

        self.onlyDouble = QDoubleValidator()
        self.onlyDouble.setBottom(0)
        self.sigma_line_edit.setValidator(self.onlyDouble)
        self.sigma_line_edit.textChanged.connect(self.setSigma)
        self.sigma_line_edit.setText(str(self.sigma))

    
    def setSigma(self, text):
        if text != '':
            self.sigma = float(text)
        else:
            self.sigma = 0
    def get_kernel(self, deriv, sigma):
      
        # Leclerc Detector 
        return np.exp(-deriv**2 / sigma**2)

    def name(self):
        return "Anisotropic Leclerc Filter"