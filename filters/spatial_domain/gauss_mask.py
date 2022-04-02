from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QDoubleValidator
import numpy as np
import math


class GaussMaskFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.mu = 0
        self.sigma = 4
        self.setupUi()
        
    def name(self):
        return "Gauss Mask Filter"
        
    def setupUi(self):
        self.gauss_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.gauss_groupBox)
        self.gauss_groupBox.setTitle("")
        self.gauss_groupBox.setObjectName("gauss_groupBox")
        self.gauss_horizontalLayout = QtWidgets.QHBoxLayout(
            self.gauss_groupBox)
        self.gauss_horizontalLayout.setObjectName("gauss_horizontalLayout")
        self.sigma_label = QtWidgets.QLabel(self.gauss_groupBox)
        self.sigma_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.sigma_label.setScaledContents(False)
        self.sigma_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sigma_label.setObjectName("sigma")
        self.gauss_horizontalLayout.addWidget(self.sigma_label)
        self.sigma_line_edit = QtWidgets.QLineEdit(self.gauss_groupBox)
        self.sigma_line_edit.setObjectName("sigma_line_edit")
        self.gauss_horizontalLayout.addWidget(self.sigma_line_edit)       
        self.gauss_horizontalLayout.setStretch(0, 1)
        self.gauss_horizontalLayout.setStretch(1, 3)
        self.gauss_horizontalLayout.setStretch(2, 1)
        self.gauss_horizontalLayout.setStretch(3, 1)
        self.gauss_horizontalLayout.setStretch(4, 3)
        self.btn_apply = QtWidgets.QPushButton(self.gauss_groupBox)
        self.btn_apply.setObjectName("btn_apply")
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.gauss_horizontalLayout.addWidget(self.btn_apply)
        self.gauss_horizontalLayout.setStretch(5, 1)
      
     

        self.sigma_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>&sigma;</></span></pre></body></html>")

        self.onlyDouble = QDoubleValidator()
        self.onlyDouble.setBottom(0)
        self.sigma_line_edit.setValidator(self.onlyDouble)
        self.sigma_line_edit.textChanged.connect(self.setSigma)
        self.sigma_line_edit.setText(str(self.sigma))
    
    def generate_mask(self,mask_size): 
      
        mask_size = int(2 * self.sigma)+ 1
        center = int(math.floor(mask_size/2))
        mask = []
        for i in range(mask_size):
            mask.append([])
            for j in range(mask_size):
                mask[i].append((i-center)**2 + (j-center)**2)
        return 1/(self.sigma * np.sqrt(2 * np.pi)) * np.exp( - (np.array(mask) - self.mu)**2 / (2 * self.sigma**2)), mask_size

    def setSigma(self, text):
        if text != '':
            self.sigma = float(text)
            if(self.sigma < 1):
                self.sigma = 1
            elif self.sigma > 6:
                self.sigma = 6
