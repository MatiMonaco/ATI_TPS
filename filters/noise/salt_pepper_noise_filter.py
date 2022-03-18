from .noise import Noise
from PyQt5.QtGui import QPixmap
import qimage2ndarray
import numpy as np
import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QDoubleValidator


class SaltPepperNoiseFilter(Noise):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.p0 = 0.1
        self.p1 = 1 - self.p0

        self.setupUI()

    def setupUI(self):

        super().setupUI()
        # self.salt_pepper_groupBox = QtWidgets.QGroupBox()
        # self.mainLayout.addWidget(self.salt_pepper_groupBox)
        # self.salt_pepper_groupBox.setTitle("")
        # self.salt_pepper_groupBox.setObjectName("gauss_groupBox")
        # self.salt_pepper_horizontalLayout = QtWidgets.QHBoxLayout(
        #     self.salt_pepper_groupBox)
        # self.salt_pepper_horizontalLayout.setObjectName(
        #     "gauss_horizontalLayout")
        # self.p0_label = QtWidgets.QLabel(self.salt_pepper_groupBox)
        # self.p0_label.setStyleSheet("font-weight:bold;")
        # self.p0_label.setScaledContents(False)
        # self.p0_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.p0_label.setObjectName("p0")
        # self.salt_pepper_horizontalLayout.addWidget(self.p0_label)
        # self.p0_line_edit = QtWidgets.QLineEdit(self.groupBox)
        # self.p0_line_edit.setObjectName("p0_line_edit")
        # self.salt_pepper_horizontalLayout.addWidget(self.p0_line_edit)
        #spacerItem = QtWidgets.QSpacerItem(72, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.salt_pepper_horizontalLayout.addItem(spacerItem)
        #self.p1_label = QtWidgets.QLabel(self.groupBox)
        # self.p1_label.setStyleSheet("font-weight:bold;font-size:16px;")
        # self.p1_label.setScaledContents(False)
        # self.p1_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.p1_label.setObjectName("p1")
        # self.salt_pepper_horizontalLayout.addWidget(self.p1_label)
       # self.p1_line_edit = QtWidgets.QLineEdit(self.groupBox)
       # self.p1_line_edit.setObjectName("p1_line_edit")
       # self.salt_pepper_horizontalLayout.addWidget(self.p1_line_edit)
        #self.salt_pepper_horizontalLayout.setStretch(0, 1)
        #self.salt_pepper_horizontalLayout.setStretch(1, 9)
        #self.salt_pepper_horizontalLayout.setStretch(2, 1)
        #self.salt_pepper_horizontalLayout.setStretch(3, 1)
       # self.salt_pepper_horizontalLayout.setStretch(4, 3)

        # self.p0_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>p<sub>0</></></span></pre></body></html>")
        # self.p1_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>p<sub>1</></></span></pre></body></html>")

        #self.onlyDouble = QDoubleValidator()
        # self.onlyDouble.setBottom(0)
        # self.p0_line_edit.setValidator(self.onlyDouble)
        # self.p1_line_edit.setValidator(self.onlyDouble)
        # self.p0_line_edit.textChanged.connect(self.setP0)
        # self.p1_line_edit.textChanged.connect(self.setP1)
        # self.p0_line_edit.setText(str(self.p0))
        # self.p1_line_edit.setText(str(self.p1))

    def setP0(self, text):
        if text != '':
            self.p0 = float(text)
            self.p1 = 1-self.p0

    def setP1(self, text):
        if text != '':
            self.p1 = float(text)

    def applyNoise(self, pixmap, density):
      
        img = pixmap.toImage()
        width = img.width()
        height = img.height()     

        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
      
        for x in range(width): 
            for y in range(height): 
                rand = np.random.uniform(0, 1)
                if rand <= self.p0:
                    img_arr[x, y] = np.array([0,0,0]) #TODO se pisa o se suma ? 
                    
                elif rand >= self.p1:
                    img_arr[x, y] = np.array([255,255,255]) 
                # else pixel does not change 
               
        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))
    

    def generateNoise(self, pixel_proportion):
        rands = np.random.uniform(0, 1, size=pixel_proportion)
        return self.saltPepearArr(rands)
