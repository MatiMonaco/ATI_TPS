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
        self.update_callback = update_callback
        self.SLIDER_MAXIMUM_VALUE = 50
        self.setupUI()

    def setupUI(self):
        self.salt_pepper_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.salt_pepper_groupBox)
        self.salt_pepper_groupBox.setTitle("")
        self.salt_pepper_groupBox.setObjectName("gauss_groupBox")
        self.salt_pepper_horizontalLayout = QtWidgets.QHBoxLayout(self.salt_pepper_groupBox)
        self.salt_pepper_horizontalLayout.setObjectName("gauss_horizontalLayout")
        self.p0_label = QtWidgets.QLabel(self.salt_pepper_groupBox)
        self.p0_label.setStyleSheet("font-weight:bold;")
        self.p0_label.setScaledContents(False)
        self.p0_label.setAlignment(QtCore.Qt.AlignCenter)
        self.p0_label.setObjectName("p0")
    
        self.p0_line_edit = QtWidgets.QLineEdit(self.salt_pepper_groupBox)
        self.p0_line_edit.setObjectName("p0_line_edit")
    

        #spacerItem = QtWidgets.QSpacerItem(72, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.salt_pepper_horizontalLayout.addItem(spacerItem)
        #self.p1_label = QtWidgets.QLabel(self.groupBox)

        self.p0_slider = QtWidgets.QSlider(self.salt_pepper_groupBox)
        self.p0_slider.setMaximum(self.SLIDER_MAXIMUM_VALUE)
        self.p0_slider.setTracking(True)
        self.p0_slider.setOrientation(QtCore.Qt.Horizontal)
        self.p0_slider.setObjectName("p0_slider")
        self.p0_slider.valueChanged.connect(self.changeP0Text)
     
        self.btn_apply = QtWidgets.QPushButton(self.salt_pepper_groupBox)
        self.btn_apply.setObjectName("btn_apply")
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")

        self.salt_pepper_horizontalLayout.addWidget(self.p0_label)
        self.salt_pepper_horizontalLayout.addWidget(self.p0_slider)
        self.salt_pepper_horizontalLayout.addWidget(self.p0_line_edit)
        self.salt_pepper_horizontalLayout.addWidget(self.btn_apply)

        self.salt_pepper_horizontalLayout.setStretch(0, 1)
        self.salt_pepper_horizontalLayout.setStretch(1, 3)
        self.salt_pepper_horizontalLayout.setStretch(2, 1)
        self.salt_pepper_horizontalLayout.setStretch(4, 1)
        self.p0_label.setText("<html><head/><body><pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:130.769%;\"><span style=\" font-family:\'inherit\'; font-size:16px; color:#ffffff; background-color:transparent;\"><p>p<sub>0</></></span></pre></body></html>")
     
        self.onlyDouble = QDoubleValidator()
        self.onlyDouble.setBottom(0)
        self.onlyDouble.setTop(0.5)
        self.p0_line_edit.setValidator(self.onlyDouble)
        self.p0_line_edit.textChanged.connect(self.setP0)
        self.p0_line_edit.setText(str(self.p0))
        self.p0_line_edit.returnPressed.connect(
            lambda: self.changeP0Slider(self.p0_line_edit.text()))

        self.p0_slider.setValue(self.p0)
        self.changeP0Text(self.p0*100)
     
    def changeP0Slider(self, value):
      
        self.p0 = float(value)
        self.p0_slider.setValue(int(value)*100)

    def changeP0Text(self, value):
        fvalue = float(value)
        self.p0 = fvalue/100
        self.p0_line_edit.setText(str(fvalue/100))

    def setP0(self, text):
        if text != '':
            self.p0 = float(text)
            self.p1 = 1-self.p0

    def setP1(self, text):
        if text != '':
            self.p1 = float(text)

    def apply(self, img):
      
    
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
