from re import S
from PyQt5 import  QtWidgets
import enum
from PyQt5.QtGui import QPixmap
import qimage2ndarray
import numpy as np
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
    EQUALIZATION = 12,
    BORDER_DETECTION_SOBEL = 13,
    BORDER_DETECTION_PREWITT = 14,
    BORDER_DETECTION_DIRECTIONS = 15,
    BORDER_DETECTION_LAPLACIAN = 16,
    BORDER_DETECTION_LOG = 17,
    GLOBAL_THRESHOLDING = 18,
    OTSU_THRESHOLDING = 19,
    ISOTROPIC_DIFUSSION = 20,
    ANISOTROPIC_LECLERC_DIFUSSION = 21,
    ANISOTROPIC_LORENTZ_DIFUSSION = 22,
    SPATIAL_DOMAIN_BILATERAL_MASK = 23,
    CANNY = 24,
    SUSAN = 25,
    HOUGH_TRANSFORM_LINE = 26,
    HOUGH_TRANSFORM_CIRCLE = 27
    



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
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')[:,:,0:self.channels]
        img_arr =  self.apply(img_arr)

        return QPixmap.fromImage(qimage2ndarray.array2qimage(img_arr))

    def apply(self,img):
        pass
        

    def name(self):
        pass
    
    def normalizeIfNeeded(self, arr):
        max = np.max(arr)
        min = np.min(arr)
        if(max <= 255 and min >= 0):
            return arr
        interval = max - min
        return 255 * ((arr - min) / interval)


    def truncate(self, arr):
        arr[arr < 0] = 0
        arr[arr > 255] = 255
        return arr

