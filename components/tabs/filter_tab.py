from filters.noise.salt_pepper_noise_filter import SaltPepperNoiseFilter
from PyQt5.QtWidgets import   QLabel, QWidget, QScrollArea
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QColor, QRgba64, QIntValidator, QCloseEvent
import numpy as np
import qimage2ndarray
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from filters.filter import FilterType
from filters.point_operators.negative_filter import NegativeFilter
from filters.point_operators.RGB_thresholding_filter import RGBThresholdingFilter
from filters.point_operators.gray_thresholding_filter import GrayThresholdingFilter
from filters.point_operators.gamma_power_filter import GammaPowerFilter
from filters.noise.gauss_noise_filter import GaussNoiseFilter
from filters.noise.exponential_noise_filter import ExponentialNoiseFilter
from filters.noise.rayleigh_noise_filter import RayleighNoiseFilter
from filters.noise.salt_pepper_noise_filter import SaltPepperNoiseFilter
from filters.spatial_domain.border_detection.laplacian import LaplacianFilter
from filters.spatial_domain.border_detection.laplacian_of_gauss import LaplacianOfGaussFilter
from filters.spatial_domain.mean_mask import MeanMaskFilter
from filters.spatial_domain.median_mask import MedianMaskFilter
from filters.spatial_domain.border_mask import BorderMaskFilter
from filters.spatial_domain.weighted_median_mask import WeightedMedianMaskFilter
from filters.spatial_domain.gauss_mask import GaussMaskFilter
from filters.equalization.equalization_filter import EqualizationFilter
from filters.spatial_domain.border_detection.prewitt import PrewittFilter
from filters.spatial_domain.border_detection.sobel import SobelFilter
from filters.spatial_domain.border_detection.directional import DirectionalFilter
from dialogs.modify_pixel_dialog import ModifyPixelDialog
from components.QSelectionableLabel import QSelectionableLabel
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtWidgets,QtCore,QtGui
from libs.TP0.img_operations import openImage, saveImage
from components.tabs.tab import Tab
orig_windows = set()
filt_windows = set()


class ImgViewerWindow(QWidget):
    STD_SIZE = 800

    def __init__(self, pixmap, type):
        super(ImgViewerWindow, self).__init__()
        w, h = ImgViewerWindow.STD_SIZE, ImgViewerWindow.STD_SIZE
        img = pixmap.toImage()
        if img.width() < w:
            w = img.width()
        if img.height() < h:
            h = img.height()
        self.setGeometry(0, 0, w, h)
        self.label = QLabel('label', self)
        self.label.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio))
        self.type = type
        if self.type == "orig":
            self.setWindowTitle("Original Image")
        elif self.type == "filt":
            self.setWindowTitle("Filtered Image")

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.type == "orig":
            orig_windows.discard(self)
        elif self.type == "filt":
            filt_windows.discard(self)
        return super().closeEvent(event)


class FilterTab(Tab):

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.selectedPxlX = None
        self.selectedPxlY = None
        self.last_time_move_X = 0
        self.last_time_move_Y = 0

        self.hist_orig_canvas = None
        self.hist_filt_canvas = None
        self.orig_img_open_tab_btn.clicked.connect(self.openOrigNewTab)
        self.filt_img_open_tab_btn.clicked.connect(self.openFiltNewTab)
        self.original_image = None
        self.filtered_image = None

        self.filtered_image_states = []
        self.orig_pixel_color.setPixmap(QPixmap(25, 25))
        self.orig_pixel_color.pixmap().fill(Qt.gray)

        self.orig_avg_color.setPixmap(QPixmap(25, 25))
        self.orig_avg_color.pixmap().fill(Qt.gray)

        self.filt_pixel_color.setPixmap(QPixmap(25, 25))
        self.filt_pixel_color.pixmap().fill(Qt.gray)

        self.filt_avg_color.setPixmap(QPixmap(25, 25))
        self.filt_avg_color.pixmap().fill(Qt.gray)

        onlyInt = QIntValidator(0, 255)
        self.orig_pixel_R_line_edit.setValidator(onlyInt)
        self.orig_pixel_G_line_edit.setValidator(onlyInt)
        self.orig_pixel_B_line_edit.setValidator(onlyInt)
        self.filt_pixel_R_line_edit.setValidator(onlyInt)
        self.filt_pixel_G_line_edit.setValidator(onlyInt)
        self.filt_pixel_B_line_edit.setValidator(onlyInt)

        self.orig_avg_R_line_edit.setValidator(onlyInt)
        self.orig_avg_G_line_edit.setValidator(onlyInt)
        self.orig_avg_B_line_edit.setValidator(onlyInt)
        self.filt_avg_R_line_edit.setValidator(onlyInt)
        self.filt_avg_G_line_edit.setValidator(onlyInt)
        self.filt_avg_B_line_edit.setValidator(onlyInt)

        self.isGrayscale = False
        self.current_filter_index = None
        ###### FILTERS #####
        self.current_filter = None
        self.filter_dic = dict()
        self.filter_dic[FilterType.NEGATIVE] = NegativeFilter()
        self.filter_dic[FilterType.RGB_THRESHOLDING] = RGBThresholdingFilter(
            self.applyFilter)
        self.filter_dic[FilterType.GRAY_THRESHOLDING] = GrayThresholdingFilter(
            self.applyFilter)
        self.filter_dic[FilterType.GAMMA_POWER] = GammaPowerFilter(
            self.applyFilter)

        self.filter_dic[FilterType.GAUSS] = GaussNoiseFilter(self.applyFilter)
        self.filter_dic[FilterType.EXPONENTIAL] = ExponentialNoiseFilter(
            self.applyFilter)
        self.filter_dic[FilterType.RAYLEIGH] = RayleighNoiseFilter(
            self.applyFilter)
        self.filter_dic[FilterType.SALTPEPPER] = SaltPepperNoiseFilter(
            self.applyFilter)

        self.filter_dic[FilterType.SPATIAL_DOMAIN_MEAN_MASK] = MeanMaskFilter(
            self.applyFilter)
        self.filter_dic[FilterType.SPATIAL_DOMAIN_MEDIAN_MASK] = MedianMaskFilter(
            self.applyFilter)
        self.filter_dic[FilterType.SPATIAL_DOMAIN_WEIGHTED_MEDIAN_MASK] = WeightedMedianMaskFilter(
            self.applyFilter)
        self.filter_dic[FilterType.SPATIAL_DOMAIN_BORDER_MASK] = BorderMaskFilter(
            self.applyFilter)
        self.filter_dic[FilterType.SPATIAL_DOMAIN_GAUSS_MASK] = GaussMaskFilter(
            self.applyFilter)

        self.filter_dic[FilterType.EQUALIZATION] = EqualizationFilter()

        self.filter_dic[FilterType.BORDER_DETECTION_PREWITT] = PrewittFilter(
            self.applyFilter)
        self.filter_dic[FilterType.BORDER_DETECTION_SOBEL] = SobelFilter(
            self.applyFilter)
        self.filter_dic[FilterType.BORDER_DETECTION_DIRECTIONS] = DirectionalFilter(
            self.applyFilter)
        self.filter_dic[FilterType.BORDER_DETECTION_LAPLACIAN] = LaplacianFilter(
            self.applyFilter)
        self.filter_dic[FilterType.BORDER_DETECTION_LOG] = LaplacianOfGaussFilter(
            self.applyFilter)


        self.btn_go_back.clicked.connect(self.goBack)
        self.btn_reset.clicked.connect(self.reset)

    def setupUI(self):

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, -1, 10, -1)
 
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.original_image_text = QtWidgets.QLabel(self)
        self.original_image_text.setStyleSheet("color:rgb(255, 255, 255)")
        self.original_image_text.setAlignment(QtCore.Qt.AlignCenter)
        self.original_image_text.setText("ORIGINAL IMAGE")
     
        self.horizontalLayout.addWidget(self.original_image_text)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_go_back = QtWidgets.QPushButton(self)
        self.btn_go_back.setText("UNDO")
        self.btn_go_back.setStyleSheet("color:rgb(255, 255, 255)")
     
        self.horizontalLayout.addWidget(self.btn_go_back)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btn_reset = QtWidgets.QPushButton(self)
        self.btn_reset.setText("RESET")
      
        self.horizontalLayout.addWidget(self.btn_reset)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 9)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.orig_img_HLayout = QtWidgets.QHBoxLayout()
        self.orig_img_HLayout.setSizeConstraint(
            QtWidgets.QLayout.SetMinAndMaxSize)
        self.orig_img_HLayout.setContentsMargins(0, -1, 0, -1)
        self.orig_img_HLayout.setSpacing(6)
    
        self.scroll_area_orig = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_orig.sizePolicy().hasHeightForWidth())
        self.scroll_area_orig.setSizePolicy(sizePolicy)
        self.scroll_area_orig.setAcceptDrops(True)
        self.scroll_area_orig.setWidgetResizable(True)
        self.scroll_area_orig.setAlignment(QtCore.Qt.AlignCenter)
      
        self.scroll_area_contents_orig_img = QtWidgets.QWidget()
        self.scroll_area_contents_orig_img.setGeometry(
            QtCore.QRect(180, 125, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_contents_orig_img.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_orig_img.setSizePolicy(sizePolicy)
       
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(
            self.scroll_area_contents_orig_img)
    
        self.scroll_area_orig.setWidget(self.scroll_area_contents_orig_img)
        self.orig_img_HLayout.addWidget(self.scroll_area_orig)
        self.orig_img_open_tab_btn = QtWidgets.QPushButton(self)
        self.orig_img_open_tab_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            "../../resources/new_tab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.orig_img_open_tab_btn.setIcon(icon)
        self.orig_img_open_tab_btn.setIconSize(QtCore.QSize(16, 16))
        self.orig_img_open_tab_btn.setFlat(True)
     
        self.orig_img_HLayout.addWidget(self.orig_img_open_tab_btn)
        spacerItem3 = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.orig_img_HLayout.addItem(spacerItem3)
        self.scroll_area_hist_orig = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_hist_orig.sizePolicy().hasHeightForWidth())
        self.scroll_area_hist_orig.setSizePolicy(sizePolicy)
        self.scroll_area_hist_orig.setWidgetResizable(True)
        self.scroll_area_hist_orig.setAlignment(QtCore.Qt.AlignCenter)
      
        self.scroll_area_contents_hist_orig = QtWidgets.QWidget()
        self.scroll_area_contents_hist_orig.setGeometry(
            QtCore.QRect(0, 0, 379, 268))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_contents_hist_orig.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_hist_orig.setSizePolicy(sizePolicy)
     
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(
            self.scroll_area_contents_hist_orig)
    
        self.scroll_area_hist_orig.setWidget(
            self.scroll_area_contents_hist_orig)
        self.orig_img_HLayout.addWidget(self.scroll_area_hist_orig)
        self.orig_img_HLayout.setStretch(0, 3)
        self.orig_img_HLayout.setStretch(2, 1)
        self.orig_img_HLayout.setStretch(3, 3)
        self.verticalLayout_2.addLayout(self.orig_img_HLayout)
        self.filt_img_HLayout = QtWidgets.QHBoxLayout()
     
        self.scroll_area_filt_img = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_filt_img.sizePolicy().hasHeightForWidth())
        self.scroll_area_filt_img.setSizePolicy(sizePolicy)
        self.scroll_area_filt_img.setWidgetResizable(True)
        self.scroll_area_filt_img.setAlignment(QtCore.Qt.AlignCenter)
      
        self.scroll_area_contents_filt_img = QtWidgets.QWidget()
        self.scroll_area_contents_filt_img.setGeometry(
            QtCore.QRect(180, 124, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_contents_filt_img.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_filt_img.setSizePolicy(sizePolicy)
      
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(
            self.scroll_area_contents_filt_img)
     
        self.scroll_area_filt_img.setWidget(self.scroll_area_contents_filt_img)
        self.filt_img_HLayout.addWidget(self.scroll_area_filt_img)
        self.filt_img_open_tab_btn = QtWidgets.QPushButton(self)
        self.filt_img_open_tab_btn.setText("")
        self.filt_img_open_tab_btn.setIcon(icon)
        self.filt_img_open_tab_btn.setIconSize(QtCore.QSize(16, 16))
        self.filt_img_open_tab_btn.setFlat(True)
      
        self.filt_img_HLayout.addWidget(self.filt_img_open_tab_btn)
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.filt_img_HLayout.addItem(spacerItem4)
        self.scroll_area_hist_filt = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_hist_filt.sizePolicy().hasHeightForWidth())
        self.scroll_area_hist_filt.setSizePolicy(sizePolicy)
        self.scroll_area_hist_filt.setWidgetResizable(True)
        self.scroll_area_hist_filt.setAlignment(QtCore.Qt.AlignCenter)
     
        self.scroll_area_contents_hist_filt = QtWidgets.QWidget()
        self.scroll_area_contents_hist_filt.setGeometry(
            QtCore.QRect(0, 0, 379, 267))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_contents_hist_filt.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_hist_filt.setSizePolicy(sizePolicy)
     
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(
            self.scroll_area_contents_hist_filt)
      
        self.scroll_area_hist_filt.setWidget(
            self.scroll_area_contents_hist_filt)
        self.filt_img_HLayout.addWidget(self.scroll_area_hist_filt)
        self.filt_img_HLayout.setStretch(0, 3)
        self.filt_img_HLayout.setStretch(2, 1)
        self.filt_img_HLayout.setStretch(3, 3)
        self.verticalLayout_2.addLayout(self.filt_img_HLayout)
        self.filter_layout = QtWidgets.QVBoxLayout()
       
        self.verticalLayout_2.addLayout(self.filter_layout)
        self.orig_img_selection_layout = QtWidgets.QGroupBox(self)
        self.orig_img_selection_layout.setTitle("Original Image")
     
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(
            self.orig_img_selection_layout)
       
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
      
        self.label_orig_clicked_pixel = QtWidgets.QLabel(self.orig_img_selection_layout)
        self.label_orig_clicked_pixel.setStyleSheet("font-weight:bold;")
        self.label_orig_clicked_pixel.setText("Clicked pixel")
      
        self.horizontalLayout_2.addWidget(self.label_orig_clicked_pixel)
        self.label_orig_clicked_R = QtWidgets.QLabel(self.orig_img_selection_layout)
        self.label_orig_clicked_R.setStyleSheet("font-weight:bold;")
        self.label_orig_clicked_R.setText("R")
      
        self.horizontalLayout_2.addWidget(self.label_orig_clicked_R)
        self.orig_pixel_R_line_edit = QtWidgets.QLineEdit(
            self.orig_img_selection_layout)
        self.orig_pixel_R_line_edit.setStyleSheet("font-weight:bold;")
       
        self.horizontalLayout_2.addWidget(self.orig_pixel_R_line_edit)
        self.label_orig_clicked_G = QtWidgets.QLabel(self.orig_img_selection_layout)
        self.label_orig_clicked_G.setStyleSheet("font-weight:bold;")
        self.label_orig_clicked_G.setText("G")
        self.horizontalLayout_2.addWidget(self.label_orig_clicked_G)
        self.orig_pixel_G_line_edit = QtWidgets.QLineEdit(
            self.orig_img_selection_layout)
        self.orig_pixel_G_line_edit.setStyleSheet("font-weight:bold;")
       
        self.horizontalLayout_2.addWidget(self.orig_pixel_G_line_edit)
        self.label_orig_clicked_B = QtWidgets.QLabel(self.orig_img_selection_layout)
        self.label_orig_clicked_B.setStyleSheet("font-weight:bold;")
        self.label_orig_clicked_B.setText("B")
        self.horizontalLayout_2.addWidget(self.label_orig_clicked_B)
        self.orig_pixel_B_line_edit = QtWidgets.QLineEdit(
            self.orig_img_selection_layout)
        self.orig_pixel_B_line_edit.setStyleSheet("font-weight:bold;")
     
        self.horizontalLayout_2.addWidget(self.orig_pixel_B_line_edit)
        self.orig_pixel_color = QtWidgets.QLabel(
            self.orig_img_selection_layout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.orig_pixel_color.sizePolicy().hasHeightForWidth())
        self.orig_pixel_color.setSizePolicy(sizePolicy)
        self.orig_pixel_color.setMinimumSize(QtCore.QSize(25, 25))
        self.orig_pixel_color.setStyleSheet("background-color: lightgray;\n"
                                            "border-width: 1px;\n"
                                            "border-style: solid;\n"
                                            "border-color: white;")
        self.orig_pixel_color.setText("")
        self.orig_pixel_color.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
     
        self.horizontalLayout_2.addWidget(self.orig_pixel_color)
        self.line_5 = QtWidgets.QFrame(self.orig_img_selection_layout)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
       
        self.horizontalLayout_2.addWidget(self.line_5)
        self.label_orig_selection_avg = QtWidgets.QLabel(self.orig_img_selection_layout)
        self.label_orig_selection_avg.setStyleSheet("font-weight:bold;")
        self.label_orig_selection_avg.setText("Selection Average")
        self.horizontalLayout_2.addWidget(self.label_orig_selection_avg)
        self.label_orig_avg_R = QtWidgets.QLabel(self.orig_img_selection_layout)
        self.label_orig_avg_R.setStyleSheet("font-weight:bold;")
        self.label_orig_avg_R.setText("R")
        self.horizontalLayout_2.addWidget(self.label_orig_avg_R)
        self.orig_avg_R_line_edit = QtWidgets.QLineEdit(
            self.orig_img_selection_layout)
        self.orig_avg_R_line_edit.setStyleSheet("font-weight:bold;")
    
        self.horizontalLayout_2.addWidget(self.orig_avg_R_line_edit)
        self.label_orig_avg_G = QtWidgets.QLabel(self.orig_img_selection_layout)
        self.label_orig_avg_G.setStyleSheet("font-weight:bold;")
        self.label_orig_avg_G.setText("G")
        self.horizontalLayout_2.addWidget(self.label_orig_avg_G)
        self.orig_avg_G_line_edit = QtWidgets.QLineEdit(
            self.orig_img_selection_layout)
        self.orig_avg_G_line_edit.setStyleSheet("font-weight:bold;")
      
        self.horizontalLayout_2.addWidget(self.orig_avg_G_line_edit)
        self.label_orig_avg_B = QtWidgets.QLabel(self.orig_img_selection_layout)
        self.label_orig_avg_B.setStyleSheet("font-weight:bold;")
        self.label_orig_avg_B.setText("B")
        self.horizontalLayout_2.addWidget(self.label_orig_avg_B)
        self.orig_avg_B_line_edit = QtWidgets.QLineEdit(
            self.orig_img_selection_layout)
        self.orig_avg_B_line_edit.setStyleSheet("font-weight:bold;")
     
        self.horizontalLayout_2.addWidget(self.orig_avg_B_line_edit)
        self.orig_avg_color = QtWidgets.QLabel(self.orig_img_selection_layout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.orig_avg_color.sizePolicy().hasHeightForWidth())
        self.orig_avg_color.setSizePolicy(sizePolicy)
        self.orig_avg_color.setMinimumSize(QtCore.QSize(25, 25))
        self.orig_avg_color.setStyleSheet("background-color: lightgray;\n"
                                          "border-width: 1px;\n"
                                          "border-style: solid;\n"
                                          "border-color: white;")
        self.orig_avg_color.setText("")
      
        self.horizontalLayout_2.addWidget(self.orig_avg_color)
        self.verticalLayout_15.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.orig_img_selection_layout)
        self.filt_img_selection_layout = QtWidgets.QGroupBox(self)
        self.filt_img_selection_layout.setTitle("Filtered Image")
  
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(
            self.filt_img_selection_layout)
      
        self.label_filt_clicked_pixel = QtWidgets.QLabel(self.filt_img_selection_layout)
        self.label_filt_clicked_pixel.setStyleSheet("font-weight:bold;")
        self.label_filt_clicked_pixel.setText("Clicked Pixel")
        self.horizontalLayout_3.addWidget(self.label_filt_clicked_pixel)
        self.label_filt_clicked_R = QtWidgets.QLabel(self.filt_img_selection_layout)
        self.label_filt_clicked_R.setStyleSheet("font-weight:bold;")
        self.label_filt_clicked_R.setText("R")
        self.horizontalLayout_3.addWidget(self.label_filt_clicked_R)
        self.filt_pixel_R_line_edit = QtWidgets.QLineEdit(
            self.filt_img_selection_layout)
        self.filt_pixel_R_line_edit.setStyleSheet("font-weight:bold;")
       
        self.horizontalLayout_3.addWidget(self.filt_pixel_R_line_edit)
        self.label_filt_clicked_G = QtWidgets.QLabel(self.filt_img_selection_layout)
        self.label_filt_clicked_G.setStyleSheet("font-weight:bold;")
        self.label_filt_clicked_G.setText("G")
        self.horizontalLayout_3.addWidget(self.label_filt_clicked_G)
        self.filt_pixel_G_line_edit = QtWidgets.QLineEdit(
            self.filt_img_selection_layout)
        self.filt_pixel_G_line_edit.setStyleSheet("font-weight:bold;")
      
        self.horizontalLayout_3.addWidget(self.filt_pixel_G_line_edit)
        self.label_filt_clicked_B = QtWidgets.QLabel(self.filt_img_selection_layout)
        self.label_filt_clicked_B.setStyleSheet("font-weight:bold;")
        self.label_filt_clicked_B.setText("B")
        self.horizontalLayout_3.addWidget(self.label_filt_clicked_B)
        self.filt_pixel_B_line_edit = QtWidgets.QLineEdit(
            self.filt_img_selection_layout)
        self.filt_pixel_B_line_edit.setStyleSheet("font-weight:bold;")
        
        self.horizontalLayout_3.addWidget(self.filt_pixel_B_line_edit)
        self.filt_pixel_color = QtWidgets.QLabel(
            self.filt_img_selection_layout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filt_pixel_color.sizePolicy().hasHeightForWidth())
        self.filt_pixel_color.setSizePolicy(sizePolicy)
        self.filt_pixel_color.setMinimumSize(QtCore.QSize(25, 25))
        self.filt_pixel_color.setStyleSheet("background-color: lightgray;\n"
                                            "border-width: 1px;\n"
                                            "border-style: solid;\n"
                                            "border-color: white;")
        self.filt_pixel_color.setText("")
        self.filt_pixel_color.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
      
        self.horizontalLayout_3.addWidget(self.filt_pixel_color)
        self.line_6 = QtWidgets.QFrame(self.filt_img_selection_layout)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
     
        self.horizontalLayout_3.addWidget(self.line_6)
        self.label_filt_selection_avg = QtWidgets.QLabel(self.filt_img_selection_layout)
        self.label_filt_selection_avg.setStyleSheet("font-weight:bold;")
        self.label_filt_selection_avg.setText("Selection Average")
        self.horizontalLayout_3.addWidget(self.label_filt_selection_avg)
        self.label_filt_avg_R = QtWidgets.QLabel(self.filt_img_selection_layout)
        self.label_filt_avg_R.setStyleSheet("font-weight:bold;")
        self.label_filt_avg_R.setText("R")
        self.horizontalLayout_3.addWidget(self.label_filt_avg_R)
        self.filt_avg_R_line_edit = QtWidgets.QLineEdit(
            self.filt_img_selection_layout)
        self.filt_avg_R_line_edit.setStyleSheet("font-weight:bold;")
       
        self.horizontalLayout_3.addWidget(self.filt_avg_R_line_edit)
        self.label_filt_avg_G = QtWidgets.QLabel(self.filt_img_selection_layout)
        self.label_filt_avg_G.setStyleSheet("font-weight:bold;")
        self.label_filt_avg_G.setText("G")
        self.horizontalLayout_3.addWidget(self.label_filt_avg_G)
        self.filt_avg_G_line_edit = QtWidgets.QLineEdit(
            self.filt_img_selection_layout)
        self.filt_avg_G_line_edit.setStyleSheet("font-weight:bold;")
      
        self.horizontalLayout_3.addWidget(self.filt_avg_G_line_edit)
        self.label_filt_avg_B = QtWidgets.QLabel(self.filt_img_selection_layout)
        self.label_filt_avg_B.setStyleSheet("font-weight:bold;")
        self.label_filt_avg_B.setText("B")
        self.horizontalLayout_3.addWidget(self.label_filt_avg_B)
        self.filt_avg_B_line_edit = QtWidgets.QLineEdit(
            self.filt_img_selection_layout)
        self.filt_avg_B_line_edit.setStyleSheet("font-weight:bold;")
       
        self.horizontalLayout_3.addWidget(self.filt_avg_B_line_edit)
        self.filt_avg_color = QtWidgets.QLabel(self.filt_img_selection_layout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filt_avg_color.sizePolicy().hasHeightForWidth())
        self.filt_avg_color.setSizePolicy(sizePolicy)
        self.filt_avg_color.setMinimumSize(QtCore.QSize(25, 25))
        self.filt_avg_color.setStyleSheet("background-color: lightgray;\n"
                                          "border-width: 1px;\n"
                                          "border-style: solid;\n"
                                          "border-color: white;")
        self.filt_avg_color.setText("")
        self.horizontalLayout_3.addWidget(self.filt_avg_color)
     
        self.verticalLayout_2.addWidget(self.filt_img_selection_layout)
        self.verticalLayout_2.setStretch(1, 3)
        self.verticalLayout_2.setStretch(2, 3)

    def origImgClickHandler(self, label):
        #x,y = label.begin.x(),label.begin.y()
        label.clearLastSelection()
        self.orig_avg_R_line_edit.setText("")
        self.orig_avg_G_line_edit.setText("")
        self.orig_avg_B_line_edit.setText("")
        self.orig_avg_color.pixmap().fill(Qt.gray)
        self.orig_avg_color.update()

        rgb = label.getSelectedPixel()
        self.orig_pixel_R_line_edit.setText(str(rgb[0]))
        self.orig_pixel_G_line_edit.setText(str(rgb[1]))
        self.orig_pixel_B_line_edit.setText(str(rgb[2]))
        self.orig_pixel_color.pixmap().fill(QColor(rgb[0], rgb[1], rgb[2]))
        self.orig_pixel_color.update()

    def origImgSelectionHandler(self,label):
        avg_rgb = label.getSelectionAverage()
        #w, h = label.getSelectionSize()
        self.orig_avg_R_line_edit.setText(str(avg_rgb[0]))
        self.orig_avg_G_line_edit.setText(str(avg_rgb[1]))
        self.orig_avg_B_line_edit.setText(str(avg_rgb[2]))
        self.orig_avg_color.pixmap().fill(
            QColor(int(avg_rgb[0]), int(avg_rgb[1]), int(avg_rgb[2])))
        self.orig_avg_color.update()

    def filtImgClickHandler(self, label):
        #x, y = label.begin.x(), label.begin.y()
        label.clearLastSelection()
        self.filt_avg_R_line_edit.setText("")
        self.filt_avg_G_line_edit.setText("")
        self.filt_avg_B_line_edit.setText("")
        self.filt_avg_color.pixmap().fill(Qt.gray)
        self.filt_avg_color.update()

        rgb = label.getSelectedPixel()
        self.filt_pixel_R_line_edit.setText(str(rgb[0]))
        self.filt_pixel_G_line_edit.setText(str(rgb[1]))
        self.filt_pixel_B_line_edit.setText(str(rgb[2]))
        self.filt_pixel_color.pixmap().fill(QColor(rgb[0], rgb[1], rgb[2]))
        self.filt_pixel_color.update()

    def filtImgSelectionHandler(self, label):
        avg_rgb = label.getSelectionAverage()
        #w, h = label.getSelectionSize()
        self.filt_avg_R_line_edit.setText(str(avg_rgb[0]))
        self.filt_avg_G_line_edit.setText(str(avg_rgb[1]))
        self.filt_avg_B_line_edit.setText(str(avg_rgb[2]))
        self.filt_avg_color.pixmap().fill(
            QColor(int(avg_rgb[0]), int(avg_rgb[1]), int(avg_rgb[2])))
        self.filt_avg_color.update()


    def reset(self):
        self.original_image.clearLastSelection()
        self.clearStates()
        self.filtered_image.setPixmap(self.original_image.pixmap())
        self.updateHistogram(self.filtered_image.pixmap(),
                             self.hist_filt_canvas, self.hist_filt_axes)

    def openOrigNewTab(self):
        orig_img_viewer = ImgViewerWindow(self.original_image.pixmap(), "orig")
        orig_img_viewer.show()
        orig_windows.add(orig_img_viewer)

    def openFiltNewTab(self):
        filt_img_viewer = ImgViewerWindow(self.filtered_image.pixmap(), "filt")
        filt_img_viewer.show()
        filt_windows.add(filt_img_viewer)

    def loadImageTab1(self):
        pixmap = openImage()
        if pixmap == None:
            return
        # self.btn_load.deleteLater()

        img = pixmap.toImage()

        #print(f"colors: ", qimage2ndarray.byte_view(img))
        if self.original_image == None:
            self.original_image = QSelectionableLabel(
                self.scroll_area_contents_orig_img)
            self.scroll_area_contents_orig_img.layout().addWidget(self.original_image)

            self.filtered_image = QSelectionableLabel(
                self.scroll_area_contents_filt_img)
            self.scroll_area_contents_filt_img.layout().addWidget(self.filtered_image)

            self.scroll_area_orig.installEventFilter(self)
            self.original_image.click_handler = self.origImgClickHandler
            self.original_image.selection_handler = self.origImgSelectionHandler
            self.filtered_image.click_handler = self.filtImgClickHandler
            self.filtered_image.selection_handler = self.filtImgSelectionHandler

        self.clearStates()

        self.filtered_image.setPixmap(pixmap)

        self.original_image.setPixmap(pixmap)

        self.original_image.adjustSize()
        self.filtered_image.adjustSize()

        self.isGrayscale = img.isGrayscale()

        print("IS GRAY SCALE: ", self.isGrayscale)
        if self.hist_orig_canvas == None:

            self.hist_orig_canvas = FigureCanvas(Figure(figsize=(5, 3)))
            self.hist_orig_canvas.figure.subplots_adjust(left=0.1,
                                                         bottom=0.1,
                                                         right=0.9,
                                                         top=0.9,
                                                         wspace=0.4,
                                                         hspace=0.4)
            self.scroll_area_contents_hist_orig.layout().addWidget(
                NavigationToolbar(self.hist_orig_canvas, self))
            self.scroll_area_contents_hist_orig.layout().addWidget(self.hist_orig_canvas)

        if self.hist_filt_canvas == None:

            self.hist_filt_canvas = FigureCanvas(Figure(figsize=(5, 3)))
            self.hist_filt_canvas.figure.subplots_adjust(left=0.1,
                                                         bottom=0.1,
                                                         right=0.9,
                                                         top=0.9,
                                                         wspace=0.4,
                                                         hspace=0.4)
            self.scroll_area_contents_hist_filt.layout().addWidget(
                NavigationToolbar(self.hist_filt_canvas, self))
            self.scroll_area_contents_hist_filt.layout().addWidget(self.hist_filt_canvas)

        self.hist_orig_canvas.figure.clear()
        self.hist_filt_canvas.figure.clear()

        axes = 3
        if self.isGrayscale:
            axes = 1
        self.hist_orig_axes = self.hist_orig_canvas.figure.subplots(
            1, axes)
        self.hist_filt_axes = self.hist_filt_canvas.figure.subplots(
            1, axes)
        #print(f"pixmap: {qimage2ndarray.byte_view(pixmap.toImage())}")

        self.updateHistograms()
        if self.current_filter != None:

            self.filter_layout.removeWidget(
                self.filter_layout.itemAt(0).widget())
            self.current_filter.setParent(None)
            self.current_filter = None

    ##################### FILTERS ####################

    def saveState(self):
        pixmap = self.filtered_image.pixmap()
        self.filtered_image_states.append(
            pixmap.copy(0, 0, pixmap.width(), pixmap.height()))

    def clearStates(self):
        self.filtered_image_states = []

    def goBack(self):
       # print("saved_states: ", self.filtered_image_states)
        if(not self.filtered_image_states):
            return
        last_pixmap = self.filtered_image_states.pop()
        #print("last state: ", last_pixmap)
        #print("current pixmap: ", self.filtered_image.pixmap())
        self.filtered_image.setPixmap(last_pixmap)
        self.updateHistogram(last_pixmap,
                             self.hist_filt_canvas, self.hist_filt_axes)

    def changeFilter(self, index,apply=False):
        if self.filtered_image == None:
            return

        if self.current_filter != None:

            self.filter_layout.removeWidget(
                self.filter_layout.itemAt(0).widget())
            self.current_filter.setParent(None)

        self.current_filter = self.filter_dic[index]
        self.current_filter_index = index

        if self.current_filter == None:
            return

        self.filter_layout.addWidget(self.current_filter)
        if apply:
            self.applyFilter()

    def applyFilter(self, options=None):
        if self.current_filter == None:
            return

        self.filtered_image.clearLastSelection()
        self.saveState()
        print(
            f"------------- Applying {self.current_filter.name()} -------------")
        filtered_pixmap = self.current_filter.applyFilter(
            self.filtered_image.pixmap().toImage(),self.isGrayscale)
        self.filtered_image.setPixmap(filtered_pixmap)
        self.updateHistograms()
        self.current_filter.after()
        print("------------- Filter applied -------------")
    ##################################################

    def updateHistograms(self):
        self.updateHistogram(self.original_image.pixmap(),
                             self.hist_orig_canvas, self.hist_orig_axes)
        self.updateHistogram(self.filtered_image.pixmap(),
                             self.hist_filt_canvas, self.hist_filt_axes)

    def updateHistogram(self, pixmap, canvas, axes):
        img = pixmap.toImage()
        hist_arr = qimage2ndarray.rgb_view(img)

        if self.isGrayscale:
            gray_arr = hist_arr[:, :, 0].flatten()
            axes.clear()
            axes.hist(
                gray_arr, color="gray", weights=np.zeros_like(gray_arr) + 1. / gray_arr.size, bins=256)
        else:
            r_arr = hist_arr[:, :, 0].flatten()
            g_arr = hist_arr[:, :, 1].flatten()
            b_arr = hist_arr[:, :, 2].flatten()
            # self.hist_orig_axes[0].set_xlim(0,255)
            axes[0].clear()
            axes[0].set_xlim(0, 256)
            axes[0].hist(
                r_arr, color="red", weights=np.zeros_like(r_arr) + 1. / r_arr.size, bins=256)

            # self.hist_orig_axes[1].set_xlim(0,255)
            axes[1].clear()
            axes[0].set_xlim(0, 256)
            axes[1].hist(
                g_arr, color="green", weights=np.zeros_like(g_arr) + 1. / g_arr.size, bins=256)

            # self.hist_orig_axes[2].set_xlim(0,255)
            axes[2].clear()
            axes[0].set_xlim(0, 256)
            axes[2].hist(
                b_arr, color="blue", weights=np.zeros_like(b_arr) + 1. / b_arr.size, bins=256)

        canvas.draw()

 

 

    def interpolate(self, value, min1, max1, min2, max2):
        return min2 + ((value-min1)/(max1-min1)) * (max2-min2)

    def eventFilter(self, source, event):

        if event.type() == QEvent.MouseMove:

            if type(source) == QScrollArea:

                if self.last_time_move_Y == 0:
                    self.last_time_move_Y = event.pos().y()
                if self.last_time_move_X == 0:
                    self.last_time_move_X = event.pos().x()

                vert_scroll_bar = source.verticalScrollBar()
                hor_scroll_bar = source.horizontalScrollBar()

                vert_scroll_bar.setValue(int(self.interpolate(
                    event.pos().y(), 0, source.height(), 0, vert_scroll_bar.maximum())))
                self.last_time_move_Y = event.pos().y()

                hor_scroll_bar.setValue(int(self.interpolate(
                    event.pos().x(), 0, source.width(), 0, hor_scroll_bar.maximum())))
                self.last_time_move_X = event.pos().x()

        elif event.type() == QEvent.MouseButtonRelease:

            if type(source) == QScrollArea:
                self.last_time_move_X = 0
                self.last_time_move_Y = 0
        return QWidget.eventFilter(self, source, event)

    def saveTab1(self):
        if self.filtered_image != None:
            pixmap = self.filtered_image.pixmap()
            if pixmap != None:
                saveImage(self,pixmap)

    def modifyPixel(self):
        if self.filtered_image == None:
            return
        pixmap = self.filtered_image.pixmap()

        dialog = ModifyPixelDialog(pixmap.width()-1, pixmap.height()-1)

        code = dialog.exec()

        if code == 1:

            x, y, r, g, b = dialog.getInputs()
            self.saveState()
            filt_img = pixmap.toImage()
            filt_img.setPixelColor(x, y, QColor(
                QRgba64.fromRgba(r, g, b, 255)))  # QImage
            self.filtered_image.setPixmap(QPixmap.fromImage(filt_img))

            print(f'LOG: Changed pixel ({x};{y}) to rgba({r},{g},{b},255)')

    def onCloseEvent(self,event):
        if self.original_image:
            self.original_image.painter.end()
        if self.filtered_image:
            self.filtered_image.painter.end()


   