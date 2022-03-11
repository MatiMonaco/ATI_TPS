from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QLabel, QWidget, QScrollArea
from PyQt5.QtCore import Qt, QRect, QPoint, QEvent

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QImage, QRgba64, QPixmap, QPainter, QIntValidator
from PIL import ImageQt
import numpy as np
import sys
import qimage2ndarray

from copy_image import CopyImageDialog
from img_operations import operate
from img_operations_test import operate_lib


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
        uic.loadUi('GUI/gui2.ui', self)

        self.setWindowTitle('ATI GUI')
        # self.btn_load.clicked.connect(self.openImage)
        ### TAB 1 ###
        self.btn_open.triggered.connect(self.loadImageTab1)
        self.btn_save.triggered.connect(self.saveImage)
        self.btn_update_pixel.clicked.connect(self.updatePixel)
        self.original_image = None
        self.filtered_image = None

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
        self.btn_copy.clicked.connect(self.copyToAnotherImage)
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
    def loadImageTab1(self):
        self.pixmap, path = self.openImage()
        if self.pixmap == None:
            return
        # self.btn_load.deleteLater()
        if self.original_image == None:
            self.original_image = QLabel(self.scroll_area_contents_orig_img)
            self.scroll_area_contents_orig_img.layout().addWidget(self.original_image)

            self.filtered_image = QLabel(self.scroll_area_contents_filt_img)
            self.scroll_area_contents_filt_img.layout().addWidget(self.filtered_image)

            self.original_image.mousePressEvent = self.handleImgClick
            self.original_image.mouseReleaseEvent = self.handleImgRelease
        #self.original_image.paintEvent = self.paintEventLbl

            self.scroll_area_orig.installEventFilter(self)

        self.filtered_image.setPixmap(self.pixmap)
        self.original_image.setPixmap(self.pixmap)

        self.original_image.adjustSize()
        self.filtered_image.adjustSize()
        print("ver max: ",  self.scroll_area_orig.verticalScrollBar().maximum())
        print("ver min: ",  self.scroll_area_orig.verticalScrollBar().minimum())

        print("hor max: ",  self.scroll_area_orig.horizontalScrollBar().maximum())
        print("hor min: ",  self.scroll_area_orig.horizontalScrollBar().minimum())

        print(f"scrollarea width: ", self.scroll_area_orig.width())
        print(f"scrollarea height: ", self.scroll_area_orig.height())

        print("HEIGHT_ ", self.original_image.height(),
              " WIDTH: ", self.original_image.width())

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        if imagePath == None or imagePath == "":
            return None

        pixmap = QPixmap()
        pixmap.loadFromData(open(imagePath, "rb").read())

        return pixmap, imagePath

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

    def saveImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "Images (*.png *.xpm *.jpg *.nef)", "")

        file = open(fileName, 'w')
        image = ImageQt.fromqpixmap(self.filtered_image.pixmap())
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
        return res_x, res_y

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

    def getPixel(self, event):
        x = event.pos().x()
        y = event.pos().y()
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

        print("vert: ", self.scroll_area_orig.verticalScrollBar().value())
        print("hor: ", self.scroll_area_orig.horizontalScrollBar().value())
        print("ver max: ",  self.scroll_area_orig.verticalScrollBar().maximum())
        print("ver min: ",  self.scroll_area_orig.verticalScrollBar().minimum())

        print("hor max: ",  self.scroll_area_orig.horizontalScrollBar().maximum())
        print("hor min: ",  self.scroll_area_orig.horizontalScrollBar().minimum())
        #
        color = QColor(self.original_image.pixmap(
        ).toImage().pixelColor(x, y))  # color object
        rgb = color.getRgb()  # 8bit RGBA: (255, 23, 0, 255)
        self.txt_pixel.setText(f"SELECTED PIXEL x={x}, y={y} with RGB={rgb}")

    def selectSubimage(self, event):
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
            img = self.original_image.pixmap().toImage()
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

        filt_img =  self.filtered_image.pixmap().toImage()
        filt_img.setPixelColor(x, y, QColor(
            QRgba64.fromRgba(r, g, b, 255)))  # QImage
        self.filtered_image.setPixmap(QPixmap.fromImage(filt_img))

        print(f'LOG: Changed pixel ({x};{y}) to rgba({r},{g},{b},255)')

    ####################### IMAGE OPERATIONS HANDLER  #######################

    def sum_imgs(self):

        img3 = operate(self.path_img1, self.path_img2, 'sum')
        #result_QImage = qimage2ndarray.array2qimage(img3)
        #self.scroll_area_contents_result.setPixmap(
        #    QPixmap.fromImage(self.filt_img))

        #self.result_image.setPixmap(QPixmap.fromImage(result_QImage.pixmap().toImage()))

    

    def substract_imgs(self):
        img3 = operate_lib(self.path_img1, self.path_img2, 'substract')
     

    def multiply_imgs(self):
        img3 = operate_lib(self.path_img1, self.path_img2, 'multiply')

    ## SELECT ##

    def paintEventLbl(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pixmap)

        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin, self.destination)
            painter.drawRect(rect.normalized())

    def handleImgClick(self, event):
        if event.buttons() & Qt.LeftButton:
            print('Point 1')
            self.begin = event.pos()
            self.destination = self.begin
            self.update()
        # empezar a dibujar el rect
        self.selectedPxlX = event.pos().x()
        self.selectedPxlY = event.pos().y()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            print('Point 2')
            self.destination = event.pos()
            self.update()

    def handleImgRelease(self, event):
        print('Point 3')
        if event.button() & Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.pixmap)
            painter.drawRect(rect.normalized())

            self.begin, self.destination = QPoint(), QPoint()
            self.update()
        releaseX = event.pos().x()
        releaseY = event.pos().y()
        if(self.selectedPxlX == releaseX and self.selectedPxlY == releaseY):
            self.getPixel(event)
        else:
            self.selectSubimage(event)


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
