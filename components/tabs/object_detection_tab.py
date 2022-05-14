from time import process_time_ns, sleep
import threading
import os
import re
from zipfile import ZipFile

import numpy as np
import qimage2ndarray
import math
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QScrollArea, QFileDialog,QLabel
from PyQt5.QtGui import QPixmap

from components.QSelectionableLabel import QSelectionableLabel
from components.tabs.tab import Tab
from filters.object_detection.active_contour import ActiveContour
from libs.TP0.img_operations import imageToPixmap
from PyQt5.QtGui import QIntValidator
LIN_IDX = 0
LOUT_IDX = 1

PLAY = 0
PAUSE = 1


class ObjectDetectionTab(Tab):

    def __init__(self):
        super().__init__()
        self.icons = {"play": QIcon('resources/play.png'), "pause": QIcon('resources/pause.png'), "back": QIcon('resources/back.png'),
                      "next": QIcon('resources/next.png'), "start": QIcon('resources/start.png'), "end": QIcon('resources/end.png')}

        self.selectedPxlX = None
        self.selectedPxlY = None
        self.last_time_move_X = 0
        self.last_time_move_Y = 0
        self.video_label = None
        self.phi_label = None
        self.active_countour = ActiveContour()
        self.FPS = 60
        # self.frames_iterations = None
        # self.object_iterations = None
        # self.current_frame = 0
        self.current_frame_arr = None
        self.total_frames = 0
        self.frames = None
        self.reproduction_state = PAUSE
        self.reproduction_state_lock = threading.Lock()
        self.current_iteration = 0
        self.total_iterations = None
    
        self.play_it_thread = None
        self.play_frame_thread = None
        self.pause_event = threading.Event()
        self.img_width = None
        self.img_height = None
        
        self.frames_iterations = list()
        self.object_iterations = list()
        self.current_frame = 0

        self.setupUI()

    def reset(self):
        self.active_countour.reset()
        self.current_iteration = 0
        self.current_frame = 0
        self.frames_iterations = list()
        self.object_iterations = list()
        self.elapsed_times = list()
        self.reproduction_state = PAUSE
        self.set_current_frame(clear=True)
        self.set_current_iteration(clear=True)

        if self.frames:
            first_frame = self.frames[0]
            self.change_pixmaps(first_frame,np.zeros((first_frame.shape[0],first_frame.shape[1],3)))
            self.video_label.adjustSize()
            

    def videoClickHandler(self, label):
        #x,y = label.begin.x(),label.begin.y()
        label.clearLastSelection()

    def videoSelectionHandler(self, label):
        print(
            f"Sup Left Point: ({label.last_selection_begin.x()},{label.last_selection_begin.y()})")
        print(
            f"Inf Right Point: ({label.last_selection_end.x()},{label.last_selection_end.y()})")
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

    def onCloseEvent(self, event):
        if self.video_label:
            self.video_label.painter.end()

    ##################### ACTIONS ####################

    def draw_borders(self, img_arr, LIns, LOuts):

        img_arr[LIns[:, 0], LIns[:, 1]] = np.array([255, 0, 0])

        img_arr[LOuts[:, 0], LOuts[:, 1]] = np.array([0, 0, 255])

        return img_arr

    def process(self, draw_last: bool=False):
        elapsed = 0
        if self.video_label is not None and self.total_frames > 0 and self.current_frame < self.total_frames:
            self.video_label.clearLastSelection()
            if not self.is_processed(self.current_frame):
                print(f"Processing frame {self.current_frame + 1}/{self.total_frames}")

                start = process_time_ns()
                frame_img_arr =self.frames[self.current_frame]

                iterations_limits,iteration_objects = self.active_countour.applyAll(frame_img_arr)
                elapsed = process_time_ns() - start
                
                self.frames_iterations.append(iterations_limits)
                self.object_iterations.append(iteration_objects)
                self.elapsed_times.append(elapsed)
                self.set_elapsed_time(elapsed=elapsed)
            self.draw_frame(None if draw_last else 0)
        return elapsed

    # def process_in_real_time(self):
   
    #     if self.video_label is not None and self.total_frames > 0:

    #         self.video_label.clearLastSelection()
    #         self.frames_iterations = list()
    #         self.object_iterations = list()
    #         self.active_countour.init()
    #         for frame in range(self.total_frames):
    #             print(f"Processing frame {frame}/{self.total_frames}")
    #             frame_img_arr =self.frames[frame]
    #             i = 0
    #             iterations_limits = []
    #             iterations_objects = []
    #             self.set_current_frame()
    #             while i < self.active_countour.max_iter and not self.active_countour.end_condition(frame_img_arr):
    #                 self.active_countour.update_edges(frame_img_arr)
                    
    #                 iteration_limits,iteration_objects = self.active_countour.apply(frame_img_arr)
        
    #                 iterations_limits.append(iteration_limits)     # draw all iterations figures
    #                 iterations_objects.append(iteration_objects)
    #                 # self.plot_phi_mask(self.phi_mask)
    #                 i += 1

    #             if i < self.active_countour.max_iter:
    #                 print(f"END CONDITION MET with i={i}")

    #             self.frames_iterations.append(iterations_limits)
    #             self.object_iterations.append(iterations_objects)

    #         self.current_frame = 0
    #         self.draw_frame(0)

    def change_pixmaps(self, img_arr,phi_mask_arr):
        self.video_label.setPixmap(QPixmap.fromImage(
            qimage2ndarray.array2qimage(img_arr)))
        self.phi_label.setPixmap(QPixmap.fromImage(
            qimage2ndarray.array2qimage(phi_mask_arr)))
       
      
    def set_elapsed_time(self, elapsed: int, clear: bool=True):
        self.it_label.setText("" if clear else
            f"Processing time {elapsed/1000000} ms")
        
    ################ video controls ##################

    IMG_NAME_PATT = "[a-zA-Z]*([0-9]+)\.(png|jpg|jpeg|ppm|pgm|raw)"

    def openImageOrZip(self):
        '''
            Retorna un array de pixmaps de imagenes.
            - Si es un ZIP, extrae las imagenes y retorna las imagenes
            en order segun el nombre img{number}.ext
            - Si es una imagen sola retorna la imagen
        '''
        path, _ = QFileDialog.getOpenFileName()
        if path is None or path == "":
            return
        split_path = os.path.splitext(path)
        file_extension = split_path[1]
        if file_extension.lower() == ".zip":
            imgs = []
            with ZipFile(path, mode='r') as zip:
                for img in zip.namelist():
                    res = re.match(
                        ObjectDetectionTab.IMG_NAME_PATT, img, re.IGNORECASE)
                    if res:
                        num = int(res.group(1))
                        pixmap = QPixmap()
                        pixmap.loadFromData(zip.read(img))
                        imgs.append((num, pixmap))
            imgs = sorted(imgs, key=lambda img: img[0])
            return list(map(lambda img: img[1], imgs))
        else:
            return [imageToPixmap(path)]

    def loadVideo(self):

        pixmaps = self.openImageOrZip()
        if pixmaps == None:
            return

        if self.video_label == None:
            self.video_label = QSelectionableLabel(
                self.scroll_area_contents_video)
            self.scroll_area_contents_video.layout().addWidget(self.video_label)
            self.scroll_area_video.installEventFilter(self)
            self.video_label.click_handler = self.videoClickHandler
            self.video_label.selection_handler = self.videoSelectionHandler
            self.phi_label = QLabel(self.scroll_area_contents_phi)
            self.scroll_area_contents_phi.layout().addWidget(self.phi_label)
  
        self.frames = list(map(lambda pmap: qimage2ndarray.rgb_view(pmap.toImage()).astype("int32"), pixmaps))
        self.total_frames = len(self.frames)
   
        self.reset()
        self.img_width = self.video_label.width()
        self.img_height = self.video_label.height()

    def thread_play_frame(self):
        if not self.is_processed(self.current_frame):
            self.current_frame -= 1

        time_between_frames = 1000/self.FPS
        while self.current_frame < self.total_frames:
        # for frame in range(self.current_frame, self.total_frames):

            if self.pause_event.is_set():
                self.pause_event.clear()
                break
            self.current_frame += 1
            elapsed = self.process(draw_last=True)
            wait = time_between_frames - elapsed/1000000
            if wait < 0:
                continue
            sleep(wait/1000)
        self.current_frame = self.total_frames - 1 if self.current_frame == self.total_frames else self.current_frame
        with self.reproduction_state_lock:
            self.reproduction_state = PAUSE
            self.btn_play.setIcon(self.icons["play"])

    def play_frame(self):
        if self.frames_iterations is not None:
            if self.current_frame != (self.total_frames-1):
                with self.reproduction_state_lock:
                    if self.reproduction_state != PLAY:
                        self.reproduction_state = PLAY
                        self.btn_play.setIcon(self.icons["pause"])
                        self.play_frame_thread = threading.Thread(
                            target=self.thread_play_frame, daemon=True)
                        self.play_frame_thread.start()
                    else:
                        self.reproduction_state = PAUSE
                        self.pause_event.set()
                        self.btn_play.setIcon(self.icons["play"])

    def is_processed(self, frame: int) -> bool:
        return len(self.frames_iterations) - 1 >= frame
    
    def next_frame(self):
        if self.frames_iterations is not None:
            with self.reproduction_state_lock:
                if self.reproduction_state != PLAY:

                    if self.current_frame == (self.total_frames-1):
                        return
                    self.current_frame += 1
                    if not self.is_processed(self.current_frame):
                        print("processing")
                        self.process()
                    self.draw_frame(0)

    def prev_frame(self):
        if self.frames_iterations is not None:
            with self.reproduction_state_lock:
                if self.reproduction_state != PLAY:
                    if self.current_frame == 0:
                        return
                    self.current_frame -= 1
                    self.draw_frame(0)

    def draw_frame(self, iteration=None):

        self.current_frame_arr = self.frames[self.current_frame]
        self.total_iterations = len(self.frames_iterations[self.current_frame])
        self.current_iteration = self.total_iterations -  1 if iteration is None else iteration
        self.set_current_frame()
        self.draw_iteration()

    def set_current_frame(self, clear: bool=False):
        self.frame_label.setText("" if clear else
            f"Frame {self.current_frame+1}/{self.total_frames}")

    def go_last_processed_frame(self):
        if self.frames_iterations is not None:
            with self.reproduction_state_lock:
                if self.reproduction_state != PLAY:

                    self.current_frame = len(self.frames_iterations) - 1
                    self.draw_frame()

    def go_start_frame(self):
        if self.frames_iterations is not None:
            with self.reproduction_state_lock:
                if self.reproduction_state != PLAY:
                    self.current_frame = 0
                    self.draw_frame()

    ################ iteration controls ################

    def thread_play_it(self):

        time_between_frames = 1000/self.FPS
        for iteration in range(self.current_iteration, self.total_iterations):

            if self.pause_event.is_set():
                self.pause_event.clear()
                break
            start = process_time_ns()
            self.current_iteration = iteration
            self.draw_iteration()
            elapsed = process_time_ns() - start
            wait = time_between_frames - elapsed/1000000
            if wait < 0:
                continue
            sleep(wait/1000)
        with self.reproduction_state_lock:
            self.reproduction_state = PAUSE
            self.btn_it_play.setIcon(self.icons["play"])

    def play_it(self):
        if self.frames_iterations is not None:
            total_iterations = len(self.frames_iterations[self.current_frame])
            if self.current_iteration != (total_iterations-1):
                with self.reproduction_state_lock:
                    if self.reproduction_state != PLAY:
                        self.reproduction_state = PLAY
                        self.btn_it_play.setIcon(self.icons["pause"])
                        self.play_it_thread = threading.Thread(
                            target=self.thread_play_it, daemon=True)
                        self.play_it_thread.start()
                    else:
                        self.reproduction_state = PAUSE
                        self.pause_event.set()
                        self.btn_it_play.setIcon(self.icons["play"])

    def next_it(self):
        if self.frames_iterations is not None:
            with self.reproduction_state_lock:
                if self.reproduction_state != PLAY:

                    if self.current_iteration == (self.total_iterations-1):
                        return
                    self.current_iteration += 1
                    self.draw_iteration()

    def prev_it(self):
        if self.frames_iterations is not None:
            with self.reproduction_state_lock:
                if self.reproduction_state != PLAY:
                    if self.current_iteration == 0:
                        return
                    self.current_iteration -= 1
                    self.draw_iteration()

    def draw_iteration(self):

        limits = self.frames_iterations[self.current_frame][self.current_iteration]
        borders_image = self.draw_borders(
            np.copy(self.current_frame_arr), limits[LIN_IDX], limits[LOUT_IDX])
        phi_mask = self.draw_borders(
            np.zeros((self.img_height,self.img_width,3)), limits[LIN_IDX], limits[LOUT_IDX])
        phi_mask = self.draw_object(phi_mask,self.object_iterations[self.current_frame][self.current_iteration])
        self.change_pixmaps(borders_image,phi_mask)
        self.set_current_iteration()
    
    def draw_object(self,img_arr,object_idx):
       
        img_arr[object_idx[:,0],object_idx[:,1]] = self.active_countour.object_thetas
        return img_arr

    def set_current_iteration(self, clear: bool=False):
        self.it_label.setText("" if clear else
            f"Iteration {self.current_iteration+1}/{len(self.frames_iterations[self.current_frame])}")

    def go_end_it(self):
        if self.frames_iterations is not None:
            with self.reproduction_state_lock:
                if self.reproduction_state != PLAY:

                    self.current_iteration = (self.total_iterations-1)
                    self.draw_iteration()

    def go_start_it(self):
        if self.frames_iterations is not None:
            with self.reproduction_state_lock:
                if self.reproduction_state != PLAY:

                    self.current_iteration = 0
                    self.draw_iteration()

    ###########################################################################################################################

    def setupUI(self):

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.titles_HLayout = QtWidgets.QHBoxLayout()
        self.titles_HLayout.addItem(QtWidgets.QSpacerItem( 20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.video_title = QtWidgets.QLabel(self)
        self.video_title.setStyleSheet("font-weight:bold;font-size:14px;")
        self.video_title.setText("Video")
      

        self.titles_HLayout.addWidget(self.video_title)
        self.titles_HLayout.addItem(QtWidgets.QSpacerItem( 20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.phi_mask_title = QtWidgets.QLabel(self)
        self.phi_mask_title.setStyleSheet("font-weight:bold;font-size:14px;")
        self.phi_mask_title.setText(
            "<html><head/><body><span>&phi; mask parts</span></body></html>")
      

        self.titles_HLayout.addWidget(self.phi_mask_title)
        self.titles_HLayout.addItem(QtWidgets.QSpacerItem( 20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.titles_HLayout.setStretch(0,2)
        self.titles_HLayout.setStretch(2,5)
        self.titles_HLayout.setStretch(4,2)
        self.verticalLayout_2.addLayout( self.titles_HLayout)
        self.video_HLayout = QtWidgets.QHBoxLayout()
        self.video_HLayout.setSizeConstraint(
            QtWidgets.QLayout.SetMinAndMaxSize)
        self.video_HLayout.setContentsMargins(0, -1, 0, -1)
        self.video_HLayout.setSpacing(6)
      
        # Video
        self.scroll_area_video = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_video.sizePolicy().hasHeightForWidth())
        self.scroll_area_video.setSizePolicy(sizePolicy)
        self.scroll_area_video.setAcceptDrops(True)
        self.scroll_area_video.setWidgetResizable(True)
        self.scroll_area_video.setAlignment(QtCore.Qt.AlignCenter)
 
        self.scroll_area_contents_video = QtWidgets.QWidget()
        self.scroll_area_contents_video.setGeometry(
            QtCore.QRect(458, 302, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_contents_video.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_video.setSizePolicy(sizePolicy)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(
            self.scroll_area_contents_video)
     
        self.scroll_area_video.setWidget(self.scroll_area_contents_video)


        # Phi
        self.scroll_area_phi = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_video.sizePolicy().hasHeightForWidth())
        self.scroll_area_phi.setSizePolicy(sizePolicy)
        self.scroll_area_phi.setAcceptDrops(True)
        self.scroll_area_phi.setWidgetResizable(True)
        self.scroll_area_phi.setAlignment(QtCore.Qt.AlignCenter)
 
        self.scroll_area_contents_phi = QtWidgets.QWidget()
        self.scroll_area_contents_phi.setGeometry(
            QtCore.QRect(458, 302, 18, 18))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_area_contents_phi.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents_phi.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(
            self.scroll_area_contents_phi)
        self.scroll_area_phi.setWidget(self.scroll_area_contents_phi)

        self.video_HLayout.addWidget(self.scroll_area_video)
        self.video_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.video_HLayout.addWidget(self.scroll_area_phi)
        self.video_HLayout.setStretch(0,4)

        self.video_HLayout.setStretch(2,4)
        self.verticalLayout_2.addLayout(self.video_HLayout)
        self.verticalLayout_2.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
       

        # Frame actions

        self.frame_actions_group_box = QtWidgets.QGroupBox(self)
       
        self.frame_actions_group_box.setTitle("Frame Controls")

        self.frame_actions_HLayout = QtWidgets.QHBoxLayout(
            self.frame_actions_group_box)
    

        self.btn_it_start = QtWidgets.QPushButton(self.frame_actions_group_box)
        self.btn_it_start.setIcon(self.icons["start"])
        self.btn_it_start.clicked.connect(self.go_start_it)
        self.frame_actions_HLayout.addWidget(self.btn_it_start)

        self.frame_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.btn_it_prev = QtWidgets.QPushButton(self.frame_actions_group_box)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_it_prev.sizePolicy().hasHeightForWidth())
        self.btn_it_prev.setSizePolicy(sizePolicy)
        self.btn_it_prev.setIcon(self.icons["back"])
        self.btn_it_prev.clicked.connect(self.prev_it)
        self.frame_actions_HLayout.addWidget(self.btn_it_prev)

        self.frame_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.btn_it_play = QtWidgets.QPushButton(self.frame_actions_group_box)
        self.btn_it_play.setIcon(self.icons["play"])
        self.btn_it_play.clicked.connect(self.play_it)
        self.frame_actions_HLayout.addWidget(self.btn_it_play)

        self.frame_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.btn_it_next = QtWidgets.QPushButton(self.frame_actions_group_box)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_it_next.sizePolicy().hasHeightForWidth())
        self.btn_it_next.setSizePolicy(sizePolicy)
        self.btn_it_next.setIcon(self.icons["next"])
        self.btn_it_next.clicked.connect(self.next_it)
        self.frame_actions_HLayout.addWidget(self.btn_it_next)

        self.frame_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.btn_it_end = QtWidgets.QPushButton(self.frame_actions_group_box)
        self.btn_it_end.setIcon(self.icons["end"])
        self.btn_it_end.clicked.connect(self.go_end_it)
        self.frame_actions_HLayout.addWidget(self.btn_it_end)

        self.frame_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.it_label = QtWidgets.QLabel(self.frame_actions_group_box)
        self.it_label.setStyleSheet("font-weight:bold;")
        self.it_label.setText("")
        self.frame_actions_HLayout.addWidget(self.it_label)

        self.frame_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.epsilon_label = QtWidgets.QLabel(self.frame_actions_group_box)
        self.epsilon_label.setText(
            "<html><head/><body><span>&epsilon;</span></body></html>")
        self.epsilon_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.epsilon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.frame_actions_HLayout.addWidget(self.epsilon_label)

        self.epsilon_slider = QtWidgets.QSlider(self.frame_actions_group_box)
        epsilon_max = int(math.sqrt(255**2 + 255**2 + 255**2))
        self.epsilon_slider.setMinimum(1)
        self.epsilon_slider.setMaximum(epsilon_max)
        self.epsilon_slider.setTracking(True)
        self.epsilon_slider.setOrientation(QtCore.Qt.Horizontal)
        self.frame_actions_HLayout.addWidget(self.epsilon_slider)

        self.epsilon_line_edit = QtWidgets.QLineEdit(
            self.frame_actions_group_box)
        self.epsilon_line_edit.editingFinished.connect(
            lambda: self.changeSlider(self.epsilon_line_edit.text()))
        onlyInt = QIntValidator()
        onlyInt.setBottom(1)
        onlyInt.setTop(epsilon_max)

        self.epsilon_line_edit.setValidator(onlyInt)
        self.epsilon_line_edit.setText(str(self.active_countour.epsilon))
        self.epsilon_slider.setValue(self.active_countour.epsilon)

        self.epsilon_slider.valueChanged.connect(
            lambda value: self.changeEpsilon(value))
        self.frame_actions_HLayout.addWidget(self.epsilon_line_edit)

        self.frame_actions_HLayout.setStretch(11, 4)
        self.frame_actions_HLayout.setStretch(13, 2)
        self.frame_actions_HLayout.setStretch(14, 1)
        # Video actions
        self.video_actions_group_box = QtWidgets.QGroupBox(self)

        self.video_actions_group_box.setTitle("Video Controls")

        self.video_actions_HLayout = QtWidgets.QHBoxLayout(
            self.video_actions_group_box)


        self.btn_start = QtWidgets.QPushButton(self.video_actions_group_box)
        self.btn_start.setIcon(self.icons["start"])
        self.btn_start.clicked.connect(self.go_start_frame)
        self.video_actions_HLayout.addWidget(self.btn_start)

        self.video_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.btn_prev = QtWidgets.QPushButton(self.video_actions_group_box)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_prev.sizePolicy().hasHeightForWidth())
        self.btn_prev.setSizePolicy(sizePolicy)
        self.btn_prev.setIcon(self.icons["back"])
        self.btn_prev.clicked.connect(self.prev_frame)
        self.video_actions_HLayout.addWidget(self.btn_prev)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.video_actions_HLayout.addItem(spacerItem1)
        self.btn_play = QtWidgets.QPushButton(self.video_actions_group_box)

        self.btn_play.clicked.connect(self.play_frame)
        self.btn_play.setIcon(self.icons["play"])
        self.video_actions_HLayout.addWidget(self.btn_play)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.video_actions_HLayout.addItem(spacerItem2)
        self.btn_next = QtWidgets.QPushButton(self.video_actions_group_box)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_next.sizePolicy().hasHeightForWidth())
        self.btn_next.setSizePolicy(sizePolicy)
        self.btn_next.setIcon(self.icons["next"])
        self.btn_next.clicked.connect(self.next_frame)
        self.video_actions_HLayout.addWidget(self.btn_next)

        self.video_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.btn_end = QtWidgets.QPushButton(self.video_actions_group_box)
        self.btn_end.setIcon(self.icons["end"])
        self.btn_end.clicked.connect(self.go_last_processed_frame)
        self.video_actions_HLayout.addWidget(self.btn_end)

        self.video_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.frame_label = QtWidgets.QLabel(self.video_actions_group_box)
        self.frame_label.setStyleSheet("font-weight:bold;")
        self.frame_label.setText("")
        self.video_actions_HLayout.addWidget(self.frame_label)

        # self.video_actions_HLayout.addItem(QtWidgets.QSpacerItem(
        #     20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        # self.elapsed_label = QtWidgets.QLabel(self.video_actions_group_box)
        # self.elapsed_label.setStyleSheet("font-weight:bold;")
        # self.elapsed_label.setText("")
        # self.video_actions_HLayout.addWidget(self.elapsed_label)

        self.video_actions_HLayout.addItem(QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.btn_process = QtWidgets.QPushButton(self.video_actions_group_box)
        self.btn_process.setText("Process")
        self.btn_process.clicked.connect(self.process)
        self.video_actions_HLayout.addWidget(self.btn_process)

        self.btn_load_video = QtWidgets.QPushButton(
            self.video_actions_group_box)
        self.btn_load_video.setText("Load")
        self.btn_load_video.clicked.connect(self.loadVideo)
        self.video_actions_HLayout.addWidget(self.btn_load_video)

        self.btn_reset_video = QtWidgets.QPushButton(
            self.video_actions_group_box)
        self.btn_reset_video.setText("Reset")
        self.btn_reset_video.clicked.connect(self.reset)
        # self.btn_reset_video.clicked.connect(self.reset)
        self.video_actions_HLayout.addWidget(self.btn_reset_video)
        self.video_actions_HLayout.setStretch(11, 5)

        self.verticalLayout_2.addWidget(self.frame_actions_group_box)
        self.verticalLayout_2.addWidget(self.video_actions_group_box)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 8)
        self.verticalLayout_2.setStretch(2, 1)

    def changeSlider(self, value):
        value = int(value)
        self.active_countour.epsilon = value
        self.epsilon_slider.setValue(value)

    def changeEpsilon(self, value):
        self.active_countour.epsilon = int(value)
        print("Epsilon changed to ", value)
        self.epsilon_line_edit.setText(str(value))
