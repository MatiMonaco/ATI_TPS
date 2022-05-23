from filters.advanced_edge_detection.canny import Canny
from filters.advanced_edge_detection.canny_rgb import CannyRGB
from filters.noise.salt_pepper_noise_filter import SaltPepperNoiseFilter
from PyQt5.QtWidgets import   QLabel, QWidget, QScrollArea
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QColor, QRgba64, QIntValidator, QCloseEvent
import numpy as np
import qimage2ndarray
from PyQt5.QtGui import QIcon
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
from filters.spatial_domain.bilateral_mask import BilateralMask
from filters.equalization.equalization_filter import EqualizationFilter
from filters.spatial_domain.border_detection.prewitt import PrewittFilter
from filters.spatial_domain.border_detection.sobel import SobelFilter
from filters.spatial_domain.border_detection.directional import DirectionalFilter
from dialogs.modify_pixel_dialog import ModifyPixelDialog
from components.QSelectionableLabel import QSelectionableLabel
from PyQt5.QtGui import QIntValidator, QImage
from PyQt5 import QtWidgets,QtCore,QtGui
from filters.thresholding.global_thresholding_filter import GlobalThresholdingFilter
from filters.thresholding.otsu_thresholding import OtsuThresholdingFilter
from filters.difussion.isotropic_difussion import  IsotropicFilter
from filters.difussion.anisotropic_leclerc_difussion import AnisotropicLeclercFilter
from filters.difussion.anisotropic_lorentz_difussion import AnisotropicLorentzFilter 
from filters.feature_extraction.straight_line import HoughTransformStraightLine 
from filters.feature_extraction.circle import HoughTransformCircle 
from filters.advanced_edge_detection.susan import Susan

from libs.TP0.img_operations import openImage, openImageOrZip, saveImage, saveImages
from components.tabs.tab import Tab
import resources.resources as resources
orig_windows = set()
filt_windows = set()

class ImageContainer:
    def __init__(self, pixmap: QPixmap):
        img                                             = pixmap.toImage()
        isGrayscale                                     = img.isGrayscale()
        self.orig_pixmap     , self.filt_pixmap         = pixmap, pixmap
        self.orig_img        , self.filt_img            = img, img
        self.orig_isGrayscale, self.filt_isGrayscale    = isGrayscale, isGrayscale
        self.filt_image_states                          = []

    def update(self, pixmap: QPixmap) -> None:
        self.filt_image_states.append(self.filt_pixmap)
        self.filt_pixmap        = pixmap
        self.filt_img           = pixmap.toImage()
        self.filt_isGrayscale   = self.filt_img.isGrayscale()

    def goBack(self) -> tuple:
        if(not self.filt_image_states):
            return None, None
        last_pixmap             = self.filt_image_states.pop()
        self.filt_pixmap        = last_pixmap
        self.filt_img           = last_pixmap.toImage()
        self.filt_isGrayscale   = self.filt_img.isGrayscale()
        return self.filt_pixmap, self.filt_img    
    
    def reset(self) -> tuple:
        self.filt_image_states  = []
        self.filt_pixmap        = self.orig_pixmap
        self.filt_img           = self.orig_img
        self.filt_isGrayscale   = self.orig_isGrayscale
        return self.filt_pixmap, self.filt_img

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

        self.images = []
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

        self.filter_dic[FilterType.GLOBAL_THRESHOLDING] = GlobalThresholdingFilter()
        self.filter_dic[FilterType.OTSU_THRESHOLDING] = OtsuThresholdingFilter()

        self.filter_dic[FilterType.ISOTROPIC_DIFUSSION] = IsotropicFilter(self.applyFilter)
        self.filter_dic[FilterType.ANISOTROPIC_LECLERC_DIFUSSION] = AnisotropicLeclercFilter(self.applyFilter)
        self.filter_dic[FilterType.ANISOTROPIC_LORENTZ_DIFUSSION] = AnisotropicLorentzFilter(self.applyFilter)
 
        
        self.filter_dic[FilterType.SPATIAL_DOMAIN_BILATERAL_MASK] = BilateralMask(self.applyFilter)

        self.filter_dic[FilterType.CANNY] = Canny(self.applyFilter)
        self.filter_dic[FilterType.CANNY_RGB] = CannyRGB(self.applyFilter)
        self.filter_dic[FilterType.SUSAN] = Susan(self.applyFilter)


        self.filter_dic[FilterType.HOUGH_TRANSFORM_LINE] = HoughTransformStraightLine(self.applyFilter)
        self.filter_dic[FilterType.HOUGH_TRANSFORM_CIRCLE] = HoughTransformCircle(self.applyFilter)

        self.btn_go_back.clicked.connect(self.goBack)
        self.btn_reset.clicked.connect(self.reset)

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
        # self.clearStates()
        filt_pixmap, filt_img = self.currImg().reset()
        self.filtered_image.setPixmap(filt_pixmap)
        self.updateHistogram(filt_img,
                             self.hist_filt_canvas, self.hist_filt_axes)

    def openOrigNewTab(self):
        if self.original_image == None:
            return
        orig_img_viewer = ImgViewerWindow(self.original_image.pixmap(), "orig")
        orig_img_viewer.show()
        orig_windows.add(orig_img_viewer)

    def openFiltNewTab(self):
        if self.filtered_image == None:
            return
        filt_img_viewer = ImgViewerWindow(self.filtered_image.pixmap(), "filt")
        filt_img_viewer.show()
        filt_windows.add(filt_img_viewer)

    def loadImageTab1(self):
        # pixmap = openImage()
        pixmaps = openImageOrZip()
        # if pixmap == None:
        #     return
        if pixmaps == None:
            return
        # self.btn_load.deleteLater()

        # img = pixmap.toImage()
        self.images = list(map(lambda p: ImageContainer(p), pixmaps))
        self.initImgIterator(self.images)
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

        # self.clearStates()
        curr                = self.currImg()
        pixmap              = curr.orig_pixmap
        self.isGrayscale    = curr.orig_isGrayscale

        self.filtered_image.setPixmap(pixmap)
        self.original_image.setPixmap(pixmap)
        self.original_image.adjustSize()
        self.filtered_image.adjustSize()

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
        if not self.video_controls_VLayout.isEmpty() and not self.hasNextImg():
            self.removeVideoControls()
        else:
       
            # self.video_controls_VLayout.addLayout(self.video_controls_HLayout)
            self.btn_prev_image.show()
            self.btn_next_image.show()
            self.curr_image_counter.show()
            self.curr_image_counter.setText(f"1/{self.max_imgs}")

    def removeVideoControls(self):
        self.btn_next_image.hide()
        self.btn_prev_image.hide()
        self.curr_image_counter.hide()
        # self.video_controls_VLayout.removeWidget(
        #     self.video_controls_VLayout.itemAt(0).widget())
        # self.video_controls_HLayout.setParent(None)


    def loadVideoControls(self):
        self.video_controls_HLayout = QtWidgets.QHBoxLayout()
        self.video_controls_VLayout.addLayout(self.video_controls_HLayout)

        self.btn_prev_image = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_prev_image.sizePolicy().hasHeightForWidth())
        self.btn_prev_image.setSizePolicy(sizePolicy)
        self.btn_prev_image.setIcon(QIcon('resources/back.png'))
        self.btn_prev_image.clicked.connect(self.renderPrevImg)
        self.video_controls_HLayout.addWidget(self.btn_prev_image)

        self.video_controls_HLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.curr_image_counter = QtWidgets.QLabel()
        self.curr_image_counter.setAlignment(QtCore.Qt.AlignCenter)
        self.curr_image_counter.setStyleSheet("font-weight:bold;")
        
        self.video_controls_HLayout.addWidget(self.curr_image_counter)

        self.video_controls_HLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.btn_next_image = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_next_image.sizePolicy().hasHeightForWidth())
        self.btn_next_image.setSizePolicy(sizePolicy)
        self.btn_next_image.setIcon(QIcon('resources/next.png'))
        self.btn_next_image.clicked.connect(self.renderNextImg)
        self.video_controls_HLayout.addWidget(self.btn_next_image)
        self.video_controls_HLayout.addItem(QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.video_controls_HLayout.setStretch(0,1)
        self.video_controls_HLayout.setStretch(1,1)
        self.video_controls_HLayout.setStretch(2,1)
        self.video_controls_HLayout.setStretch(3,1)
        self.video_controls_HLayout.setStretch(4,1)
        self.video_controls_HLayout.setStretch(5,5)
        self.btn_next_image.hide()
        self.btn_prev_image.hide()
        self.curr_image_counter.hide()

        

    ##################### IMGS HANDLER ####################
    def initImgIterator(self, imgs: list) -> None:
        self.curr_img_idx, self.max_imgs = 0, len(imgs)
    
    def currImg(self) -> ImageContainer:
        return self.images[self.curr_img_idx]
    
    def nextImg(self) -> ImageContainer:
        if self.hasNextImg():
            self.curr_img_idx += 1
        return self.images[self.curr_img_idx]

    def prevImg(self) -> ImageContainer:
        if self.hasPrevImg():
            self.curr_img_idx -= 1
        return self.images[self.curr_img_idx]
    
    def hasNextImg(self) -> bool:
        return self.curr_img_idx + 1 < self.max_imgs
    
    def hasPrevImg(self) -> bool:
        return self.curr_img_idx - 1 >= 0

    def renderNextImg(self):
        img_meta = self.nextImg()
        self.original_image.setPixmap(img_meta.orig_pixmap)
        self.filtered_image.setPixmap(img_meta.filt_pixmap)
        self.curr_image_counter.setText(f"{self.curr_img_idx+1}/{self.max_imgs}")
        self.updateHistograms()

    def renderPrevImg(self):
        img_meta = self.prevImg()
        self.original_image.setPixmap(img_meta.orig_pixmap)
        self.filtered_image.setPixmap(img_meta.filt_pixmap)
        self.curr_image_counter.setText(f"{self.curr_img_idx+1}/{self.max_imgs}")
        self.updateHistograms()
        
    ##################### FILTERS ####################

    def saveState(self):
        pixmap = self.filtered_image.pixmap()
        self.filtered_image_states.append(
            pixmap.copy(0, 0, pixmap.width(), pixmap.height()))

    def clearStates(self):
        self.filtered_image_states = []

    def goBack(self):
       # print("saved_states: ", self.filtered_image_states)
        # if(not self.filtered_image_states):
        #     return
        # last_pixmap = self.filtered_image_states.pop()
        last_pixmap, last_img = self.currImg().goBack()
        if last_pixmap == None:
            return 
        #print("last state: ", last_pixmap)
        #print("current pixmap: ", self.filtered_image.pixmap())
        self.filtered_image.setPixmap(last_pixmap)
        self.updateHistogram(last_img,
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
        # self.saveState()
        print(
            f"------------- Applying {self.current_filter.name()} -------------")
        # img =   self.filtered_image.pixmap().toImage()
        for img_meta in self.images:
            img = img_meta.filt_img
            isGrayscale = img_meta.filt_isGrayscale
            filtered_pixmap = self.current_filter.applyFilter(img, isGrayscale)
            img_meta.update(filtered_pixmap)

        self.filtered_image.setPixmap(self.currImg().filt_pixmap)
        # curr = self.currImg()
        # img = curr.filt_img
        # isGrayscale = curr.filt_isGrayscale
        # filtered_pixmap = self.current_filter.applyFilter(img, isGrayscale)
        # self.currImg().update(filtered_pixmap)
        # self.filtered_image.setPixmap(filtered_pixmap)
        self.updateHistograms()
        self.current_filter.after()
        print("------------- Filter applied -------------")
    ##################################################

    def updateHistograms(self):
        curr = self.currImg()
        self.updateHistogram(curr.orig_img,
                             self.hist_orig_canvas, self.hist_orig_axes)
        self.updateHistogram(curr.filt_img,
                             self.hist_filt_canvas, self.hist_filt_axes)

    def updateHistogram(self, img, canvas, axes):
        # img = pixmap.toImage()
        hist_arr = qimage2ndarray.rgb_view(img)

        if self.isGrayscale:
            gray_arr = hist_arr[:, :, 0].flatten()
            axes.clear()
            axes.hist(
                gray_arr, color="gray", weights=np.zeros_like(gray_arr) + 1. / gray_arr.size, bins=256)
           
            #get x and y limits
            x_left, x_right = axes.get_xlim()
            y_low, y_high = axes.get_ylim()

            #set aspect ratio
            axes.set_aspect(abs((x_right-x_left)/(y_low-y_high))*1.0)
        else:
            r_arr = hist_arr[:, :, 0].flatten()
            g_arr = hist_arr[:, :, 1].flatten()
            b_arr = hist_arr[:, :, 2].flatten()
            # self.hist_orig_axes[0].set_xlim(0,255)
            axes[0].clear()
            axes[0].set_xlim(0, 256)
            axes[0].hist(
                r_arr, color="red", weights=np.zeros_like(r_arr) + 1. / r_arr.size, bins=256)

        
            #get x and y limits
            x_left, x_right =  axes[0].get_xlim()
            y_low, y_high =  axes[0].get_ylim()

            #set aspect ratio
            axes[0].set_aspect(abs((x_right-x_left)/(y_low-y_high))*1.0)

            # self.hist_orig_axes[1].set_xlim(0,255)
            axes[1].clear()
            axes[1].set_xlim(0, 256)
            axes[1].hist(
                g_arr, color="green", weights=np.zeros_like(g_arr) + 1. / g_arr.size, bins=256)
            
            x_left, x_right = axes[1].get_xlim()
            y_low, y_high = axes[1].get_ylim()
            axes[1].set_aspect(abs((x_right-x_left)/(y_low-y_high))*1.0)
            # self.hist_orig_axes[2].set_xlim(0,255)
            axes[2].clear()
            axes[2].set_xlim(0, 256)
            axes[2].hist(
                b_arr, color="blue", weights=np.zeros_like(b_arr) + 1. / b_arr.size, bins=256)
            x_left, x_right = axes[2].get_xlim()
            y_low, y_high = axes[2].get_ylim()
            axes[2].set_aspect(abs((x_right-x_left)/(y_low-y_high))*1.0)

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
        if self.filtered_image != None and self.images != None and len(self.images) > 0:
            saveImages(self, list(map(lambda meta: meta.filt_pixmap, self.images)))
            # pixmap = self.filtered_image.pixmap()
            # if pixmap != None:
            #     saveImage(self,pixmap)

    def modifyPixel(self):
        if self.filtered_image == None:
            return
        pixmap = self.filtered_image.pixmap()

        dialog = ModifyPixelDialog(pixmap.width()-1, pixmap.height()-1)

        code = dialog.exec()

        if code == 1:

            x, y, r, g, b = dialog.getInputs()
            # self.saveState()
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

    ###########################################################################################################################
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
        icon.addPixmap(QtGui.QPixmap(":/icons/new_tab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
      
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

        self.video_controls_VLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.addLayout(self.video_controls_VLayout)
        self.loadVideoControls()
        

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
   