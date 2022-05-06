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
        print("IN CIRCLE")
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
            "min": 0,
            "max": 100,
            "parts": 10
        }
        self.params = [self.a_param, self.b_param, self.radius_param]
        self.params_len = len(self.params)
        self.setupUI()

    def setupUI(self):
        super().setupUI()
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout2)

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

        self.radius_label = QtWidgets.QLabel(self.groupBox)
        self.radius_label.setText(
            "<html><head/><body><span>Radius parts</span></body></html>")
        self.radius_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.radius_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.radius_label)

        self.radius_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.radius_line_edit.setValidator(onlyInt)
        self.radius_line_edit.editingFinished.connect(
            lambda: self.changeRadiusParts(self.radius_line_edit.text()))
        self.horizontalLayout2.addWidget(self.radius_line_edit)

        self.b_line_edit.setText(str(self.b_param["parts"]))
        self.a_line_edit.setText(str(self.a_param["parts"]))
        self.radius_line_edit.setText(str(self.radius_param["parts"]))
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 3)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(6, 1)
        self.horizontalLayout.setStretch(7, 3)

    def changeAParts(self, value):
        self.a_param["parts"] = int(value)
        print("Center X parts changed to ", value)

    def changeBParts(self, value):
        self.b_param["parts"] = int(value)
        print("Center Y parts changed to ", value)

    def changeRadiusParts(self, value):
        self.radius_param["parts"] = int(value)
        print("Radius parts changed to ", value)

    def accumulate(self, x, y):

        for i in range(self.params[0]["parts"]):
            a = self.param_values[0][i]
            for j in range(self.params[1]["parts"]):
                b = self.param_values[1][j]
                for k in range(self.params[2]["parts"]):
                    radius = self.param_values[2][k]
                    dist_to_circle = self.calculate_distance_to_circle(
                        x, y, a, b, radius)
                    if dist_to_circle < self.epsilon:
                        self.accumulator[i, j, k] += 1

    def calculate_distance_to_circle(self, x, y, a, b, radius):
        # (x-a)**2 + (y-b)**2 = radius**2
        return abs(radius**2 - (x-a)**2 - (y-b)**2)

    def draw_figure(self, img_arr, param_indexes):
        # line = [ theta, rho]
        img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1]))

        img = Image.fromarray(img_arr.astype(np.uint8),
                              mode='L' if self.isGrayScale else 'RGB')
        draw = ImageDraw.Draw(img)

        for circle in param_indexes:

            print(circle)
            center_x = self.param_values[0][circle[0]]
            center_y = self.param_values[1][circle[1]]
            radius = self.param_values[2][circle[2]]
            print(f"a = {center_x} b = {center_y} radius = {radius}")

            draw.ellipse((center_x-radius,  center_y-radius, center_x +
                         radius,  center_y+radius), fill=None, outline='red')

        return np.asarray(img)
