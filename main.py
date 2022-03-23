import os
from filters.noise.salt_pepper_noise_filter import SaltPepperNoiseFilter
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QWidget, QScrollArea
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QRgba64, QIntValidator, QCloseEvent
from PIL import ImageQt
import numpy as np
import sys
import qimage2ndarray
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from libs.TP0.img_operations import operate
from filters.filter import FilterType
from filters.point_operators.negative_filter import NegativeFilter
from filters.point_operators.thresholding_filter import ThresholdingFilter
from filters.point_operators.gamma_power_filter import GammaPowerFilter
from filters.noise.gauss_noise_filter import GaussNoiseFilter
from filters.noise.exponential_noise_filter import ExponentialNoiseFilter
from filters.noise.rayleigh_noise_filter import RayleighNoiseFilter
from filters.noise.salt_pepper_noise_filter import SaltPepperNoiseFilter
from filters.spatial_domain.mean_mask import MeanMaskFilter
from filters.spatial_domain.median_mask import MedianMaskFilter
from filters.spatial_domain.border_mask import BorderMaskFilter
from filters.spatial_domain.weighted_median_mask import WeightedMedianMaskFilter
from filters.spatial_domain.gauss_mask import GaussMaskFilter
from filters.equalization.equalization_filter import EqualizationFilter
from dialogs.raw_size_input_dialog import RawSizeInputDialog
from dialogs.modify_pixel_dialog import ModifyPixelDialog
from components.QSelectionableLabel import QSelectionableLabel
from PyQt5.QtGui import QIntValidator
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


class ATIGUI(QMainWindow):
    def __init__(self):
        super(ATIGUI, self).__init__()
        uic.loadUi('main_gui.ui', self)

        self.setWindowTitle('ATI GUI')
        # self.btn_load.clicked.connect(self.openImage)
        ### TAB 1 ###
        self.btn_open.triggered.connect(self.loadImageTab1)
        self.btn_save.triggered.connect(self.saveTab1)
        self.orig_img_open_tab_btn.clicked.connect(self.openOrigNewTab)
        self.filt_img_open_tab_btn.clicked.connect(self.openFiltNewTab)
        self.btn_modify_pixel.triggered.connect(self.modifyPixel)
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

 

        onlyInt = QIntValidator(0,255)
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

       
        ###### FILTERS #####
        self.current_filter = None

        # Point Operators
        self.btn_thresholding_filter.triggered.connect(
            lambda: self.changeFilter(FilterType.THRESHOLDING))
        self.btn_negative_filter.triggered.connect(
            lambda: {self.changeFilter(FilterType.NEGATIVE), self.applyFilter()})
        self.btn_gamma_filter.triggered.connect(
            lambda: self.changeFilter(FilterType.GAMMA_POWER))

        # Noises
        self.btn_rayleigh_noise.triggered.connect(
            lambda:  self.changeFilter(FilterType.RAYLEIGH))
        self.btn_exponential_noise.triggered.connect(
            lambda: self.changeFilter(FilterType.EXPONENTIAL))
        self.btn_gauss_noise.triggered.connect(
            lambda: self.changeFilter(FilterType.GAUSS))
        self.btn_salt_pepper_noise.triggered.connect(
            lambda: self.changeFilter(FilterType.SALTPEPPER))

        # Spatial Domain Masks
        self.btn_mean_mask.triggered.connect(
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_MEAN_MASK)})
        self.btn_median_mask.triggered.connect(
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_MEDIAN_MASK)})
        self.btn_weighted_median_mask.triggered.connect(
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_WEIGHTED_MEDIAN_MASK)})
        self.btn_border_mask.triggered.connect(
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_BORDER_MASK)})
        self.btn_gauss_mask.triggered.connect(
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_GAUSS_MASK)})

        # Equalization
        self.btn_equalization.triggered.connect(
            lambda: {self.changeFilter(FilterType.EQUALIZATION), self.applyFilter()})

        self.filter_dic = dict()
        self.filter_dic[FilterType.NEGATIVE] = NegativeFilter()
        self.filter_dic[FilterType.THRESHOLDING] = ThresholdingFilter(
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

      
        ############


        ### TAB 2 ###
        self.image_1 = None
        self.image_2 = None
        self.result_image = None

        self.btn_copy_img.triggered.connect(self.copyToAnotherImage)
        self.btn_sum_imgs.clicked.connect(self.sum_imgs)
        self.btn_substract_imgs.clicked.connect(self.substract_imgs)
        self.btn_multiply_imgs.clicked.connect(self.multiply_imgs)
        self.btn_load_1.clicked.connect(self.loadImage1Tab2)
        self.btn_load_2.clicked.connect(self.loadImage2Tab2)
        self.btn_res_save.clicked.connect(self.saveTab2)
        self.btn_copy.clicked.connect(self.copyToAnotherImage)
        self.btn_go_back.clicked.connect(self.goBack)

        self.onlyInt = QIntValidator()

        self.txt_x_img1.setValidator(self.onlyInt)
        self.txt_y_img1.setValidator(self.onlyInt)
        self.txt_x_img2.setValidator(self.onlyInt)
        self.txt_y_img2.setValidator(self.onlyInt)
        self.txt_x_img3.setValidator(self.onlyInt)
        self.txt_y_img3.setValidator(self.onlyInt)
        ############

        self.selectedPxlX = None
        self.selectedPxlY = None
        self.last_time_move_X = 0
        self.last_time_move_Y = 0

        self.hist_orig_canvas = None
        self.hist_filt_canvas = None

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
    
    ####################### TAB 2 ########################

    def loadImage1Tab2(self):
        # TODO: antes era self.pixmap, nose para que se usa
        pixmap, self.path_img1 = self.openImage()
        if pixmap == None:
            return
        # self.btn_load.deleteLater()
        if self.image_1 == None:
            self.image_1 = QLabel(self.scroll_area_contents_img_1)
            self.scroll_area_contents_img_1.layout().addWidget(self.image_1)

        #self.image_1.mousePressEvent = self.handleImgClick
        #self.image_1.mouseReleaseEvent = self.handleImgRelease
        self.image_1.setPixmap(pixmap)
        self.image_1.adjustSize()

        self.scroll_area_img_1.installEventFilter(self)

    def loadImage2Tab2(self):
        # TODO: antes era self.pixmap, nose para que se usa
        pixmap, self.path_img2 = self.openImage()
        if pixmap == None:
            return
        # self.btn_load.deleteLater()
        if self.image_2 == None:
            self.image_2 = QLabel(self.scroll_area_contents_img_2)
            self.scroll_area_contents_img_2.layout().addWidget(self.image_2)

        self.image_2.setPixmap(pixmap)
        self.image_2.adjustSize()

        #self.image_2.mousePressEvent = self.handleImgClick
        #self.image_2.mouseReleaseEvent = self.handleImgRelease
        #self.original_image.paintEvent = self.paintEventLbl

        self.scroll_area_img_2.installEventFilter(self)

    ####################### TAB 1 ########################

    def reset(self):
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
        pixmap = self.openImage()
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

            
    

        self.filtered_image.setPixmap(pixmap)
        
        self.original_image.setPixmap(pixmap)

        self.original_image.adjustSize()
        self.filtered_image.adjustSize()

        self.isGrayscale = img.isGrayscale()

        self.original_image.handleImgClick = lambda event: print("click: ",self.original_image.pixel_rgb)

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
        self.isGrayscale = pixmap.toImage().isGrayscale()
        axes = 3
        if self.isGrayscale:
            axes = 1
        self.hist_orig_axes = self.hist_orig_canvas.figure.subplots(
            1, axes)
        self.hist_filt_axes = self.hist_filt_canvas.figure.subplots(
            1, axes)
        #print(f"pixmap: {qimage2ndarray.byte_view(pixmap.toImage())}")

        self.updateHistograms()

    ##################### FILTERS ####################

    def saveState(self):
        pixmap = self.filtered_image.pixmap()
        self.filtered_image_states.append(
            pixmap.copy(0, 0, pixmap.width(), pixmap.height()))

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

    def changeFilter(self, index):
        if self.filtered_image == None:
            return

        if self.current_filter != None:

            self.filter_layout.removeWidget(
                self.filter_layout.itemAt(0).widget())
            self.current_filter.setParent(None)

        self.current_filter = self.filter_dic[index]
       
        if self.current_filter == None:
            return
        self.filter_layout.addWidget(self.current_filter)
        # self.applyFilter()

    def applyFilter(self, options=None):
        print("Apply filter")
        if self.current_filter == None:
            return
        self.saveState()
        self.filtered_image.clearLastSelection()
        print("aca 1")
        filtered_pixmap = self.current_filter.apply(
            self.filtered_image.pixmap().toImage())
        print("aca 2")
        self.filtered_image.setPixmap(filtered_pixmap)
        self.updateHistograms()

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
            axes[0].hist(
                r_arr, color="red", weights=np.zeros_like(r_arr) + 1. / r_arr.size, bins=256)

            # self.hist_orig_axes[1].set_xlim(0,255)
            axes[1].clear()
            axes[1].hist(
                g_arr, color="green", weights=np.zeros_like(g_arr) + 1. / g_arr.size, bins=256)

            # self.hist_orig_axes[2].set_xlim(0,255)
            axes[2].clear()
            axes[2].hist(
                b_arr, color="blue", weights=np.zeros_like(b_arr) + 1. / b_arr.size, bins=256)

        canvas.draw()

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()

        if imagePath == None or imagePath == "":
            return None
           # this will return a tuple of root and extension
        split_path = os.path.splitext(imagePath)
        file_extension = split_path[1]
      
        pixmap = None
        if file_extension.upper() == ".RAW":
         

            pixmap = self.read_raw_image(imagePath)

        else:
            pixmap = QPixmap()
            pixmap.loadFromData(open(imagePath, "rb").read())

        return pixmap

    def read_raw_image(self, imagePath):
        with open(imagePath, 'r') as infile:
            data = np.fromfile(infile, dtype=np.uint8)

            size = len(data)
            dialog = RawSizeInputDialog()

            width = 0
            height = 0
            code = 1
            while size != width * height and code == 1:
                code = dialog.exec()

                width, height = dialog.getInputs()

            if code == 0:
                return None

            data = data.reshape(height, width)

            return QPixmap.fromImage(qimage2ndarray.gray2qimage(data))

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
    
                vert_scroll_bar.setValue(int(self.interpolate(event.pos().y(), 0, source.height(), 0, vert_scroll_bar.maximum())))
                self.last_time_move_Y = event.pos().y()

                hor_scroll_bar.setValue(self.interpolate(
                    event.pos().x(), 0, source.width(), 0, hor_scroll_bar.maximum()))
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
                self.saveImage(pixmap)

    def saveTab2(self):
        if self.result_image != None:
            pixmap = self.result_image.pixmap()
            if pixmap != None:
                self.saveImage(pixmap)

    def saveImage(self, pixmap):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "Images (*.png *.xpm *.jpg *.nef)", "")

        file = open(fileName, 'w')
        image = ImageQt.fromqpixmap(pixmap)
        print(f'LOG: saved filtered image to {file.name}')
        image.save(file.name)

    def copyToAnotherImage(self):
        if self.image_1 == None or self.image_2 == None:
            return
        img1_x1 = int(self.txt_x_img1.text())
        img1_y1 = int(self.txt_y_img1.text())

        img1_x2 = int(self.txt_x_img2.text())
        img1_y2 = int(self.txt_y_img2.text())

        img2_x = int(self.txt_x_img3.text())
        img2_y = int(self.txt_y_img3.text())

        img_width = min(self.image_1.pixmap().width(),
                        self.image_2.pixmap().width())
        img_height = min(self.image_1.pixmap().height(),
                         self.image_2.pixmap().height())

       
        img1 = self.image_1.pixmap().toImage()

        img1_x1, img1_y1 = self.fixBounds(
            img1_x1, img1_y1, img_width, img_height)
        img2_x, img2_y = self.fixBounds(
            img2_x, img2_y, img_width, img_height)
        img1_x2, img1_y2 = self.fixBounds(
            img1_x2, img1_y2, img_width, img_height)
        # print(
        #     f"img1 start: ({img1_x1},{img1_y1}), img end: ({img1_x2},{img1_y2})")
        # print(f"img1 w: {img_width} img1 h: {img_height}")

        # print(f"img2: ({img2_x},{img2_y})")

        if self.result_image == None:
            self.result_image = QLabel(self.scroll_area_contents_result)
            self.scroll_area_contents_result.layout().addWidget(self.result_image)
        self.result_image.setPixmap(self.image_2.pixmap())
        self.result_image.adjustSize()
        result_img = self.result_image.pixmap().toImage()
        target_x = img2_x
        img1_x1, img1_y1, img1_x2, img1_y2 = self.getCorrectedCoords(
            img1_x1, img1_y1, img1_x2, img1_y2)
        for from_x in range(img1_x1, img1_x2+1):
            #print(f"from_x: {from_x}")
            target_y = img2_y
            for from_y in range(img1_y1, img1_y2+1):
                #print(f"from_y: {from_y}")
                pixel = img1.pixelColor(from_x, from_y)
                result_img.setPixelColor(target_x, target_y, pixel)  # QImage
                target_y += 1
            target_x += 1

            self.result_image.setPixmap(QPixmap.fromImage(result_img))

    def getCorrectedCoords(self, x1, y1, x2, y2):
        if x1 <= x2:
            if y1 <= y2:
                return x1, y1, x2, y2
            else:
                return x1, y2, x2, y1
        elif y1 <= y2:
            return x2, y1, x1, y2
        else:
            return x2, y2, x1, y1

    def fixBounds(self, target_x, target_y, img_width, img_height):
        res_x = target_x
        res_y = target_y
        if target_x > img_width:
            res_x = img_width-1
        elif target_x < 0:
            res_x = 0
        if target_y > img_height:
            res_y = img_height-1
        elif target_y < 0:
            res_y = 0
        return res_x, res_y

    ####################### PIXEL HANDLER  #######################

  
    

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

    ####################### IMAGE OPERATIONS HANDLER  
    def sum_imgs(self):

        img3 = operate(self.path_img1, self.path_img2, 'sum')
        #result_QImage = qimage2ndarray.array2qimage(img3)
        # self.scroll_area_contents_result.setPixmap(
        #    QPixmap.fromImage(self.filt_img))

        # self.result_image.setPixmap(QPixmap.fromImage(result_QImage.pixmap().toImage()))

    def substract_imgs(self):
        img3 = operate(self.path_img1, self.path_img2, 'substract')

    def multiply_imgs(self):
        img3 = operate(self.path_img1, self.path_img2, 'multiply')



  


####################### MAIN  #######################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QMenuBar,QMenu{color: rgb(255,255,255);}")
    MainWindow = ATIGUI()

    MainWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing ATI GUI...')
