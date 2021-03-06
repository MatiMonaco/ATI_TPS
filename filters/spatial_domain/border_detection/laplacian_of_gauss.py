from filters.spatial_domain.border_detection.second_derivative import SecondDerivativeFilter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QDoubleValidator
import math
import numpy as np

class LaplacianOfGaussFilter(SecondDerivativeFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.sigma = 2
        self.setupUI()

    def setupUI(self):
        super().setupUI()
      
        
        self.log_horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.log_horizontalLayout)
       
        self.sigma_label = QtWidgets.QLabel(self.groupBox)
        self.sigma_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.sigma_label.setScaledContents(False)
        self.sigma_label.setAlignment(QtCore.Qt.AlignCenter)
      
        self.log_horizontalLayout.addWidget(self.sigma_label)
        self.sigma_line_edit = QtWidgets.QLineEdit(self.groupBox)

        self.log_horizontalLayout.addWidget(self.sigma_line_edit)     
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.log_horizontalLayout.addItem(spacerItem)  
        self.log_horizontalLayout.setStretch(0, 1)
        self.log_horizontalLayout.setStretch(1, 7)
        self.log_horizontalLayout.setStretch(2, 2)
       
     
        self.sigma_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&sigma;</></span></pre></body></html>")

        self.onlyDouble = QDoubleValidator()
        self.onlyDouble.setBottom(0)
        self.sigma_line_edit.setValidator(self.onlyDouble)
        self.sigma_line_edit.textChanged.connect(self.setSigma)
        self.sigma_line_edit.setText(str(self.sigma))

    def generate_mask(self,mask_size): 
      
        mask_size = int(4 * self.sigma)+ 1
        center = int(math.floor(mask_size/2))
        mask = []
        for i in range(mask_size):
            mask.append([])
            for j in range(mask_size):
                mask[i].append((i-center)**2 + (j-center)**2)
        mask = np.array(mask) # x^2 + y^2
        return (1/(self.sigma**3 * np.sqrt(2 * np.pi)) )    *    (2- (mask/self.sigma**2))    *    np.exp( - (mask) / (2 * self.sigma**2)), mask_size

    def setSigma(self, text):
        if text != '':
            self.sigma = float(text)
            if(self.sigma < 1):
                self.sigma = 1
            elif self.sigma > 6:
                self.sigma = 6

    def name(self):
        return "Laplacian of Gauss Filter"