from operator import index
from PyQt5.QtGui import QPixmap
import qimage2ndarray
import numpy as np
import math
from PIL import Image, ImageDraw
from filters.feature_extraction.hough_transform import HoughTransform
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator

# Override la funcion del circle


class HoughTransformCircle(HoughTransform):

    def __init__(self, update_callback):
        super().__init__(update_callback)

        self.a_param = {
            "param_name": "center_x",
            "min": 0,
            "max": 200,
            "parts": 100
        }

        self.b_param = {
            "param_name": "center_y",
            "min": 0,
            "max": 200,
            "parts": 100
        }

        self.radius_param = {
            "param_name": "radius",
            "min": 10,
            "max": 50,
            "parts": 100
        }
        self.params = [self.a_param, self.b_param, self.radius_param]
        self.params_len = len(self.params)
        self.setupUI()

    def setupUI(self):
        super().setupUI()
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.horizontalLayout3 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout3)

        self.a_label = QtWidgets.QLabel(self.groupBox)
        self.a_label.setText(
            "<html><head/><body><span>Center X parts</span></body></html>")
        self.a_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.a_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.a_label)

        self.a_line_edit = QtWidgets.QLineEdit(self.groupBox)
        onlyInt = QIntValidator()
        onlyInt.setBottom(0)
        self.a_line_edit.setValidator(onlyInt)
        self.a_line_edit.editingFinished.connect(
            lambda: self.changeAParts(self.a_line_edit.text()))
        self.horizontalLayout2.addWidget(self.a_line_edit)

        line = QtWidgets.QFrame(self.groupBox)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout2.addWidget(line)

        self.b_label = QtWidgets.QLabel(self.groupBox)
        self.b_label.setText(
            "<html><head/><body><span>Center Y parts</span></body></html>")
        self.b_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.b_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.b_label)

        self.b_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.b_line_edit.setValidator(onlyInt)
        self.b_line_edit.editingFinished.connect(
            lambda: self.changeBParts(self.b_line_edit.text()))
        self.horizontalLayout2.addWidget(self.b_line_edit)

        line2 = QtWidgets.QFrame(self.groupBox)
        line2.setFrameShape(QtWidgets.QFrame.VLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout2.addWidget(line2)

        self.radius_min_label = QtWidgets.QLabel(self.groupBox)
        self.radius_min_label.setText(
            "<html><head/><body><span>Radius min</span></body></html>")
        self.radius_min_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.radius_min_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout3.addWidget(self.radius_min_label)

        self.radius_min_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.radius_min_line_edit.setValidator(onlyInt)
        self.radius_min_line_edit.editingFinished.connect(
            lambda: self.changeRadiusMin(self.radius_min_line_edit.text()))
        self.horizontalLayout3.addWidget(self.radius_min_line_edit)

        self.radius_max_label = QtWidgets.QLabel(self.groupBox)
        self.radius_max_label.setText(
            "<html><head/><body><span>Radius max</span></body></html>")
        self.radius_max_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.radius_max_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout3.addWidget(self.radius_max_label)

        self.radius_max_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.radius_max_line_edit.setValidator(onlyInt)
        self.radius_max_line_edit.editingFinished.connect(
            lambda: self.changeRadiusMax(self.radius_max_line_edit.text()))
        self.horizontalLayout3.addWidget(self.radius_max_line_edit)


        self.radius_parts_label = QtWidgets.QLabel(self.groupBox)
        self.radius_parts_label.setText(
            "<html><head/><body><span>Radius parts</span></body></html>")
        self.radius_parts_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.radius_parts_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout3.addWidget(self.radius_parts_label)

        self.radius_parts_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.radius_parts_line_edit.setValidator(onlyInt)
        self.radius_parts_line_edit.editingFinished.connect(
            lambda: self.changeRadiusParts(self.radius_parts_line_edit.text()))
        self.horizontalLayout3.addWidget(self.radius_parts_line_edit)

        self.b_line_edit.setText(str(self.b_param["parts"]))
        self.a_line_edit.setText(str(self.a_param["parts"]))
        self.radius_parts_line_edit.setText(str(self.radius_param["parts"]))
        self.radius_min_line_edit.setText(str(self.radius_param["min"]))
        self.radius_max_line_edit.setText(str(self.radius_param["max"]))


        self.figure_qty_slider.setMaximum(
            self.a_param["parts"]*self.b_param["parts"]*self.radius_param["parts"])

    def changeAParts(self, value):
        value = int(value)
        self.a_param["parts"] = value
        self.calculate_param_parts()
        print("Center X parts changed to ", value)

    def changeBParts(self, value):
        value = int(value)
        self.b_param["parts"] = value
        self.calculate_param_parts()

        print("Center Y parts changed to ", value)

    def changeRadiusParts(self, value):
        value = int(value)
        self.radius_param["parts"] = value
        self.calculate_param_parts()

        print("Radius parts changed to ", value)

    def changeRadiusMin(self, value):
        value = int(value)
        self.radius_param["min"] = value
        self.calculate_param_parts()
        print("Radius min changed to ", value)


    def changeRadiusMax(self, value):
            value = int(value)
            self.radius_param["max"] = value
            self.calculate_param_parts()
            print("Radius max changed to ", value)


    def calculate_param_parts(self):
        self.param_values = list()
        As = np.linspace(
            self.params[0]["min"], self.params[0]["max"], self.params[0]["parts"])
        Bs = np.linspace(
            self.params[1]["min"], self.params[1]["max"], self.params[1]["parts"])
        radiuses = np.linspace(
            self.params[2]["min"], self.params[2]["max"], self.params[2]["parts"])

        self.param_values.append(As)
        self.param_values.append(Bs)
        self.param_values.append(radiuses)

        self.figure_qty_slider.setMaximum(
            self.a_param["parts"]*self.b_param["parts"]*self.radius_param["parts"])
        self.accumulator = self.calculate_accumulator()
    def set_up_parameters(self, height, width):
        print("Setting up parameters")
        self.a_param["max"] = width
        self.b_param["max"] = height
        self.calculate_param_parts()

    def accumulate(self, edge_points):

        for edge_point in edge_points:
            x = edge_point[1]
            y = edge_point[0]
            a = self.param_values[0].reshape(self.params[0]["parts"], 1)
            b = self.param_values[1]

            for k in range(self.params[2]["parts"]):
                radius = self.param_values[2][k]
                epsilons = np.abs(radius**2 - (x-a)**2 - (y-b)**2)

                indexes = np.argwhere(epsilons <= self.epsilon)
                # Para esos rhos y el theta, sumo 1 al acumulador
                self.accumulator[indexes[:, 0], indexes[:, 1], k] += 1

    def draw_figure(self, img_arr, param_indexes):
        # line = [ theta, rho]
        img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1]))
        print("draw figure img shape : ",img_arr.shape)
        if self.isGrayScale:
            print("is gray scale")
            img_arr = np.repeat(img_arr[:, :, np.newaxis], 3, axis=2)
        img = Image.fromarray(img_arr.astype(np.uint8), 'RGB')
        draw = ImageDraw.Draw(img)

        for circle in param_indexes:
            center_x = self.param_values[0][circle[0]]
            center_y = self.param_values[1][circle[1]]
            radius = self.param_values[2][circle[2]]

            draw.ellipse((center_x-radius,  center_y-radius, center_x +
                         radius,  center_y+radius), fill=None, outline='red')

        return np.asarray(img)
    
    def top_n_indexes(self, arr, n):
        result = np.where(arr == np.amax(arr))   
        index = (result[0][0], result[1][0]  , result[2][0]  )
        top_n = []
        top_n.append(index)
        return top_n
