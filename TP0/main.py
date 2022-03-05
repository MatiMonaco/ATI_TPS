from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QImage 
from PIL import ImageQt

import sys 


class ATIGUI(QMainWindow):
    def __init__(self):
        super(ATIGUI,self).__init__()
        uic.loadUi('GUI/gui2.ui',self)
        self.setWindowTitle('ATI GUI')
        self.btn_open.triggered.connect(self.openImage)
        self.btn_save.triggered.connect(self.saveImage)
        self.org_img = None
        self.filt_img = None

    
    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        self.org_img = QImage(imagePath)
        pixmap = QPixmap()
        pixmap.loadFromData(open(imagePath,"rb").read())
        w = self.original_image.width()
        h = self.original_image.height()
        self.original_image.setPixmap(pixmap.scaled(w,h, Qt.KeepAspectRatio))
        
        self.original_image.mousePressEvent = self.getPixel
        self.filtered_image.setPixmap(pixmap) #todo: remove
        print("HEIGHT_ ",self.original_image.height()," WIDTH: ",self.original_image.width())
        print("2 HEIGHT_ ",self.org_img.height()," WIDTH: ",self.org_img.width())

    def getPixel(self, event):
        x       = event.pos().x()
        y       = event.pos().y() 
        color   = QColor(self.org_img.pixel(x,y))  # color object
        rgb     = color.getRgb()  # 8bit RGBA: (255, 23, 0, 255)
        self.txt_pixel.setText(f"pixel in x={x}, y={y} has value {rgb}")

    def saveImage(self):
        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.xpm *.jpg *.nef)", "")

        file = open(fileName,'w')
        image = ImageQt.fromqpixmap(self.filtered_image.pixmap()) 
        print(file.name)
        image.save(file.name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QMenuBar,QMenu{color: rgb(255,255,255);}")
    MainWindow = ATIGUI()
    
    MainWindow.show()
   
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing ATI GUI...')