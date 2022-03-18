from PyQt5 import  QtWidgets
import enum

class FilterType(enum.Enum):
    NEGATIVE = 0
    THRESHOLDING = 1
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

class Filter(QtWidgets.QWidget):
    
    def __init__(self):
        super(Filter, self).__init__()
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.L = 256  # levels of colors amount

    def setupUi(self):
        pass

    def apply(self,pixmap):
        pass

    # def clearlayout():
    #     for i in reversed(range(self.layout().count())):
    #         print(layout.itemAt(i))
    #         layout.itemAt(i).setParent(None)
    #         layout.removeItem(layout.itemAt(i))
    #         layout.itemAt(i).show()
