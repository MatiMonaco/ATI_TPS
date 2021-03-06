
from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import numpy as np
import qimage2ndarray
from PyQt5 import QtWidgets,QtCore

from PyQt5.QtGui import QIntValidator

class SecondDerivativeFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.threshold = 5
       
        
    def setupUI(self):
        
        self.groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.groupBox)
        self.groupBox.setTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
     
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout( self.horizontalLayout)
        #self.horizontalLayout.setContentsMargins(-1, -1, -1, 9)

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
        self.horizontalLayout.setStretch(1, 6)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(4, 2)

        self.slider.setValue(self.threshold)
        self.threshold_line_edit.setText(str(self.threshold))

    def changeSlider(self, value):

        self.threshold = int(value)
        self.slider.setValue(int(value))

    def changeThresholdText(self, value):
        self.threshold = value
        self.threshold_line_edit.setText(str(value))
        

    def apply(self,img_arr):
      
     

        mask, self.mask_size = self.generate_mask(self.mask_size)
        extended_img, padding_size = self.complete_image(img_arr, self.mask_size)
     
        result_img = self.mask_filtering(
            extended_img, mask, padding_size, norm=False)
        # print(result_img)
        result_img  = self.zero_crossing(result_img)
        
        return self.normalizeIfNeeded(result_img)

    #### CASOS A TENER EN CUENTA:
    ## -a b --> OK
    ## a -b --> OK
    ## a b --> OK
    ## -a 0 b --> OK
    ## a 0 -b --> OK
    ## a 0 b --> OK (queda en 0)
    ## 0 b --> OK (queda en 0)
    ## a 0 0 ... --> OK (queda en 0)
    ## a 0 ] --> OK (queda en 0)
    ## por ahora todos los FALTA dejan 0
     
    def zero_crossing(self,second_der_arr):
        height = second_der_arr.shape[0]
        width = second_der_arr.shape[1]
        new_img_by_row = np.zeros((height, width, self.channels), dtype=int)
        new_img_by_col = np.zeros((height, width, self.channels), dtype=int)

        for channel in range(self.channels):

            ## For each row 
            for row in range(height):
                for col in range(width - 1): # 0 - 510 (anteultima) # saltear el ultimo pixel que dejamos en 0 

                    if second_der_arr[row, col, channel] == 0:  
                        continue

                    next_pixel = second_der_arr[row,col+1, channel]
                    if next_pixel == 0 and col < width - 2: # 512-2 = 510 
                        next_pixel = second_der_arr[row, col+2, channel] # TODO index outbound, TODO del TODO que hacemos con el 0 
            
                    if self.sign_change_with_threshold(second_der_arr[row, col, channel], next_pixel):
                        new_img_by_row[row, col, channel] = 255
                    # else already a zero

            ## Same for each col
            for col in range(width):
                for row in range(height-1): # 0 - 510 (anteultima) # saltear el ultimo pixel que dejamos en 0 

                    if second_der_arr[row, col, channel] == 0:  
                        continue

                    next_pixel = second_der_arr[row+1,col, channel]
                    if next_pixel == 0 and row < height - 2: # 512-2 = 510 
                        next_pixel = second_der_arr[row+2, col, channel] # TODO index outbound, TODO del TODO que hacemos con el 0 
            
                    if self.sign_change_with_threshold(second_der_arr[row, col, channel], next_pixel):
                        new_img_by_col[row, col, channel] = 255
                    # else already a zero
        # new_img = np.zeros((height, width, self.channels))
        
        return new_img_by_row | new_img_by_col
        
    def sign_change_with_threshold(self, curr_pixel, next_pixel):
        if curr_pixel*next_pixel < 0:
            return abs(curr_pixel) + abs(next_pixel) >= self.threshold
        return False