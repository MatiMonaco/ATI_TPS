import numpy as np
import qimage2ndarray
from ..filter import Filter
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QIntValidator
class Difussion(Filter):

    def __init__(self):
        super().__init__()
       
        self.lambda_ = 0.25
        self.iterations = 10
        self.sigma = 2
      


    def setupUI(self):
    
        self.difussion_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.difussion_groupBox)
        self.difussion_groupBox.setTitle("")
   
        self.difussion_horizontalLayout = QtWidgets.QHBoxLayout(
            self.difussion_groupBox)
       
        self.it_label = QtWidgets.QLabel(self.difussion_groupBox)
        self.it_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.it_label.setScaledContents(False)
        self.it_label.setAlignment(QtCore.Qt.AlignCenter)
      
        self.difussion_horizontalLayout.addWidget(self.it_label)
        self.it_line_edit = QtWidgets.QLineEdit(self.difussion_groupBox)

        self.difussion_horizontalLayout.addWidget(self.it_line_edit)       
        self.difussion_horizontalLayout.setStretch(0, 1)
        self.difussion_horizontalLayout.setStretch(1, 8)
        
        self.it_label.setText("Iterations")

        self.onlyInt = QIntValidator()
        self.onlyInt.setBottom(0)
        self.it_line_edit.setValidator(self.onlyInt)
        self.it_line_edit.textChanged.connect(self.setIterations)
        self.it_line_edit.setText(str(self.iterations))

    def setIterations(self, text):
        if text != '':
            self.iterations = int(text)
        else:
            self.iterations = 0

    def apply(self, img):

        img_arr = qimage2ndarray.rgb_view(img).astype('int32')[:,:,0:self.channels]
        height = img_arr.shape[0]
        width = img_arr.shape[1] 

        # Iij_t+1 = Iij_t + lambda(DnCn + DsCs + DeCe + DoCo)
        for it in range(self.iterations):
            for channel in range(self.channels):
                #TODO y la condicion inicial ?? 
                for i in range(1,width-1):
                    for j in range(1,height-1):

                        curr_pixel = img_arr[i,j, channel]

                        north_deriv = img_arr[i+1,j, channel] - curr_pixel
                        south_deriv = img_arr[i-1,j, channel] - curr_pixel
                        east_deriv  = img_arr[i,j+1, channel] - curr_pixel
                        west_deriv  = img_arr[i,j-1, channel] - curr_pixel

                        img_arr[i,j, channel]+= self.lambda_ * (north_deriv * self.get_kernel(north_deriv, self.sigma) +
                                                                south_deriv * self.get_kernel(south_deriv, self.sigma) +
                                                                east_deriv  * self.get_kernel(east_deriv,  self.sigma) +
                                                                west_deriv  * self.get_kernel(west_deriv,  self.sigma))
        # TODO norm            
        return img_arr


    def get_kernel(self,deriv, sigma):

        pass







