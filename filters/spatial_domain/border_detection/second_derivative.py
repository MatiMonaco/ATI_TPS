
from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import numpy as np
import qimage2ndarray
from PyQt5 import QtWidgets,QtCore

from PyQt5.QtGui import QIntValidator

class SecondDerivativeFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.threshold = 0

        
    def setupUI(self):

        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 9)

        self.threshold_label = QtWidgets.QLabel(self.groupBox)
        self.threshold_label.setText("Threshold")
        self.threshold_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.threshold_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.threshold_label)

        self.slider = QtWidgets.QSlider(self.groupBox)
        self.slider.setMaximum(255)
        self.slider.setTracking(True)
        self.slider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalLayout.addWidget(self.slider)

        self.threshold_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.threshold_line_edit.editingFinished.connect(
            lambda: self.changeSlider(self.threshold_line_edit.text()))
        self.threshold_line_edit.setValidator(QIntValidator())

        self.slider.valueChanged.connect(self.changeThresholdText)

        self.horizontalLayout.addWidget(self.threshold_line_edit)
        spacerItem1 = QtWidgets.QSpacerItem(
            69, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.btn_apply = QtWidgets.QPushButton(self.groupBox)
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.horizontalLayout.addWidget(self.btn_apply)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.slider.setValue(self.threshold)

    def changeSlider(self, value):

        self.threshold = int(value)
        self.slider.setValue(int(value))

    def changeThresholdText(self, value):
        self.threshold = value
        self.threshold_line_edit.setText(str(value))
        

    def apply(self,img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')

        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)

        mask, self.mask_size = self.generate_mask(self.mask_size)
     
        result_img = self.mask_filtering(
            extended_img, mask, padding_size)
        
        result_img  = self.zero_crossing(result_img)
        
        return self.normalizeIfNeeded(result_img)

    def zero_crossing(self,second_der_arr):
        height = second_der_arr.shape[0]
        width = second_der_arr.shape[1]
        new_img = np.zeros(height, width)

        for row in range(height):
            for col in range(width - 2): # saltear el ultimo pixel que dejamos en 0 

                # if row[i] == 0  # TODO cuando estoy parada en el cero y cuando me viene una secuencia de ceros
                next_pixel = second_der_arr[row,col+1]
                if next_pixel == 0:
                    next_pixel = second_der_arr[row, col+2] # TODO index outbound 
        
                if self.sign_change(second_der_arr[row, col], next_pixel):
                    new_img[row, col] = 255
                # else already a zero
              


                # diff_1 = math.abs(row[i+1] - row[i])
                # diff_2 = math.abs(row[i+2] - row[i])
                # if diff_1 >= self.threshold:

                # if diff_2 >= self.threshold:
    
    def sign_change(self, curr_pixel, next_pixel ):

        return curr_pixel*next_pixel < 0