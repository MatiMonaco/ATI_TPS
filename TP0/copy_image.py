from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSizePolicy, QDialog
from PyQt5.QtCore import Qt, QRect
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QImage, QRgba64

class CopyImageDialog(): 

    def __init__(self):
         
        uic.loadUi('GUI/gui.ui',self)
      