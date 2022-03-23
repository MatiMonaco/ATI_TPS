
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QPoint

from PyQt5.QtGui import  QColor, QPainter
import qimage2ndarray
class QSelectionableLabel(QtWidgets.QLabel):

    def __init__(self,parent):
        super().__init__(parent)
        self.mousePressEvent = self.handleImgClick
        self.mouseReleaseEvent = self.handleImgRelease
        self.last_selection = None
        self.last_selection_begin = None
       
        self.pixel_rgb = None
        #self.selection_color = QColor(0, 223, 255)
        self.click_handler = None
        self.selection_handler = None

        self.begin  = None
        self.destination = None
        self.painter = None
    def setPixmap(self,pixmap):
        if self.painter != None:
            self.painter.end()
        self.last_selection = None
        self.last_selection_begin = None
        self.last_selection_end = None
        super().setPixmap(pixmap)
        self.painter = QPainter(self.pixmap())

    def handleImgClick(self, event):
        print("handleImgClick:",event.pos())
        if event.buttons() & Qt.LeftButton:

            self.begin = event.pos()
            self.destination = self.begin
            self.update()
        

    def clearLastSelection(self):
        print("clear selection: ",self.last_selection)
        if self.last_selection != None:
            self.painter.drawPixmap(self.last_selection_begin, self.last_selection)
           
            self.last_selection = None
            self.last_selection_begin = None
            self.last_selection_end = None
            self.update()
           
        
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

    def handleImgRelease(self, event):
      
        release_x,release_y = self.fixBounds(event.pos().x(),event.pos().y(),self.width(),self.height())

        begin_x,begin_y = self.begin.x(),self.begin.y()
        print("handleImgRelease: ", release_x, ", ", release_y)

        if event.button() & Qt.LeftButton:

            if begin_x != release_x and begin_y != release_y:
                realBegin = QPoint()
                realDest = QPoint()
                if begin_x < release_x:
                    realBegin.setX(begin_x)
                    realDest.setX(release_x)
                else:
                    realDest.setX(begin_x)
                    realBegin.setX(release_x)
                
                if begin_y < release_y:
                    realBegin.setY(begin_y)
                    realDest.setY(release_y)
                else:
                    realDest.setY(begin_y)
                    realBegin.setY(release_y)
                
                
               
                new_selection = QRect(realBegin, realDest)

                self.clearLastSelection()
              
                self.last_selection_begin = realBegin
                self.last_selection_end = realDest
                self.last_selection = self.pixmap().copy(
                    QRect(realBegin, QPoint(realDest.x() + 1, realDest.y()+1)))
              

               # painter.drawRect(new_selection, QBrush( self.selection_color)) <- No tenemos alpha channel
                self.painter.drawRect(new_selection)

                self.begin, self.destination = QPoint(), QPoint()
                self.update()
                if self.selection_handler != None:
                    self.selection_handler(self)

            else:
               
                if self.click_handler != None:
                    self.click_handler(self)
           
    def getSelectedPixel(self):
        # todo ver si esta bien
        print(f"selected pixel: {self.begin.x()}, {self.begin.y()}")
        return QColor(self.pixmap().toImage().pixelColor(self.begin.x(), self.begin.y())).getRgb()  # color object
   

    def getSelectionAverage(self):
     
        if self.last_selection == None:
            return None
        rgb = qimage2ndarray.rgb_view(self.last_selection.toImage())

        # print(colors)
        avg_r = int(np.mean(rgb[:, :, 0]))
        avg_g = int(np.mean(rgb[:, :, 1]))
        avg_b = int(np.mean(rgb[:, :, 2]))

        #print(f"Pixels: {w*h}, Avg Colors: R G B")
        #self.txt_selected_pixels_amount.setText(f"SELECTED PIXELS AMOUNT: {w*h}")
        #self.txt_colors_avg.setText( f"AVG: R {avg_r:.2f} G {avg_g:.2f} B {avg_b:.2f}")
        return  [avg_r,avg_g,avg_b]
        

    def getSelectionSize(self):
        if self.last_selection == None:
            return 0,0
        return self.last_selection.width(),self.last_selection.height()

    