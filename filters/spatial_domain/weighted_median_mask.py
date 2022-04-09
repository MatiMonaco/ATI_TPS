
from filters.spatial_domain.spatial_domain_2 import SpatialDomainFilter
import numpy as np
import statistics
from PyQt5 import QtWidgets
from filters.spatial_domain.spatial_domain_matrix_dialog import SpatialDomainMatrixInputDialog


class WeightedMedianMaskFilter(SpatialDomainFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        self.mask = np.ones(
            (self.mask_size,  self.mask_size), dtype='int32')
      
        self.setupUI()

    def name(self):
        return "Weighted Median Mask Filter"
        
    def maskSizeChanged(self):
        self.mask = np.ones((self.mask_size,  self.mask_size), dtype='int32')


    def setupUI(self):
        super().setupUI()
       
        self.btn_change_weights = QtWidgets.QPushButton(self.spatial_domain_groupBox)
        self.btn_change_weights.setObjectName("btn_change_weights")
        self.btn_change_weights.clicked.connect(self.openDialog)
        self.btn_change_weights.setStyleSheet("font-weight: bold;color:white;")
        self.btn_change_weights.setText("Set Weights")
        self.spatial_domain_horizontalLayout.insertWidget(
            2, self.btn_change_weights)

    def openDialog(self):
        dialog = SpatialDomainMatrixInputDialog(self.mask, self.mask_size)
        code = dialog.exec()
      
        if code == 1:

            self.mask = dialog.getMaskWeights()
    

    def generate_mask(self,mask_size): 

        return self.mask, mask_size

    def apply_mask(self, sub_img, mask): 
                
        pixels_by_channel = []     
     
        for channel in range(0,self.channels):
            sub_img_by_channel = sub_img[:, :, channel]
            sub_img_arr = sub_img_by_channel.flatten()
            mask_arr = mask.flatten()
          
            sub_img_arr = np.repeat(sub_img_arr,mask_arr)
         
            median = statistics.median(sub_img_arr)
         
            pixels_by_channel.append(median) 
         
    
        return pixels_by_channel
        