from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QIntValidator
from components.QSelectionableLabel import QSelectionableLabel
from PyQt5.QtWidgets import  QLabel
from libs.TP0.img_operations import operate, OperationsEnum,openImage,saveImage
from PyQt5.QtGui import QPixmap,QPainter

from PyQt5.QtCore import QRect,QPoint
from components.tabs.tab import Tab

class OperationsTab(Tab):


    def __init__(self):
        super().__init__()
        self.setupUI()
        self.onlyInt = QIntValidator()

        self.txt_x_img1.setValidator(self.onlyInt)
        self.txt_y_img1.setValidator(self.onlyInt)
        self.txt_x_img2.setValidator(self.onlyInt)
        self.txt_y_img2.setValidator(self.onlyInt)
        self.txt_x_img3.setValidator(self.onlyInt)
        self.txt_y_img3.setValidator(self.onlyInt)

        ### TAB 2 ###
        self.image_1 = None
        self.image_2 = None
        self.result_image = None

        self.btn_sum_imgs.clicked.connect(lambda: self.operate(self.sum_imgs))
        self.btn_substract_imgs.clicked.connect(
            lambda: self.operate(self.substract_imgs))
        self.btn_multiply_imgs.clicked.connect(
            lambda: self.operate(self.multiply_imgs))
      
        self.btn_load_2.clicked.connect(self.loadImage2Tab2)
        self.btn_res_save.clicked.connect(self.saveTab2)
        self.btn_copy.clicked.connect(self.copyToAnotherImage)
        self.btn_load_1.clicked.connect(self.loadImage1Tab2)

    def operate(self,operation):
        self.image_1.clearLastSelection()
        operation()
    def setupUI(self):
     
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
  
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
      
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
   
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 2, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 2, 2, 1, 1)
        self.scroll_area_img_2 = QtWidgets.QScrollArea(self)
        self.scroll_area_img_2.setWidgetResizable(True)
        self.scroll_area_img_2.setAlignment(QtCore.Qt.AlignCenter)
     
        self.scroll_area_contents_img_2 = QtWidgets.QWidget()
        self.scroll_area_contents_img_2.setGeometry(QtCore.QRect(40, 5, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area_contents_img_2.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_img_2.setSizePolicy(sizePolicy)
     
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.scroll_area_contents_img_2)

        self.scroll_area_img_2.setWidget(self.scroll_area_contents_img_2)
        self.gridLayout.addWidget(self.scroll_area_img_2, 3, 1, 1, 1)
        self.scroll_area_img_1 = QtWidgets.QScrollArea(self)
        self.scroll_area_img_1.setWidgetResizable(True)
        self.scroll_area_img_1.setAlignment(QtCore.Qt.AlignCenter)
 
        self.scroll_area_contents_img_1 = QtWidgets.QWidget()
        self.scroll_area_contents_img_1.setGeometry(QtCore.QRect(40, 5, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area_contents_img_1.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_img_1.setSizePolicy(sizePolicy)
    
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.scroll_area_contents_img_1)

        self.scroll_area_img_1.setWidget(self.scroll_area_contents_img_1)
        self.gridLayout.addWidget(self.scroll_area_img_1, 1, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 2, 0, 1, 1)
        self.btn_load_2 = QtWidgets.QPushButton(self)
        self.btn_load_2.setText("LOAD IMAGE 2")
        self.btn_load_2.setStyleSheet("b")
       
        self.gridLayout.addWidget(self.btn_load_2, 3, 0, 1, 1)
        self.btn_load_1 = QtWidgets.QPushButton(self)
        self.btn_load_1.setText("LOAD IMAGE 1")
        self.gridLayout.addWidget(self.btn_load_1, 1, 0, 1, 1)
        self.gridLayout.setColumnStretch(1, 6)
        self.gridLayout.setRowStretch(1, 5)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 5)
        self.horizontalLayout_8.addLayout(self.gridLayout)
        self.scroll_area_result = QtWidgets.QScrollArea(self)
        self.scroll_area_result.setWidgetResizable(True)
        self.scroll_area_result.setAlignment(QtCore.Qt.AlignCenter)
    
        self.scroll_area_contents_result = QtWidgets.QWidget()
        self.scroll_area_contents_result.setGeometry(QtCore.QRect(40, 5, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area_contents_result.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_result.setSizePolicy(sizePolicy)
      
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scroll_area_contents_result)
     
        self.scroll_area_result.setWidget(self.scroll_area_contents_result)
        self.horizontalLayout_8.addWidget(self.scroll_area_result)
        self.horizontalLayout_8.setStretch(0, 5)
        self.horizontalLayout_8.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
 
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
    
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
    
        self.btn_sum_imgs = QtWidgets.QPushButton(self)
        self.btn_sum_imgs.setText("SUM")
      
        self.verticalLayout_6.addWidget(self.btn_sum_imgs)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
  
        self.btn_substract_imgs = QtWidgets.QPushButton(self)
        self.btn_substract_imgs.setText("SUBSTRACT")
        self.verticalLayout_7.addWidget(self.btn_substract_imgs)
        self.horizontalLayout_5.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
       
        self.btn_multiply_imgs = QtWidgets.QPushButton(self)
        self.btn_multiply_imgs.setText("MULTIPLY")
        self.verticalLayout_8.addWidget(self.btn_multiply_imgs)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)
        self.btn_reset_operations = QtWidgets.QPushButton(self)
        self.btn_reset_operations.setText("RESET")
        self.horizontalLayout_5.addWidget(self.btn_reset_operations)


        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
      
        self.label_copy_from = QtWidgets.QLabel(self)
        self.label_copy_from.setMinimumSize(QtCore.QSize(102, 0))
        self.label_copy_from.setMaximumSize(QtCore.QSize(102, 102))
        self.label_copy_from.setText("COPY FROM")
        self.horizontalLayout_9.addWidget(self.label_copy_from)
        self.line = QtWidgets.QFrame(self)
        self.line.setStyleSheet("color:white;")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
   
        self.horizontalLayout_9.addWidget(self.line)
        self.label_from_x = QtWidgets.QLabel(self)
        self.label_from_x.setText("X1")
        self.horizontalLayout_9.addWidget(self.label_from_x)
        self.txt_x_img1 = QtWidgets.QLineEdit(self)
        self.txt_x_img1.setMinimumSize(QtCore.QSize(0, 0))
    
        self.horizontalLayout_9.addWidget(self.txt_x_img1)
        self.label_from_y = QtWidgets.QLabel(self)
        self.label_from_y.setText("Y1")
        self.horizontalLayout_9.addWidget(self.label_from_y)
        self.txt_y_img1 = QtWidgets.QLineEdit(self)
 
        self.horizontalLayout_9.addWidget(self.txt_y_img1)
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
       
        self.horizontalLayout_9.addWidget(self.line_2)
        self.label_from_x2 = QtWidgets.QLabel(self)
        self.label_from_x2.setText("X2")
 
        self.horizontalLayout_9.addWidget(self.label_from_x2)
        self.txt_x_img2 = QtWidgets.QLineEdit(self)
       
        self.horizontalLayout_9.addWidget(self.txt_x_img2)
        self.label_from_y2 = QtWidgets.QLabel(self)
        self.label_from_y2.setText("Y2")
     
        self.horizontalLayout_9.addWidget(self.label_from_y2)
        self.txt_y_img2 = QtWidgets.QLineEdit(self)
  
        self.horizontalLayout_9.addWidget(self.txt_y_img2)
        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(3, 1)
        self.horizontalLayout_9.setStretch(5, 1)
        self.horizontalLayout_9.setStretch(8, 1)
        self.horizontalLayout_9.setStretch(10, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()

        self.label_copy_to = QtWidgets.QLabel(self)
        self.label_copy_to.setMinimumSize(QtCore.QSize(102, 0))
        self.label_copy_to.setMaximumSize(QtCore.QSize(102, 16777215))
        self.label_copy_to.setText("COPY TO")

        self.horizontalLayout_10.addWidget(self.label_copy_to)
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
      
        self.horizontalLayout_10.addWidget(self.line_3)
        self.label_to_x = QtWidgets.QLabel(self)
        self.label_to_x.setMaximumSize(QtCore.QSize(20, 10))
        self.label_to_x.setText("X")
        self.horizontalLayout_10.addWidget(self.label_to_x)
        self.txt_x_img3 = QtWidgets.QLineEdit(self)
     
        self.horizontalLayout_10.addWidget(self.txt_x_img3)
        self.label_to_y = QtWidgets.QLabel(self)
        self.label_to_y.setText("Y")
        self.horizontalLayout_10.addWidget(self.label_to_y)
        self.txt_y_img3 = QtWidgets.QLineEdit(self)
       
        self.horizontalLayout_10.addWidget(self.txt_y_img3)
        self.line_4 = QtWidgets.QFrame(self)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.horizontalLayout_10.addWidget(self.line_4)
        self.btn_copy = QtWidgets.QPushButton(self)
        self.btn_copy.setText("COPY")
       
        self.horizontalLayout_10.addWidget(self.btn_copy)
        self.btn_res_save = QtWidgets.QPushButton(self)
        self.btn_res_save.setText("SAVE")
  
        self.horizontalLayout_10.addWidget(self.btn_res_save)
        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(3, 1)
        self.horizontalLayout_10.setStretch(5, 1)
        self.horizontalLayout_10.setStretch(7, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.verticalLayout.setStretch(0, 8)
        self.verticalLayout.setStretch(1, 2)

    def copySelectionHandler(self,label):
        
        self.txt_x_img1.setText(str(label.last_selection_begin.x()))
        self.txt_y_img1.setText(str(label.last_selection_begin.y()))
        self.txt_x_img2.setText(str(label.last_selection_end.x()))
        self.txt_y_img2.setText(str(label.last_selection_end.y()))

    def copyClickHandler(self,event):
        
        x,y = event.pos().x(),event.pos().y()
        self.txt_x_img3.setText(str(x))
        self.txt_y_img3.setText(str(y))

    def copyToAnotherImage(self):
        if self.image_1 == None or self.image_2 == None:
            return
        img1_x1 = int(self.txt_x_img1.text())
        img1_y1 = int(self.txt_y_img1.text())

        img1_x2 = int(self.txt_x_img2.text())
        img1_y2 = int(self.txt_y_img2.text())

        img2_x = int(self.txt_x_img3.text())
        img2_y = int(self.txt_y_img3.text())

        max_img_width = min(self.image_1.pixmap().width(),
                        self.image_2.pixmap().width())
        max_img_height = min(self.image_1.pixmap().height(),
                            self.image_2.pixmap().height())

        img1_x1, img1_y1 = self.fixBounds(
            img1_x1, img1_y1, max_img_width, max_img_height)

        img1_x2, img1_y2 = self.fixBounds(
            img1_x2, img1_y2, max_img_width, max_img_height)

        img2_x, img2_y = self.fixBounds(
            img2_x, img2_y,self.image_2.pixmap().width(),  self.image_2.pixmap().height())

        selection_pixmap = self.image_1.last_selection
        if selection_pixmap != None:
            sel_x1, sel_y1 = self.image_1.last_selection_begin.x(),self.image_1.last_selection_begin.y()
            sel_x2, sel_y2 = self.image_1.last_selection_end.x(), self.image_1.last_selection_end.y()
        
            if (img1_x1 != sel_x1 or img1_y1 != sel_y1 or img1_x2 != sel_x2 or img1_y2 != sel_y2):
                self.image_1.clearLastSelection()
                img1_x1, img1_y1, img1_x2, img1_y2 = self.getCorrectedCoords(
                    img1_x1, img1_y1, img1_x2, img1_y2)
                selection_pixmap = self.image_1.pixmap().copy(QRect(QPoint(img1_x1,img1_y1),QPoint(img1_x2+1,img1_y2+1)))
        else:
            img1_x1, img1_y1, img1_x2, img1_y2 = self.getCorrectedCoords(
                img1_x1, img1_y1, img1_x2, img1_y2)
            selection_pixmap = self.image_1.pixmap().copy(
                QRect(QPoint(img1_x1, img1_y1), QPoint(img1_x2+1, img1_y2+1)))
        
        painter = QPainter(self.result_image.pixmap())
        painter.drawPixmap(img2_x,img2_y,selection_pixmap)
        painter.end()
        self.result_image.update()
      



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

    def loadImage1Tab2(self):
            # TODO: antes era self.pixmap, nose para que se usa
            pixmap = openImage()
            if pixmap == None:
                return
            # self.btn_load.deleteLater()
            if self.image_1 == None:
                self.image_1 = QSelectionableLabel(self.scroll_area_contents_img_1)
                self.scroll_area_contents_img_1.layout().addWidget(self.image_1)
                self.image_1.selection_handler = self.copySelectionHandler

            #self.image_1.mousePressEvent = self.handleImgClick
            #self.image_1.mouseReleaseEvent = self.handleImgRelease
            self.image_1.setPixmap(pixmap)
            self.image_1.adjustSize()

            self.scroll_area_img_1.installEventFilter(self)

    def loadImage2Tab2(self):
        # TODO: antes era self.pixmap, nose para que se usa
        pixmap = openImage()
        if pixmap == None:
            return
        # self.btn_load.deleteLater()
        if self.image_2 == None:
            self.image_2 = QLabel(self.scroll_area_contents_img_2)
            self.scroll_area_contents_img_2.layout().addWidget(self.image_2)
            self.image_2.mousePressEvent = self.copyClickHandler
            
            

        self.image_2.setPixmap(pixmap)
        self.image_2.adjustSize()
        if self.result_image == None:
                self.result_image = QLabel(self.scroll_area_contents_result)
                self.scroll_area_contents_result.layout().addWidget(self.result_image)

        self.result_image.setPixmap(self.image_2.pixmap())

        #self.image_2.mousePressEvent = self.handleImgClick
        #self.image_2.mouseReleaseEvent = self.handleImgRelease
        #self.original_image.paintEvent = self.paintEventLbl

        self.scroll_area_img_2.installEventFilter(self)

    def saveTab2(self):
        if self.result_image != None:
            pixmap = self.result_image.pixmap()
            if pixmap != None:
                saveImage(self,pixmap)
        ####################### IMAGE OPERATIONS HANDLER

    def sum_imgs(self):
        if self.image_1 == None or self.image_2 == None:
            return
        result = operate(self.image_1.pixmap().toImage(),
                            self.image_2.pixmap().toImage(), OperationsEnum.SUMA)

        self.result_image.setPixmap(QPixmap.fromImage(result))

    def substract_imgs(self):
        if self.image_1 == None or self.image_2 == None:
            return
        result = operate(self.image_1.pixmap().toImage(),
                            self.image_2.pixmap().toImage(), OperationsEnum.RESTA)

        self.result_image.setPixmap(QPixmap.fromImage(result))

    def multiply_imgs(self):
        if self.image_1 == None or self.image_2 == None:
            return
        result = operate(self.image_1.pixmap().toImage(
        ), self.image_2.pixmap().toImage(), OperationsEnum.MULTIPLICACION)

        self.result_image.setPixmap(QPixmap.fromImage(result))

    def onCloseEvent(self,event):
        if self.image_1:
            self.image_1.painter.end()
      