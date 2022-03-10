from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSizePolicy, QDialog, QLabel
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QImage, QRgba64, QPixmap, QPainter
from PIL import ImageQt
import numpy as np
import sys

from  copy_image import CopyImageDialog 
from img_operations import operate

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
        super(ATIGUI,self).__init__()
        uic.loadUi('GUI/gui2.ui',self)
      
        self.setWindowTitle('ATI GUI')
        self.btn_open.triggered.connect(self.openImage)
        self.btn_save.triggered.connect(self.saveImage)
        self.btn_update_pixel.clicked.connect(self.updatePixel)
        self.btn_copy_img.triggered.connect(self.copyToAnotherImage)
        self.btn_sum_imgs.clicked.connect(self.sum_imgs)
        self.btn_substract_imgs.clicked.connect(self.substract_imgs)
        self.btn_multiply_imgs.clicked.connect(self.multiply_imgs)
        self.org_img = None
        self.filt_img = None
        self.selectedPxlX = None
        self.selectedPxlY = None
        
        # self.pixmap = QPixmap(self.rect().size())
        # self.pixmap.fill(Qt.white)
        # self.begin, self.destination = QPoint(), QPoint()	


    
    ####################### IMAGE HANDLER ####################### 

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        self.org_img = QImage(imagePath)
        self.filt_img = QImage(imagePath)
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(open(imagePath,"rb").read())
        w = self.original_image.width()
        h = self.original_image.height()
        self.original_image.resize(w,h)
        self.filtered_image.resize(w,h)
        #self.original_image.setPixmap(pixmap)
        
        self.original_image.mousePressEvent = self.handleImgClick
        self.original_image.mouseReleaseEvent = self.handleImgRelease
        self.original_image.paintEvent = self.paintEventLbl
        self.filtered_image.setPixmap(self.pixmap.scaled(w, h))  # todo: remove
        self.original_image.setPixmap(self.pixmap.scaled(w, h))
        print("HEIGHT_ ",self.original_image.height()," WIDTH: ",self.original_image.width())
        print("2 HEIGHT_ ",self.org_img.height()," WIDTH: ",self.org_img.width())
   

    def saveImage(self):
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.xpm *.jpg *.nef)", "")

        file = open(fileName,'w')
        image = ImageQt.fromqpixmap(self.filtered_image.pixmap()) 
        print(f'LOG: saved filtered image to {file.name}')
        image.save(file.name)

    def copyToAnotherImage(self): 
  
        dialog = QDialog()
        dialog.ui = CopyImageDialog()
        dialog.ui.setupUi(dialog)
        #dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

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
        x       = event.pos().x()
        y       = event.pos().y() 
        color   = QColor(self.original_image.pixmap().toImage().pixelColor(x, y))  # color object
        rgb     = color.getRgb()  # 8bit RGBA: (255, 23, 0, 255)
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
            colors = list(map(lambda point: img.pixelColor(point[0], point[1]).getRgb(),mat))
            print(colors)
            avg_r = np.mean(np.array(list(map(lambda rgba: rgba[0],colors))))
            avg_g = np.mean(np.array(list(map(lambda rgba: rgba[1],colors))))
            avg_b = np.mean(np.array(list(map(lambda rgba: rgba[2],colors))))
            width  = abs(self.selectedPxlX - endPxlX)
            height = abs(self.selectedPxlY - endPxlY)
            print(f"Pixels: {height * width}, Avg Colors: R G B")
            self.txt_selected_pixels_amount.setText(f"SELECTED PIXELS AMOUNT: {height * width}")
            self.txt_colors_avg.setText(f"AVG: R {avg_r:.2f} G {avg_g:.2f} B {avg_b:.2f}")
            self.selectedPxlX = None
            self.selectedPxlY = None

    def updatePixel(self):

        x       = int(self.input_pixel_x.text())
        y       = int(self.input_pixel_y.text())

        r       = int(self.input_pixel_new_r.text())
        g       = int(self.input_pixel_new_g.text())
        b       = int(self.input_pixel_new_b.text()) 

        self.filt_img.setPixelColor(x, y, QColor(QRgba64.fromRgba(r, g, b, 255))) #QImage 
        self.filtered_image.setPixmap(QPixmap.fromImage(self.filt_img))

        print(f'LOG: Changed pixel ({x};{y}) to rgba({r},{g},{b},255)')

    ####################### IMAGE OPERATIONS HANDLER  #######################

    def sum_imgs(self): 

        return 
    
    def substract_imgs(self): 
        return 

    def multiply_imgs(self): 
        return 


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
        releaseX       = event.pos().x()
        releaseY       = event.pos().y() 
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