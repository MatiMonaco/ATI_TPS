from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSizePolicy, QDialog
from PyQt5.QtCore import Qt, QRect
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QImage, QRgba64
from PIL import ImageQt

import sys

from  copy_image import CopyImageDialog 
from img_operations import operate


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
    
    ####################### IMAGE HANDLER ####################### 

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        self.org_img = QImage(imagePath)
        self.filt_img = QImage(imagePath)
        pixmap = QPixmap()
        pixmap.loadFromData(open(imagePath,"rb").read())
        w = self.original_image.width()
        h = self.original_image.height()
        self.original_image.resize(w,h)
        self.filtered_image.resize(w,h)
        #self.original_image.setPixmap(pixmap)
        
        self.original_image.mousePressEvent = self.getPixel
        self.filtered_image.setPixmap(pixmap.scaled(w, h))  # todo: remove
        self.original_image.setPixmap(pixmap.scaled(w, h))
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

    def getPixel(self, event):
        x       = event.pos().x()
        y       = event.pos().y() 
        color = QColor(self.original_image.pixmap().toImage().pixelColor(x, y))  # color object
        rgb     = color.getRgb()  # 8bit RGBA: (255, 23, 0, 255)
        self.txt_pixel.setText(f"pixel in x={x}, y={y} has value {rgb}")

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