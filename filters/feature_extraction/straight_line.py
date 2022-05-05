from PyQt5.QtGui import QPixmap
import qimage2ndarray
import numpy as np
import math
from filters.feature_extraction.hough_transform import HoughTransform
from PIL import Image, ImageDraw
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QDoubleValidator, QIntValidator
# Override la funcion de la recta


class HoughTransformStraightLine(HoughTransform):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        rho_range = math.sqrt(2) * max(200, 200)
        self.rho_param = {
            "param_name": "rho",
            "min": -rho_range,
            "max": rho_range,
            "parts": 10
        }

        self.theta_param = {
            "param_name": "theta",
            "min": -90,
            "max": 90,
            "parts": 10
        }
        self.params = [self.theta_param, self.rho_param]
        self.params_len = len(self.params)
        self.setupUI()

    def setupUI(self):
        super().setupUI()
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout2)

        self.theta_label = QtWidgets.QLabel(self.groupBox)
        self.theta_label.setText(
            "<html><head/><body><span>&theta; parts</span></body></html>")
        self.theta_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.theta_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.theta_label)

        self.theta_line_edit = QtWidgets.QLineEdit(self.groupBox)
        onlyInt = QIntValidator()
        onlyInt.setBottom(0)
        self.theta_line_edit.setValidator(onlyInt)
        self.theta_line_edit.editingFinished.connect(lambda: self.changeThetaParts(self.theta_line_edit.text()))
        self.horizontalLayout2.addWidget(self.theta_line_edit)

        line = QtWidgets.QFrame(self.groupBox)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontalLayout2.addWidget(line)

        self.rho_label = QtWidgets.QLabel(self.groupBox)
        self.rho_label.setText(
            "<html><head/><body><span>&rho; parts</span></body></html>")
        self.rho_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.rho_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.rho_label)

        self.rho_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.rho_line_edit.setValidator(onlyInt)
        self.rho_line_edit.editingFinished.connect(lambda:self.changeRhoParts(self.rho_line_edit.text()))
        self.horizontalLayout2.addWidget(self.rho_line_edit)

        self.rho_line_edit.setText(str(self.rho_param["parts"]))
        self.theta_line_edit.setText(str(self.theta_param["parts"]))
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 3)

    def changeRhoParts(self, value):
        self.rho_param["parts"] = int(value)
        print("Rho parts changed to ",value)

    def changeThetaParts(self, value):
        self.theta_param["parts"] = int(value)
        print("Theta parts changed to ",value)

    def accumulate(self, x, y):
       

        for i in range(self.params[0]["parts"]):  # theta
            theta = self.param_values[0][i]
            for j in range(self.params[1]["parts"]):  # rho
                rho = self.param_values[1][j]
                dist_to_line = self.calculate_distance_to_line(
                    x, y, theta, rho)
                if dist_to_line < self.epsilon:
                    self.accumulator[i, j] += 1

    def calculate_distance_to_line(self, x, y, theta, rho):
        # y*sen(theta) + x*cos(theta) = rho
        return abs(rho - x*math.cos(theta) - y*math.sin(theta))

    def straight_line(self, x, theta, rho):
        y = (rho - x*math.cos(theta)) / math.sen(theta)
        return y

    def draw_figure(self, img_arr, lines):
        # line = [ the
        # ta, rho]
        img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1]))
        print(img_arr.shape)

        img = Image.fromarray(img_arr.astype(np.uint8),
                              mode='L' if self.isGrayScale else 'RGB')

        draw = ImageDraw.Draw(img)
        for line in lines:
            theta = line[0]
            rho = line[1]

            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            #x1 = 1
            #x2 = 2
            #y1 = self.straight_line(x1, theta, rho)
            #y2 = self.straight_line(x2, theta, rho)

            draw.line((x1, y1, x2, y2), fill=128)

        return np.asarray(img)
