import qimage2ndarray
from ..filter import Filter
from PyQt5 import QtWidgets,QtCore
class ThresholdingFilter(Filter):


    def __init__(self):
        super().__init__()
        self.channels_threshold = [0,0,0]
        self.setupUI()
  
        
    def setupUI(self):
        self.thresholding_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.thresholding_groupBox)
        self.thresholding_groupBox.setTitle("")
        self.thresholding_horizontalLayout = QtWidgets.QHBoxLayout(self.thresholding_groupBox)

        # self.thresholds_label = QtWidgets.QLabel(self.thresholding_groupBox)
        # self.thresholds_label.setStyleSheet("font-weight:bold;font-size:16px;")
        # self.thresholds_label.setScaledContents(False)
        # self.thresholds_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.thresholds_label.setText("Thresholds")
        # self.thresholding_horizontalLayout.addWidget( self.thresholds_label)

        line = QtWidgets.QFrame(self.thresholding_groupBox)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        line2 = QtWidgets.QFrame(self.thresholding_groupBox)
        line2.setFrameShape(QtWidgets.QFrame.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)

        

  
        self.threshold_R_label = QtWidgets.QLabel(self.thresholding_groupBox)
        self.threshold_R_label.setScaledContents(False)
        self.threshold_R_label.setAlignment(QtCore.Qt.AlignCenter)
        self.threshold_R_label.setText(f"Threshold R = {self.channels_threshold[0]}")
        self.threshold_R_label.setStyleSheet("font-weight:bold;")
        self.thresholding_horizontalLayout.addWidget( self.threshold_R_label)
        self.thresholding_horizontalLayout.addWidget(line)

        self.threshold_G_label = QtWidgets.QLabel(self.thresholding_groupBox)
        self.threshold_G_label.setScaledContents(False)
        self.threshold_G_label.setAlignment(QtCore.Qt.AlignCenter)
        self.threshold_G_label.setText(f"Threshold G = {self.channels_threshold[1]}")
        self.threshold_G_label.setStyleSheet("font-weight:bold;")
        self.thresholding_horizontalLayout.addWidget(self.threshold_G_label)
        self.thresholding_horizontalLayout.addWidget(line2)


        self.threshold_B_label = QtWidgets.QLabel(self.thresholding_groupBox)
        self.threshold_B_label.setScaledContents(False)
        self.threshold_B_label.setAlignment(QtCore.Qt.AlignCenter)
        self.threshold_B_label.setText(f"Threshold B = {self.channels_threshold[2]}")
        self.threshold_B_label.setStyleSheet("font-weight:bold;")
        self.thresholding_horizontalLayout.addWidget(self.threshold_B_label)
      
        

   
        self.thresholding_horizontalLayout.setStretch(0, 2) # R
   
        self.thresholding_horizontalLayout.setStretch(1, 0) # Line 
        self.thresholding_horizontalLayout.setStretch(2, 2) # G

        self.thresholding_horizontalLayout.setStretch(3, 0) # Line
        self.thresholding_horizontalLayout.setStretch(4, 2) # B
   
   

    def get_threshold(self, img_arr):
        pass
     

    def update_GUI(self):
        if self.channels == 1:
            self.channels_threshold[1] = self.channels_threshold[0]
            self.channels_threshold[2] = self.channels_threshold[0]
        self.threshold_R_label.setText(f"Threshold R = {self.channels_threshold[0]}")
        self.threshold_G_label.setText(f"Threshold G = {self.channels_threshold[1]}")
        self.threshold_B_label.setText(f"Threshold B = {self.channels_threshold[2]}")

    def apply(self,img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')[:,:,0:self.channels]
        height = img_arr.shape[0]
        width = img_arr.shape[1]

        
        for channel in range(self.channels):
               
            self.channels_threshold [channel] = int(self.get_threshold(img_arr[:,:,channel]))
            print(f"Threshold is {self.channels_threshold[channel]} for channel {channel}") 
            
            for x in range(height):
                for y in range(width):
                
                    if img_arr[x,y,channel] < self.channels_threshold[channel]:         
                        img_arr[x,y,channel] = 0   
                    else:  
                        img_arr[x,y,channel] = 255
        self.update_GUI()
        return img_arr

      