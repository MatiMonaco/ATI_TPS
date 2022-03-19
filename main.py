
import os
from filters.noise.salt_pepper_noise_filter import SaltPepperNoiseFilter
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QWidget, QScrollArea
from PyQt5.QtCore import Qt, QRect, QPoint, QEvent
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QRgba64, QPainter, QIntValidator
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
from libs.TP1.raw_size_input_dialog import RawSizeInputDialog
from filters.noise.salt_pepper_noise_filter import SaltPepperNoiseFilter
from filters.spatial_domain.mean_mask import MeanMask
from filters.spatial_domain.median_mask import MedianMask
from filters.spatial_domain.border_mask import BorderMask
from filters.spatial_domain.weighted_median_mask import WeightedMedianMask
from filters.spatial_domain.gauss_mask import GaussMask


class ImgLabel(QLabel):
    def __init__(self):
        self.selectedPxlX = None
        self.selectedPxlY = None

    def resetCoords(self):
        self.selectedPxlX = None
        self.selectedPxlY = None

    def click(self, x, y):
        if(self.selectedPxlX != None and self.selectedPxlY != None):
            self.selectedPxlX = x
            self.selectedPxlY = y
        else:
            pass


class ATIGUI(QMainWindow):
    def __init__(self):
        super(ATIGUI, self).__init__()
        uic.loadUi('main_gui.ui', self)

        self.setWindowTitle('ATI GUI')
        # self.btn_load.clicked.connect(self.openImage)

        ### TAB 1 ###
        self.btn_open.triggered.connect(self.loadImageTab1)
        self.btn_save.triggered.connect(self.saveTab1)
        self.btn_update_pixel.clicked.connect(self.updatePixel)
        self.original_image = None
        self.filtered_image = None

        ###### FILTERS #####
        self.current_filter = None

        #Point Operators
        self.btn_thresholding_filter.triggered.connect(
            lambda: self.changeFilter(FilterType.THRESHOLDING))
        self.btn_negative_filter.triggered.connect(
            lambda: {self.changeFilter(FilterType.NEGATIVE), self.applyFilter()})
        self.btn_gamma_filter.triggered.connect(
            lambda: self.changeFilter(FilterType.GAMMA_POWER))

        #Noises   
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
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_MEAN_MASK), self.applyFilter()})
        self.btn_median_mask.triggered.connect(
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_MEDIAN_MASK), self.applyFilter()})
        self.btn_weighted_median_mask.triggered.connect(
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_WEIGHTED_MEDIAN_MASK), self.applyFilter()})
        self.btn_border_mask.triggered.connect(
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_BORDER_MASK), self.applyFilter()})
        self.btn_gauss_mask.triggered.connect(
            lambda: {self.changeFilter(FilterType.SPATIAL_DOMAIN_GAUSS_MASK), self.applyFilter()})
            
            

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

        self.filter_dic[FilterType.SPATIAL_DOMAIN_MEAN_MASK] = MeanMask(self.applyFilter)
        self.filter_dic[FilterType.SPATIAL_DOMAIN_MEDIAN_MASK] = MedianMask(self.applyFilter)
        self.filter_dic[FilterType.SPATIAL_DOMAIN_WEIGHTED_MEDIAN_MASK] = WeightedMedianMask(self.applyFilter)
        self.filter_dic[FilterType.SPATIAL_DOMAIN_BORDER_MASK] = BorderMask(self.applyFilter)
        self.filter_dic[FilterType.SPATIAL_DOMAIN_GAUSS_MASK] = GaussMask(self.applyFilter)

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
        self.btn_go_back.clicked.connect(self.reset)

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

    ####################### IMAGE HANDLER #######################

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

    def loadImageTab1(self):
        pixmap = self.openImage()
        if pixmap == None:
            return
        # self.btn_load.deleteLater()

        img = pixmap.toImage()
        print(f"is grey scale: {img.isGrayscale()}")
        #print(f"colors: ", qimage2ndarray.byte_view(img))
        if self.original_image == None:
            self.original_image = QLabel(self.scroll_area_contents_orig_img)
            self.scroll_area_contents_orig_img.layout().addWidget(self.original_image)

            self.filtered_image = QLabel(self.scroll_area_contents_filt_img)
            self.scroll_area_contents_filt_img.layout().addWidget(self.filtered_image)
            #self.original_image.mouseMoveEvent = self.mouseMoveEvent
            self.original_image.mousePressEvent = self.handleImgClick
            self.original_image.mouseReleaseEvent = lambda event: self.handleImgRelease(
                event, self.original_image)

            self.filtered_image.mousePressEvent = self.handleImgClick
            self.filtered_image.mouseReleaseEvent = lambda event: self.handleImgRelease(
                event, self.filtered_image)
        #self.original_image.paintEvent = self.paintEventLbl

            self.scroll_area_orig.installEventFilter(self)

        self.filtered_image.setPixmap(pixmap)
        self.original_image.setPixmap(pixmap)

        self.original_image.adjustSize()
        self.filtered_image.adjustSize()

        isGrayscale = img.isGrayscale()

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
    def changeFilter(self, index):
        if self.filtered_image == None:
            return
     
        if self.current_filter != None:
          
            self.filter_layout.removeWidget(
                self.filter_layout.itemAt(0).widget())
            self.current_filter.setParent(None)

        self.current_filter = self.filter_dic[index]
        print(f"CURRENT FILTER : {self.current_filter}")
        if self.current_filter == None:
            return
        self.filter_layout.addWidget(self.current_filter)
        # self.applyFilter()

    def applyFilter(self, options = None):
        print("Apply filter")
        if self.current_filter == None:
            return
        filtered_pixmap = self.current_filter.apply(
            self.filtered_image.pixmap())
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
                gray_arr, color="gray", weights=np.zeros_like(gray_arr) + 1. / gray_arr.size)
        else:
            r_arr = hist_arr[:, :, 0].flatten()
            g_arr = hist_arr[:, :, 1].flatten()
            b_arr = hist_arr[:, :, 2].flatten()
            # self.hist_orig_axes[0].set_xlim(0,255)
            axes[0].clear()
            axes[0].hist(
                r_arr, color="red", weights=np.zeros_like(r_arr) + 1. / r_arr.size)

            # self.hist_orig_axes[1].set_xlim(0,255)
            axes[1].clear()
            axes[1].hist(
                g_arr, color="green", weights=np.zeros_like(g_arr) + 1. / g_arr.size)

            # self.hist_orig_axes[2].set_xlim(0,255)
            axes[2].clear()
            axes[2].hist(
                b_arr, color="blue", weights=np.zeros_like(b_arr) + 1. / b_arr.size)

        canvas.draw()

  
            
           

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()


        if imagePath == None or imagePath == "":
            return None
           # this will return a tuple of root and extension
        split_path = os.path.splitext(imagePath)
        file_extension = split_path[1]
        print(split_path)
        pixmap = None
        if file_extension.upper() == ".RAW":
            print("ES RAW")
         
            pixmap = self.read_raw_image(imagePath)
          
        else:
            pixmap = QPixmap()
            pixmap.loadFromData(open(imagePath, "rb").read())
            

        return pixmap

    def read_raw_image(self,imagePath):
        with open(imagePath, 'r') as infile:
            data = np.fromfile(infile, dtype=np.uint8)
           
            size = len(data)
            dialog = RawSizeInputDialog()
           
            width = 0
            height = 0
            code = 1
            while size != width * height and code == 1:
                code = dialog.exec()
             
                width,height = dialog.getInputs()

            if code == 0:
                return None

            data = data.reshape(height,width)
      
         
            return QPixmap.fromImage(qimage2ndarray.gray2qimage(data))


    def interpolate(self, value, min1, max1, min2, max2):
        return min2 + ((value-min1)/(max1-min1)) * (max2-min2)

    def eventFilter(self, source, event):

        if event.type() == QEvent.MouseMove:
            print(f"event x: {event.pos().x()}, event y: {event.pos().y()}")
            print("TYPE: ", type(source))
            if type(source) == QScrollArea:

                if self.last_time_move_Y == 0:
                    self.last_time_move_Y = event.pos().y()
                if self.last_time_move_X == 0:
                    self.last_time_move_X = event.pos().x()

                #distanceY = self.last_time_move_Y - event.pos().y()
                #distanceX = self.last_time_move_X - event.pos().x()
                vert_scroll_bar = source.verticalScrollBar()
                hor_scroll_bar = source.horizontalScrollBar()
                print("vert: ", vert_scroll_bar.value())
                print("hor: ", hor_scroll_bar.value())
                print(f"scrollarea width: ", source.width())
                print(f"scrollarea height: ", source.height())

                vert_scroll_bar.setValue(self.interpolate(
                    event.pos().y(), 0, source.height(), 0, vert_scroll_bar.maximum()))
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

        # Chequeo que no se pase de las dimensiones
        print(
            f"img1 start: ({img1_x1},{img1_y1}), img end: ({img1_x2},{img1_y2})")
        print(f"img2: ({img2_x},{img2_y})")
        img1 = self.image_1.pixmap().toImage()

        img1_x1, img1_y1 = self.fixBounds(
            img1_x1, img1_y1, img_width, img_height)
        img2_x, img2_y = self.fixBounds(
            img2_x, img2_y, img_width, img_height)
        img1_x2, img1_y2 = self.fixBounds(
            img1_x2, img1_y2, img_width, img_height)
        print(
            f"img1 start: ({img1_x1},{img1_y1}), img end: ({img1_x2},{img1_y2})")
        print(f"img1 w: {img_width} img1 h: {img_height}")

        print(f"img2: ({img2_x},{img2_y})")

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
        return res_x,res_y

    ####################### PIXEL HANDLER  #######################

    # def handleImgRelease(self, event):
    #     releaseX       = event.pos().x()
    #     releaseY       = event.pos().y()
    #     if(self.selectedPxlX == releaseX and self.selectedPxlY == releaseY):
    #         self.getPixel(event)
    #     else:
    #         self.selectSubimage(event)

    # def handleImgClick(self, event):
    #     # empezar a dibujar el rect
    #     self.selectedPxlX = event.pos().x()
    #     self.selectedPxlY = event.pos().y()

    def getPixel(self, x, y):

        print(f"x: {x}, y: {y}")
        # todo ver si esta bien
        if x >= self.original_image.width():
            x = self.original_image.width()
        elif x <= 0:
            x = 0
        if y >= self.original_image.height():
            y = self.original_image.height()
        elif y <= 0:
            y = 0

        #
        color = QColor(self.original_image.pixmap(
        ).toImage().pixelColor(x, y))  # color object
        rgb = color.getRgb()  # 8bit RGBA: (255, 23, 0, 255)
        self.txt_pixel.setText(f"SELECTED PIXEL x={x}, y={y} with RGB={rgb}")

    def selectSubimage(self, event, img_label):
        if(self.selectedPxlX == None and self.selectedPxlX == None):
            self.selectedPxlX = event.pos().x()
            self.selectedPxlY = event.pos().y()
        else:
            endPxlX = event.pos().x()
            endPxlY = event.pos().y()
            startX, startY, endX, endY = 0, 0, 0, 0
            if(self.selectedPxlX < endPxlX):
                startX = int(self.selectedPxlX)
                endX = int(endPxlX)
            else:
                endX = int(self.selectedPxlX)
                startX = int(endPxlX)
            if(self.selectedPxlY < endPxlY):
                startY = int(self.selectedPxlY)
                endY = int(endPxlY)
            else:
                endY = int(self.selectedPxlY)
                startY = int(endPxlY)
            mat = []
            img = img_label.pixmap().toImage()

            startX, startY = self.fixBounds(
                startX, startY, img.width(), img.height())
            endX, endY = self.fixBounds(endX, endY, img.width(), img.height())

            for pixY in range(startY, endY+1):
                for pixX in range(startX, endX + 1):
                    mat.append((pixX, pixY))
            colors = list(map(lambda point: img.pixelColor(
                point[0], point[1]).getRgb(), mat))
           # print(colors)
            avg_r = np.mean(np.array(list(map(lambda rgba: rgba[0], colors))))
            avg_g = np.mean(np.array(list(map(lambda rgba: rgba[1], colors))))
            avg_b = np.mean(np.array(list(map(lambda rgba: rgba[2], colors))))
            width = abs(self.selectedPxlX - endPxlX)
            height = abs(self.selectedPxlY - endPxlY)
            print(f"Pixels: {height * width}, Avg Colors: R G B")
            self.txt_selected_pixels_amount.setText(
                f"SELECTED PIXELS AMOUNT: {height * width}")
            self.txt_colors_avg.setText(
                f"AVG: R {avg_r:.2f} G {avg_g:.2f} B {avg_b:.2f}")
            self.selectedPxlX = None
            self.selectedPxlY = None

    def updatePixel(self):

        x = int(self.input_pixel_x.text())
        y = int(self.input_pixel_y.text())

        r = int(self.input_pixel_new_r.text())
        g = int(self.input_pixel_new_g.text())
        b = int(self.input_pixel_new_b.text())

        filt_img = self.filtered_image.pixmap().toImage()
        filt_img.setPixelColor(x, y, QColor(
            QRgba64.fromRgba(r, g, b, 255)))  # QImage
        self.filtered_image.setPixmap(QPixmap.fromImage(filt_img))

        print(f'LOG: Changed pixel ({x};{y}) to rgba({r},{g},{b},255)')

    ####################### IMAGE OPERATIONS HANDLER  #######################

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

    ## SELECT ##

    # def paintEventLbl(self, event):
    #     painter = QPainter(self)
    #     painter.drawPixmap(QPoint(), self.pixmap)

    #     if not self.begin.isNull() and not self.destination.isNull():
    #         rect = QRect(self.begin, self.destination)
    #         painter.drawRect(rect.normalized())

    def handleImgClick(self, event):

        if event.buttons() & Qt.LeftButton:

            self.begin = event.pos()
            self.destination = self.begin
            self.update()
        # empezar a dibujar el rect
        self.selectedPxlX = event.pos().x()
        self.selectedPxlY = event.pos().y()

    def mouseMoveEvent(self, event):
        self.destination = event.pos()
        self.update()
       

    def handleImgRelease(self, event, img_label):
        print("IMAGE RELEASE")
        if event.button() & Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            painter = QPainter(img_label.pixmap())
            painter.drawRect(rect.normalized())

            self.begin, self.destination = QPoint(), QPoint()
            self.update()
        releaseX = event.pos().x()
        releaseY = event.pos().y()
        if(self.selectedPxlX == releaseX and self.selectedPxlY == releaseY):
            self.getPixel(releaseX, releaseY)
        else:
            self.selectSubimage(event, img_label)


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
