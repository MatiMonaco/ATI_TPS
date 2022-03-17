from PyQt5.QtWidgets import QTabWidget, QLabel, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QIntValidator
from widgets.abstract_tab import AbstractTab
from libs.TP0.img_operations import operate 
from PyQt5 import QtWidgets, QtCore
from PIL import ImageQt

### TAB 2 ###
class OperationsTab(QWidget):
    # def __init__(self, parent: None) -> None:
    #     super().__init__(parent)
        
    #     self.image_1 = None
    #     self.image_2 = None
    #     self.result_image = None

        # self.btn_copy_img.triggered.connect(self.copyToAnotherImage)
        # self.btn_sum_imgs.clicked.connect(self.sum_imgs)
        # self.btn_substract_imgs.clicked.connect(self.substract_imgs)
        # self.btn_multiply_imgs.clicked.connect(self.multiply_imgs)
        # self.btn_load_1.clicked.connect(self.loadImage1)
        # self.btn_load_2.clicked.connect(self.loadImage2)
        # self.btn_res_save.clicked.connect(self.saveTab)
        # self.btn_copy.clicked.connect(self.copyToAnotherImage)

    def __init__(self, *args, **kwargs):
        super(OperationsTab, self).__init__(*args, **kwargs)
        self.__init_elems__()
        # QTabWidget.__init__(self, args, kwargs)  
         
        self.image_1 = None
        self.image_2 = None
        self.result_image = None
        # self.btn_copy_img.triggered.connect(self.copyToAnotherImage)
        self.btn_sum_imgs.clicked.connect(self.sum_imgs)
        self.btn_substract_imgs.clicked.connect(self.substract_imgs)
        self.btn_multiply_imgs.clicked.connect(self.multiply_imgs)
        self.btn_load_1.clicked.connect(self.loadImage1)
        self.btn_load_2.clicked.connect(self.loadImage2)
        self.btn_res_save.clicked.connect(self.saveTab)
        self.btn_copy.clicked.connect(self.copyToAnotherImage)
        
        self.onlyInt = QIntValidator()

        self.txt_x_img1.setValidator(self.onlyInt)
        self.txt_y_img1.setValidator(self.onlyInt)
        self.txt_x_img2.setValidator(self.onlyInt)
        self.txt_y_img2.setValidator(self.onlyInt)
        self.txt_x_img3.setValidator(self.onlyInt)
        self.txt_y_img3.setValidator(self.onlyInt)
    ####################### OPERATIONS ##############################
    def sum_imgs(self):
        img3 = operate(self.path_img1, self.path_img2, 'sum')

    def substract_imgs(self):
        img3 = operate(self.path_img1, self.path_img2, 'substract')
     
    def multiply_imgs(self):
        img3 = operate(self.path_img1, self.path_img2, 'multiply')

    def loadImage1(self):
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

    def loadImage2(self):
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

    def saveTab(self):
        pixmap = self.result_image.pixmap()
        if pixmap != None:
            self.saveImage(pixmap)

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
        
    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        if imagePath == None or imagePath == "":
            return None

        pixmap = QPixmap()
        pixmap.loadFromData(open(imagePath, "rb").read())

        return pixmap, imagePath

    def saveImage(self,pixmap):
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "Images (*.png *.xpm *.jpg *.nef)", "")

        file = open(fileName, 'w')
        image = ImageQt.fromqpixmap(pixmap)
        print(f'LOG: saved filtered image to {file.name}')
        image.save(file.name)



    ############################################################################
    def __init_elems__(self):
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.scroll_area_img_2 = QtWidgets.QScrollArea(self)
        self.scroll_area_img_2.setWidgetResizable(True)
        self.scroll_area_img_2.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area_img_2.setObjectName("scroll_area_img_2")
        self.scroll_area_contents_img_2 = QtWidgets.QWidget()
        self.scroll_area_contents_img_2.setGeometry(QtCore.QRect(112, 76, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area_contents_img_2.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_img_2.setSizePolicy(sizePolicy)
        self.scroll_area_contents_img_2.setObjectName("scroll_area_contents_img_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.scroll_area_contents_img_2)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.scroll_area_img_2.setWidget(self.scroll_area_contents_img_2)
        self.gridLayout.addWidget(self.scroll_area_img_2, 3, 1, 1, 1)
        self.scroll_area_img_1 = QtWidgets.QScrollArea(self)
        self.scroll_area_img_1.setWidgetResizable(True)
        self.scroll_area_img_1.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area_img_1.setObjectName("scroll_area_img_1")
        self.scroll_area_contents_img_1 = QtWidgets.QWidget()
        self.scroll_area_contents_img_1.setGeometry(QtCore.QRect(112, 76, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area_contents_img_1.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_img_1.setSizePolicy(sizePolicy)
        self.scroll_area_contents_img_1.setObjectName("scroll_area_contents_img_1")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.scroll_area_contents_img_1)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.scroll_area_img_1.setWidget(self.scroll_area_contents_img_1)
        self.gridLayout.addWidget(self.scroll_area_img_1, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        self.btn_load_2 = QtWidgets.QPushButton(self)
        self.btn_load_2.setStyleSheet("b")
        self.btn_load_2.setObjectName("btn_load_2")
        self.btn_load_2.setText("Load Image")
        self.gridLayout.addWidget(self.btn_load_2, 3, 0, 1, 1)
        self.btn_load_1 = QtWidgets.QPushButton(self)
        self.btn_load_1.setObjectName("btn_load_1")
        self.btn_load_1.setText("Load Image")
        self.gridLayout.addWidget(self.btn_load_1, 1, 0, 1, 1)
        self.gridLayout.setColumnStretch(1, 6)
        self.gridLayout.setRowStretch(1, 5)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 5)
        self.horizontalLayout_8.addLayout(self.gridLayout)
        self.scroll_area_result = QtWidgets.QScrollArea(self)
        self.scroll_area_result.setWidgetResizable(True)
        self.scroll_area_result.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area_result.setObjectName("scroll_area_result")
        self.scroll_area_contents_result = QtWidgets.QWidget()
        self.scroll_area_contents_result.setGeometry(QtCore.QRect(172, 181, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area_contents_result.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_result.setSizePolicy(sizePolicy)
        self.scroll_area_contents_result.setObjectName("scroll_area_contents_result")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scroll_area_contents_result)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scroll_area_result.setWidget(self.scroll_area_contents_result)
        self.horizontalLayout_8.addWidget(self.scroll_area_result)
        self.horizontalLayout_8.setStretch(0, 5)
        self.horizontalLayout_8.setStretch(1, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btn_sum_imgs = QtWidgets.QPushButton(self)
        self.btn_sum_imgs.setObjectName("btn_sum_imgs")
        self.btn_sum_imgs.setText("SUM")
        self.verticalLayout_6.addWidget(self.btn_sum_imgs)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.btn_substract_imgs = QtWidgets.QPushButton(self)
        self.btn_substract_imgs.setObjectName("btn_substract_imgs")
        self.btn_substract_imgs.setText("SUBSTRACT")
        self.verticalLayout_7.addWidget(self.btn_substract_imgs)
        self.horizontalLayout_5.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.btn_multiply_imgs = QtWidgets.QPushButton(self)
        self.btn_multiply_imgs.setObjectName("btn_multiply_imgs")
        self.btn_multiply_imgs.setText("MULTIPLY")
        self.verticalLayout_8.addWidget(self.btn_multiply_imgs)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)
        self.btn_reset_operations = QtWidgets.QPushButton(self)
        self.btn_reset_operations.setObjectName("btn_reset_operations")
        self.btn_reset_operations.setText("RESET")
        self.horizontalLayout_5.addWidget(self.btn_reset_operations)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label = QtWidgets.QLabel(self)
        self.label.setMinimumSize(QtCore.QSize(102, 0))
        self.label.setMaximumSize(QtCore.QSize(102, 102))
        self.label.setObjectName("label")
        self.label.setText("COPY FROM")
        self.horizontalLayout_9.addWidget(self.label)
        self.line = QtWidgets.QFrame(self)
        self.line.setStyleSheet("color:white;")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_9.addWidget(self.line)
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("x1")
        self.horizontalLayout_9.addWidget(self.label_4)
        self.txt_x_img1 = QtWidgets.QLineEdit(self)
        self.txt_x_img1.setMinimumSize(QtCore.QSize(0, 0))
        self.txt_x_img1.setObjectName("txt_x_img1")
        self.horizontalLayout_9.addWidget(self.txt_x_img1)
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("x2")
        self.horizontalLayout_9.addWidget(self.label_5)
        self.txt_y_img1 = QtWidgets.QLineEdit(self)
        self.txt_y_img1.setObjectName("txt_y_img1")
        self.horizontalLayout_9.addWidget(self.txt_y_img1)
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_9.addWidget(self.line_2)
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("x2")
        self.horizontalLayout_9.addWidget(self.label_3)
        self.txt_x_img2 = QtWidgets.QLineEdit(self)
        self.txt_x_img2.setObjectName("txt_x_img2")
        self.horizontalLayout_9.addWidget(self.txt_x_img2)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("y2")
        self.horizontalLayout_9.addWidget(self.label_2)
        self.txt_y_img2 = QtWidgets.QLineEdit(self)
        self.txt_y_img2.setObjectName("txt_y_img2")
        self.horizontalLayout_9.addWidget(self.txt_y_img2)
        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(3, 1)
        self.horizontalLayout_9.setStretch(5, 1)
        self.horizontalLayout_9.setStretch(8, 1)
        self.horizontalLayout_9.setStretch(10, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setMinimumSize(QtCore.QSize(102, 0))
        self.label_8.setMaximumSize(QtCore.QSize(102, 16777215))
        self.label_8.setObjectName("label_8")
        self.label_8.setText("COPY TO")
        self.horizontalLayout_10.addWidget(self.label_8)
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_10.addWidget(self.line_3)
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setMaximumSize(QtCore.QSize(20, 10))
        self.label_6.setObjectName("label_6")
        self.label_6.setText("x")
        self.horizontalLayout_10.addWidget(self.label_6)
        self.txt_x_img3 = QtWidgets.QLineEdit(self)
        self.txt_x_img3.setObjectName("txt_x_img3")
        self.horizontalLayout_10.addWidget(self.txt_x_img3)
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setObjectName("label_7")
        self.label_7.setText("y")
        self.horizontalLayout_10.addWidget(self.label_7)
        self.txt_y_img3 = QtWidgets.QLineEdit(self)
        self.txt_y_img3.setObjectName("txt_y_img3")
        self.horizontalLayout_10.addWidget(self.txt_y_img3)
        self.line_4 = QtWidgets.QFrame(self)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_10.addWidget(self.line_4)
        self.btn_copy = QtWidgets.QPushButton(self)
        self.btn_copy.setObjectName("btn_copy")
        self.btn_copy.setText("COPY")
        self.horizontalLayout_10.addWidget(self.btn_copy)
        self.btn_res_save = QtWidgets.QPushButton(self)
        self.btn_res_save.setObjectName("btn_res_save")
        self.btn_res_save.setText("SAVE")
        self.horizontalLayout_10.addWidget(self.btn_res_save)
        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(3, 1)
        self.horizontalLayout_10.setStretch(5, 1)
        self.horizontalLayout_10.setStretch(7, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_10)