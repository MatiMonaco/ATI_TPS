import qimage2ndarray
from ..filter import Filter
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QIntValidator
class Difussion(Filter):

    def __init__(self,update_callback):
        super().__init__()
        self.update_callback = update_callback
        self.lambda_ = 0.25
        self.iterations = 20
        self.sigma = 4
      
    def setupUI(self):
    
        self.difussion_groupBox = QtWidgets.QGroupBox()
        self.mainLayout.addWidget(self.difussion_groupBox)
        self.difussion_groupBox.setTitle("")
        self.difussion_verticalLayout = QtWidgets.QVBoxLayout(
            self.difussion_groupBox)    
        self.difussion_horizontalLayout = QtWidgets.QHBoxLayout()
        self.difussion_verticalLayout.addLayout(self.difussion_horizontalLayout)
       
        self.it_label = QtWidgets.QLabel(self.difussion_groupBox)
        self.it_label.setStyleSheet("font-weight:bold;font-size:16px;")
        self.it_label.setScaledContents(False)
        self.it_label.setAlignment(QtCore.Qt.AlignCenter)
      
        self.difussion_horizontalLayout.addWidget(self.it_label)
        self.it_line_edit = QtWidgets.QLineEdit(self.difussion_groupBox)

        self.difussion_horizontalLayout.addWidget(self.it_line_edit)       
  
        
        self.it_label.setText("Iterations")

        self.onlyInt = QIntValidator()
        self.onlyInt.setBottom(0)
        self.it_line_edit.setValidator(self.onlyInt)
        self.it_line_edit.textChanged.connect(self.setIterations)
        self.it_line_edit.setText(str(self.iterations))

        self.btn_apply = QtWidgets.QPushButton(self.difussion_groupBox)
        self.btn_apply.clicked.connect(self.update_callback)
        self.btn_apply.setStyleSheet("font-weight: bold;color:white;")
        self.btn_apply.setText("Apply")
        self.difussion_horizontalLayout.addWidget(self.btn_apply)
        self.difussion_horizontalLayout.setStretch(0, 1)
        self.difussion_horizontalLayout.setStretch(1, 8)
        self.difussion_horizontalLayout.setStretch(2,1)

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
                for i in range(height):
                    for j in range(width):

                        curr_pixel = img_arr[i,j, channel]

                        east_deriv  = (img_arr[i+1,j, channel] - curr_pixel) if i != height-1    else (img_arr[0,j, channel]-curr_pixel)
                        west_deriv  = (img_arr[i-1,j, channel] - curr_pixel) if i != 0          else (img_arr[height-1,j, channel]-curr_pixel)   
                        north_deriv = (img_arr[i,j+1, channel] - curr_pixel) if j != width-1   else (img_arr[i,0, channel]-curr_pixel)   
                        south_deriv = (img_arr[i,j-1, channel] - curr_pixel) if j != 0          else (img_arr[i,width-1, channel]-curr_pixel)

                        img_arr[i,j, channel]+= self.lambda_ * (north_deriv * self.get_kernel(north_deriv, self.sigma) +
                                                                south_deriv * self.get_kernel(south_deriv, self.sigma) +
                                                                east_deriv  * self.get_kernel(east_deriv,  self.sigma) +
                                                                west_deriv  * self.get_kernel(west_deriv,  self.sigma))
        # TODO norm            
        return self.normalizeIfNeeded(img_arr)


    def get_kernel(self,deriv, sigma):

        pass







