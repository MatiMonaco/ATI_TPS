from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets,QtCore,QtGui
import sys
from filters.filter import FilterType
from components.tabs.filter_tab import FilterTab
from components.tabs.operations_tab import OperationsTab
orig_windows = set()
filt_windows = set()



class ATIGUI(QMainWindow):
    def __init__(self):
        super(ATIGUI, self).__init__()
        self.setupUI()
        self.setupActions()
        self.setWindowTitle('ATI GUI')
       

    def setupActions(self):
        ### TAB 1 ###
        self.btn_open.triggered.connect(self.filters_tab.loadImageTab1)
        self.btn_save.triggered.connect(self.filters_tab.saveTab1)

        self.btn_modify_pixel.triggered.connect(self.filters_tab.modifyPixel)

        # Point Operators
        self.btn_thresholding_filter.triggered.connect(
            lambda: self.filters_tab.changeFilter(FilterType.GRAY_THRESHOLDING if self.filters_tab.isGrayscale else FilterType.RGB_THRESHOLDING))
        self.btn_negative_filter.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.NEGATIVE, True)})
        self.btn_gamma_filter.triggered.connect(
            lambda: self.filters_tab.changeFilter(FilterType.GAMMA_POWER))

        # Noises
        self.btn_rayleigh_noise.triggered.connect(
            lambda:  self.filters_tab.changeFilter(FilterType.RAYLEIGH))
        self.btn_exponential_noise.triggered.connect(
            lambda: self.filters_tab.changeFilter(FilterType.EXPONENTIAL))
        self.btn_gauss_noise.triggered.connect(
            lambda: self.filters_tab.changeFilter(FilterType.GAUSS))
        self.btn_salt_pepper_noise.triggered.connect(
            lambda: self.filters_tab.changeFilter(FilterType.SALTPEPPER))

        # Spatial Domain Masks
        self.btn_mean_mask.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.SPATIAL_DOMAIN_MEAN_MASK)})
        self.btn_median_mask.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.SPATIAL_DOMAIN_MEDIAN_MASK)})
        self.btn_weighted_median_mask.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.SPATIAL_DOMAIN_WEIGHTED_MEDIAN_MASK)})
        self.btn_border_mask.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.SPATIAL_DOMAIN_BORDER_MASK)})
        self.btn_gauss_mask.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.SPATIAL_DOMAIN_GAUSS_MASK)})
        self.btn_bilateral_mask.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.SPATIAL_DOMAIN_BILATERAL_MASK, True)})

        # Equalization
        self.btn_equalization.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.EQUALIZATION, True)})

        # Border Detection
        self.btn_border_prewitt.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.BORDER_DETECTION_PREWITT, True)})
      
        self.btn_border_sobel.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.BORDER_DETECTION_SOBEL,True)})
    
        self.btn_border_directions.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.BORDER_DETECTION_DIRECTIONS, True)})
   
        self.btn_border_laplacian.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.BORDER_DETECTION_LAPLACIAN)})
   
        self.btn_border_laplacian_gauss.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.BORDER_DETECTION_LOG)})

        # Thresholding
        self.btn_threshold_global.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.GLOBAL_THRESHOLDING,True)})

        # Diffusion 
        self.btn_isotropic_difussion.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.ISOTROPIC_DIFUSSION,True)})
        
        self.btn_anisotropic_lorentz_difussion.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.ANISOTROPIC_LORENTZ_DIFUSSION,True)})

        self.btn_anisotropic_leclerc_difussion.triggered.connect(
            lambda: {self.filters_tab.changeFilter(FilterType.ANISOTROPIC_LECLERC_DIFUSSION,True)})
            

    def setupTabs(self):
        self.filters_tab = FilterTab()
        self.operations_tab = OperationsTab()

        self.tabWidget.addTab(self.filters_tab, "Filters")
        self.tabWidget.addTab(self.operations_tab, "Operations")

  
    def setupUI(self):

        ################## Layout ##################
        self.setObjectName("MainWindow")
        self.resize(980, 821)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setAutoFillBackground(True)
        self.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(980, 780))
        self.centralwidget.setMaximumSize(QtCore.QSize(640, 480))
        self.centralwidget.setStyleSheet("background-color: rgb(40, 44, 52); \n"
                                         " ")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_10.setSizeConstraint(
            QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("color:rgb(255, 255, 255)")
        self.tabWidget.setObjectName("tabWidget")

        ################## Menu Bar ##################

        self.verticalLayout_10.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 980, 21))
        self.menubar.setStyleSheet("color:rgb(255, 255, 255);background-color: rgb(24, 24,24); \n"
                                   " ")
        self.menubar.setObjectName("menubar")

        ################## Image ##################        
        self.menu_image = QtWidgets.QMenu(self.menubar)
        self.menu_image.setStyleSheet("color:rgb(255, 255, 255);")
        self.menu_image.setObjectName("menu_image")
        self.menu_image.setTitle("Image")

        ################## Pixel ##################

        self.menu_pixel = QtWidgets.QMenu(self.menubar)
        self.menu_pixel.setStyleSheet("color:rgb(255, 255, 255);")
        self.menu_pixel.setObjectName("menu_pixel")
        self.menu_pixel.setTitle("Pixel")

        ################## Filter ##################

        self.menu_filter = QtWidgets.QMenu(self.menubar)
        self.menu_filter.setObjectName("menu_filter")
        self.menu_filter.setTitle("Filter")

        ################## Filter Menu ##################
        self.btn_point_Operators = QtWidgets.QMenu(self.menu_filter)
        self.btn_point_Operators.setObjectName("btn_point_Operators")
        self.btn_point_Operators.setTitle("Point Operators")

        self.menuNoise = QtWidgets.QMenu(self.menu_filter)
        self.menuNoise.setObjectName("menuNoise")
        self.menuNoise.setTitle("Noise")
    
        self.menuSpatial_Domain = QtWidgets.QMenu(self.menu_filter)
        self.menuSpatial_Domain.setObjectName("menuSpatial_Domain")
        self.menuSpatial_Domain.setTitle("Spatial Domain")
        self.setMenuBar(self.menubar)

        self.menuBorder_Detection = QtWidgets.QMenu(self.menu_filter)
        self.menuBorder_Detection.setObjectName("menuBorder_Detection")
        self.menuBorder_Detection.setTitle("Border Detection")
        self.setMenuBar(self.menubar)

        self.menu_thresholding = QtWidgets.QMenu(self.menu_filter)
        self.menu_thresholding.setObjectName("menu_thresholding")
        self.menu_thresholding.setTitle("Thresholding")
        self.setMenuBar(self.menubar)

        self.menu_difussion = QtWidgets.QMenu(self.menu_filter)
        self.menu_difussion.setObjectName("menu_difussion")
        self.menu_difussion.setTitle("Difussion")
        self.setMenuBar(self.menubar)

        ################## Image Menu ##################

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.btn_open = QtWidgets.QAction(self)
        self.btn_open.setObjectName("btn_open")
        self.btn_open.setText("Open")
        self.btn_save = QtWidgets.QAction(self)
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setText("Save")

        ################## Pixel Menu ##################

        self.btn_show_pixel_value = QtWidgets.QAction(self)
        self.btn_show_pixel_value.setObjectName("btn_show_pixel_value")
        self.btn_show_pixel_value.setText("Show pixel value")
        self.btn_modify_pixel = QtWidgets.QAction(self)
        self.btn_modify_pixel.setObjectName("btn_modify_pixel")
        self.btn_modify_pixel.setText("Modify pixel")          
        self.btn_show_pixel_value = QtWidgets.QAction(self)
        self.btn_show_pixel_value.setObjectName("btn_show_pixel_value")
        self.btn_show_pixel_value.setText("Show pixel value")

        ################## Point Operators Menu ##################

        self.btn_gamma_filter = QtWidgets.QAction(self)
        self.btn_gamma_filter.setObjectName("btn_gamma_filter")
        self.btn_gamma_filter.setText("Gamma")
        self.btn_thresholding_filter = QtWidgets.QAction(self)
        self.btn_thresholding_filter.setObjectName("btn_thresholding_filter")
        self.btn_thresholding_filter.setText("Thresholding")
        self.btn_negative_filter = QtWidgets.QAction(self)
        self.btn_negative_filter.setObjectName("btn_negative_filter")
        self.btn_negative_filter.setText("Negative")

        ################## Noise Menu ##################

        self.btn_gauss_noise = QtWidgets.QAction(self)
        self.btn_gauss_noise.setObjectName("btn_gauss_noise")
        self.btn_gauss_noise.setText("Gauss")
        self.btn_rayleigh_noise = QtWidgets.QAction(self)
        self.btn_rayleigh_noise.setObjectName("btn_rayleigh_noise")
        self.btn_rayleigh_noise.setText("Rayleigh")
        self.btn_exponential_noise = QtWidgets.QAction(self)
        self.btn_exponential_noise.setObjectName("btn_exponential_noise")
        self.btn_exponential_noise.setText("Exponential")
        self.btn_salt_pepper_noise = QtWidgets.QAction(self)
        self.btn_salt_pepper_noise.setObjectName("btn_salt_pepper_noise")
        self.btn_salt_pepper_noise.setText("Salt and pepper")

        ################## Spatial Domain Menu ##################
        self.btn_mean_mask = QtWidgets.QAction(self)
        self.btn_mean_mask.setObjectName("btn_mean_mask")
        self.btn_mean_mask.setText("Mean mask")
        self.btn_gauss_mask = QtWidgets.QAction(self)
        self.btn_gauss_mask.setObjectName("btn_gauss_mask")
        self.btn_gauss_mask.setText("Gauss Mask")
        self.btn_median_mask = QtWidgets.QAction(self)
        self.btn_median_mask.setObjectName("btn_median_mask")
        self.btn_median_mask.setText("Median Mask")
        self.btn_weighted_median_mask = QtWidgets.QAction(self)
        self.btn_weighted_median_mask.setObjectName("btn_weighted_median_mask")
        self.btn_weighted_median_mask.setText("Weighted Median Mask")
        self.btn_border_mask = QtWidgets.QAction(self)
        self.btn_border_mask.setObjectName("btn_border_mask")
        self.btn_border_mask.setText("High Pass")
        self.btn_bilateral_mask = QtWidgets.QAction(self)
        self.btn_bilateral_mask.setObjectName("btn_bilateral_mask")
        self.btn_bilateral_mask.setText("Bilateral Mask")

        ################## Equalization ##################
        self.btn_equalization = QtWidgets.QAction(self)
        self.btn_equalization.setObjectName("btn_equalization")
        self.btn_equalization.setText("Equalization")

        ################## Border Detection Menu ##################
        self.btn_border_prewitt = QtWidgets.QAction(self)
        self.btn_border_prewitt.setObjectName("btn_border_prewitt")
        self.btn_border_prewitt.setText("Prewitt")

        self.btn_border_sobel = QtWidgets.QAction(self)
        self.btn_border_sobel.setObjectName("btn_border_sobel")
        self.btn_border_sobel.setText("Sobel")

        self.btn_border_directions = QtWidgets.QAction(self)
        self.btn_border_directions.setObjectName("btn_border_directions")
        self.btn_border_directions.setText("Directions")

        self.btn_border_laplacian = QtWidgets.QAction(self)
        self.btn_border_laplacian.setObjectName("btn_border_laplacian")
        self.btn_border_laplacian.setText("Laplacian")

        self.btn_border_laplacian_gauss = QtWidgets.QAction(self)
        self.btn_border_laplacian_gauss.setObjectName("btn_border_laplacian_gauss")
        self.btn_border_laplacian_gauss.setText("Laplacian of Gauss")

        ################## Thresholding Menu ##################
        self.btn_threshold_global = QtWidgets.QAction(self)
        self.btn_threshold_global.setObjectName("btn_threshold_global")
        self.btn_threshold_global.setText("Global")

        self.btn_threshold_otsu = QtWidgets.QAction(self)
        self.btn_threshold_otsu.setObjectName("btn_threshold_otsu")
        self.btn_threshold_otsu.setText("Otsu")

        ################## Difussion Menu ##################
        self.btn_isotropic_difussion = QtWidgets.QAction(self)
        self.btn_isotropic_difussion.setObjectName("btn_isotropic_difussion")
        self.btn_isotropic_difussion.setText("Isotropic")

        self.btn_anisotropic_lorentz_difussion = QtWidgets.QAction(self)
        self.btn_anisotropic_lorentz_difussion.setObjectName("btn_anisotropic_lorentz_difussion")
        self.btn_anisotropic_lorentz_difussion.setText("Anisotropic Lorentz")

        self.btn_anisotropic_leclerc_difussion = QtWidgets.QAction(self)
        self.btn_anisotropic_leclerc_difussion.setObjectName("btn_anisotropic_leclerc_difussion")
        self.btn_anisotropic_leclerc_difussion.setText("Anisotropic Leclerc")

        ################## Set Btn Actions ##################
        self.menu_image.addAction(self.btn_open)
        self.menu_image.addAction(self.btn_save)
        self.menu_pixel.addAction(self.btn_modify_pixel)

        self.btn_point_Operators.addAction(self.btn_gamma_filter)
        self.btn_point_Operators.addAction(self.btn_thresholding_filter)
        self.btn_point_Operators.addAction(self.btn_negative_filter)

        self.menuNoise.addAction(self.btn_gauss_noise)
        self.menuNoise.addAction(self.btn_rayleigh_noise)
        self.menuNoise.addAction(self.btn_exponential_noise)
        self.menuNoise.addAction(self.btn_salt_pepper_noise)

        self.menuSpatial_Domain.addAction(self.btn_mean_mask)
        self.menuSpatial_Domain.addAction(self.btn_gauss_mask)
        self.menuSpatial_Domain.addAction(self.btn_median_mask)
        self.menuSpatial_Domain.addAction(self.btn_weighted_median_mask)
        self.menuSpatial_Domain.addAction(self.btn_border_mask)
        self.menuSpatial_Domain.addAction(self.btn_bilateral_mask)

        self.menuBorder_Detection.addAction(self.btn_border_prewitt)
        self.menuBorder_Detection.addAction(self.btn_border_sobel)
        self.menuBorder_Detection.addAction(self.btn_border_directions)
        self.menuBorder_Detection.addAction(self.btn_border_laplacian)
        self.menuBorder_Detection.addAction(self.btn_border_laplacian_gauss)

        self.menu_thresholding.addAction(self.btn_threshold_global)
        self.menu_thresholding.addAction(self.btn_threshold_otsu)

        self.menu_difussion.addAction(self.btn_isotropic_difussion)
        self.menu_difussion.addAction(self.btn_anisotropic_leclerc_difussion)
        self.menu_difussion.addAction(self.btn_anisotropic_lorentz_difussion)

        self.menu_filter.addAction(self.btn_point_Operators.menuAction())
        self.menu_filter.addAction(self.menuNoise.menuAction())
        self.menu_filter.addAction(self.menuSpatial_Domain.menuAction())
        self.menu_filter.addAction(self.menuBorder_Detection.menuAction())
        self.menu_filter.addAction(self.menu_thresholding.menuAction())
        self.menu_filter.addAction(self.menu_difussion.menuAction())
        self.menu_filter.addAction(self.btn_equalization)
        
        self.menubar.addAction(self.menu_image.menuAction())
        self.menubar.addAction(self.menu_pixel.menuAction())
        self.menubar.addAction(self.menu_filter.menuAction())

        self.tabWidget.setCurrentIndex(0)
        self.setupTabs()

    def closeEvent(self, event):
        count = self.tabWidget.count()
        for i in range(count):
            self.tabWidget.widget(i).onCloseEvent(event)


####################### MAIN  #######################
if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    app.setStyleSheet("QMenuBar,QMenu{color: rgb(255,255,255);}")
    MainWindow = ATIGUI()

    MainWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        # if MainWindow.image_1:
        #     MainWindow.image_1.painter.end()
        # if MainWindow.original_image:
        #     MainWindow.original_image.painter.end()
        # if MainWindow.filtered_image:
        #     MainWindow.filtered_image.painter.end()
        print('Closing ATI GUI...')
