from re import S
from PyQt5 import  QtWidgets
import enum
from PyQt5.QtGui import QPixmap
import qimage2ndarray
class FilterType(enum.Enum):
    NEGATIVE = 0
    RGB_THRESHOLDING = 1
    GRAY_THRESHOLDING = 13
    GAMMA_POWER = 2
    GAUSS = 3
    RAYLEIGH = 4
    EXPONENTIAL = 5
    SALTPEPPER = 6
    SPATIAL_DOMAIN_MEAN_MASK = 7
    SPATIAL_DOMAIN_MEDIAN_MASK = 8
    SPATIAL_DOMAIN_GAUSS_MASK = 9
    SPATIAL_DOMAIN_WEIGHTED_MEDIAN_MASK = 10
    SPATIAL_DOMAIN_BORDER_MASK = 11
    EQUALIZATION = 12

class Filter(QtWidgets.QWidget):
    
    def __init__(self):
        super(Filter, self).__init__()
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.L = 256  # levels of colors amount
        self.channels = 3
    def after(self):
        pass

    def setupUi(self):
        pass


    def applyFilter(self,img,isGrayScale):
        if isGrayScale:
            self.channels = 1
        else:
            self.channels = 3
        img_arr =  self.apply(img)
   
        # if isGrayScale:
        #     img_arr[:,:,1] = img_arr[:,:,0]
        #     img_arr[:, :, 2] = img_arr[:, :, 0]

     
        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

    def apply(self,img):
        pass
        

    def name(self):
        pass
    
