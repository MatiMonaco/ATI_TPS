from PyQt5 import  QtWidgets,QtCore,QtGui
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QColor
from components.QSelectionableLabel import QSelectionableLabel
from PyQt5.QtWidgets import   QLabel, QWidget, QScrollArea
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from libs.TP0.img_operations import openImage, saveImage
from components.tabs.tab import Tab
import resources.resources as resources
from filters.object_detection.active_contour import ActiveContour 
import qimage2ndarray
from PyQt5.QtGui import QPixmap
class ObjectDetectionTab(Tab):

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.selectedPxlX = None
        self.selectedPxlY = None
        self.last_time_move_X = 0
        self.last_time_move_Y = 0

        self.video_label = None
        self.video_states = []
        self.active_countour = ActiveContour()

        self.current_state = 0
    


    def videoClickHandler(self, label):
        #x,y = label.begin.x(),label.begin.y()
        label.clearLastSelection()
        

    def videoSelectionHandler(self,label):
        print(f"Sup Left Point: ({label.last_selection_begin.x()},{label.last_selection_begin.y()})")
        print(f"Inf Right Point: ({label.last_selection_end.x()},{label.last_selection_end.y()})")
        self.active_countour.setSupLeftPoint(label.last_selection_begin)
        self.active_countour.setInfRightPoint(label.last_selection_end)

   
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

                vert_scroll_bar.setValue(int(self.interpolate(
                    event.pos().y(), 0, source.height(), 0, vert_scroll_bar.maximum())))
                self.last_time_move_Y = event.pos().y()

                hor_scroll_bar.setValue(int(self.interpolate(
                    event.pos().x(), 0, source.width(), 0, hor_scroll_bar.maximum())))
                self.last_time_move_X = event.pos().x()

        elif event.type() == QEvent.MouseButtonRelease:

            if type(source) == QScrollArea:
                self.last_time_move_X = 0
                self.last_time_move_Y = 0
        return QWidget.eventFilter(self, source, event)



    ##################### ACTIONS ####################

    def saveState(self):
        pixmap = self.video_label.pixmap()
        self.video_states.append(
            pixmap.copy(0, 0, pixmap.width(), pixmap.height()))

    def clearStates(self):
        self.video_states = []
    
    def process(self):
        img = self.video_label.pixmap().toImage()
        self.saveState()
        new_img = self.active_countour.applyFilter(img,img.isGrayscale())
        self.video_label.setPixmap(new_img)

    def prev(self):
     
        if(not self.video_states) or self.current_state == 0:
            return
        self.current_state-=1
        last_pixmap = self.video_states[self.current_state]
        self.video_label.setPixmap(last_pixmap)

    def next(self):
     
        if(not self.video_states) or self.current_state == (len(self.video_states)-1):
            return
        self.current_state+=1
        next_pixmap = self.video_states[self.current_state]
        self.video_label.setPixmap(next_pixmap)
      

    def loadVideo(self):
        pixmap = openImage()
        if pixmap == None:
            return

        img = pixmap.toImage()

        if self.video_label == None:
            self.video_label = QSelectionableLabel(
                self.scroll_area_contents_video)
            self.scroll_area_contents_video.layout().addWidget(self.video_label)
            self.scroll_area_video.installEventFilter(self)
            self.video_label.click_handler = self.videoClickHandler
            self.video_label.selection_handler = self.videoSelectionHandler

        self.clearStates()

        self.video_label.setPixmap(pixmap)

        self.video_label.adjustSize()
     

   

    ###########################################################################################################################
    def setupUI(self):
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.video_HLayout = QtWidgets.QHBoxLayout()
        self.video_HLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.video_HLayout.setContentsMargins(0, -1, 0, -1)
        self.video_HLayout.setSpacing(6)
        self.video_HLayout.setObjectName("video_HLayout")
        self.scroll_area_video = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area_video.sizePolicy().hasHeightForWidth())
        self.scroll_area_video.setSizePolicy(sizePolicy)
        self.scroll_area_video.setAcceptDrops(True)
        self.scroll_area_video.setWidgetResizable(True)
        self.scroll_area_video.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area_video.setObjectName("scroll_area_video")
        self.scroll_area_contents_video = QtWidgets.QWidget()
        self.scroll_area_contents_video.setGeometry(QtCore.QRect(458, 302, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area_contents_video.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_video.setSizePolicy(sizePolicy)
        self.scroll_area_contents_video.setObjectName("scroll_area_contents_video")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scroll_area_contents_video)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scroll_area_video.setWidget(self.scroll_area_contents_video)
        self.video_HLayout.addWidget(self.scroll_area_video)
        self.video_HLayout.setStretch(0, 3)
        self.verticalLayout_2.addLayout(self.video_HLayout)
        self.frame_info_HLayout = QtWidgets.QHBoxLayout()
        self.frame_info_HLayout.setObjectName("frame_info_HLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.frame_info_HLayout.addItem(spacerItem)
        self.frame_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame_label.setFont(font)
        self.frame_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.frame_label.setIndent(10)
        self.frame_label.setText("Frame = 0")
        self.frame_info_HLayout.addWidget(self.frame_label)
        self.frame_info_HLayout.setStretch(0, 8)
        self.frame_info_HLayout.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.frame_info_HLayout)
        self.actions_group_box = QtWidgets.QGroupBox(self)
        self.actions_group_box.setObjectName("actions_group_box")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.actions_group_box)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.actions_HLayout = QtWidgets.QHBoxLayout()
        self.actions_HLayout.setObjectName("actions_HLayout")
        self.btn_prev = QtWidgets.QPushButton(self.actions_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_prev.sizePolicy().hasHeightForWidth())
        self.btn_prev.setSizePolicy(sizePolicy)
        self.btn_prev.setText("<")
        self.btn_prev.clicked.connect(self.prev)
        self.actions_HLayout.addWidget(self.btn_prev)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.actions_HLayout.addItem(spacerItem1)
        self.btn_play = QtWidgets.QPushButton(self.actions_group_box)
        self.btn_play.setText("Play")
        self.actions_HLayout.addWidget(self.btn_play)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.actions_HLayout.addItem(spacerItem2)
        self.btn_next = QtWidgets.QPushButton(self.actions_group_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_next.sizePolicy().hasHeightForWidth())
        self.btn_next.setSizePolicy(sizePolicy)
        self.btn_next.setText(">")
        self.btn_next.clicked.connect(self.next)
        self.actions_HLayout.addWidget(self.btn_next)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.actions_HLayout.addItem(spacerItem3)
        self.btn_process = QtWidgets.QPushButton(self.actions_group_box)
        self.btn_process.setText("Process")
        self.btn_process.clicked.connect(self.process)
        self.actions_HLayout.addWidget(self.btn_process)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.actions_HLayout.addItem(spacerItem4)
        self.btn_load_video = QtWidgets.QPushButton(self.actions_group_box)
        self.btn_load_video.setText("Load")
        self.btn_load_video.clicked.connect(self.loadVideo)
        self.actions_HLayout.addWidget(self.btn_load_video)
        self.btn_save_video = QtWidgets.QPushButton(self.actions_group_box)
        self.btn_save_video.setText("Save")
        self.actions_HLayout.addWidget(self.btn_save_video)
        self.actions_HLayout.setStretch(0, 1)
        self.actions_HLayout.setStretch(4, 1)
        self.actions_HLayout.setStretch(6, 1)
        self.actions_HLayout.setStretch(7, 4)
        self.verticalLayout_15.addLayout(self.actions_HLayout)
        self.verticalLayout_2.addWidget(self.actions_group_box)
        self.verticalLayout_2.setStretch(0, 3)
