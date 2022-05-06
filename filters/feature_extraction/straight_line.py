from PyQt5.QtGui import QPixmap
import qimage2ndarray
import numpy as np
import math
from filters.feature_extraction.hough_transform import HoughTransform
from PIL import Image, ImageDraw
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator

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
            "parts": 181
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
        self.theta_line_edit.editingFinished.connect(
            lambda: self.changeThetaParts(self.theta_line_edit.text()))
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
        self.rho_line_edit.editingFinished.connect(
            lambda: self.changeRhoParts(self.rho_line_edit.text()))
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
        print("Rho parts changed to ", value)

    def changeThetaParts(self, value):
        self.theta_param["parts"] = int(value)
        print("Theta parts changed to ", value)

    def accumulate(self, x, y):

        for i in range(self.params[0]["parts"]):  # theta
            theta = self.param_values[0][i]

            for j in range(self.params[1]["parts"]):  # rho
                rho = self.param_values[1][j]

                dist_to_line = self.calculate_distance_to_line(
                    x, y, theta, rho)

                if dist_to_line < self.epsilon:  # si pertenece a la recta
                    self.accumulator[i, j] += 1

    def calculate_distance_to_line(self, x, y, theta, rho):
        # y*sen(theta) + x*cos(theta) = rho
        return abs(rho - x*math.cos(theta) - y*math.sin(theta))

    def straight_line_y(self, x, theta, rho):

        if theta == 0:
            return None
        y = (rho - x*math.cos(theta)) / math.sin(theta)
        return y

    def straight_line_x(self, y, theta, rho):

        x = (rho - y*math.sin(theta))/math.cos(theta)
        return x

    def draw_figure(self, img_arr, param_indexes):
        # line = [ theta, rho]
        img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1]))
        print(img_arr.shape)

        img = Image.fromarray(img_arr.astype(np.uint8),
                              mode='L' if self.isGrayScale else 'RGB')

        draw = ImageDraw.Draw(img)
        width = img_arr.shape[1]
        height = img_arr.shape[0]
        for line in param_indexes:

            theta = self.param_values[0][line[0]]
            rho = self.param_values[1][line[1]]
        #   print(f"theta: {theta} , rho = {rho}")

            if theta == 0.0:
                # es vertical
                print("es vertical")
                real_x1 = rho
                real_y1 = 0
                real_x2 = rho
                real_y2 = height-1
            else:

                # borde vertical izquierdo

                y1 = self.straight_line_y(0, theta, rho)
                y2 = self.straight_line_y(width-1, theta, rho)
                # Encontre horizontal
                if y1 >= 0 and y1 <= height and y2 >= 0 and y2 <= height:
                    real_y1, real_x1 = y1, 0
                    real_y2, real_x2 = y2, width-1
                else:
                    x1 = self.straight_line_x(0, theta, rho)
                    x2 = self.straight_line_x(height-1, theta, rho)
                    # Me quedo con el borde en y valida
                    real_y1, real_x1 = (
                        y1, 0) if y1 >= 0 and y1 <= height else (y2, width-1)
                    # Me quedo con el borde en x valida
                    real_y2, real_x2 = (
                        0, x1) if x1 >= 0 and x1 <= width else (height-1, x2)

            draw.line((real_x1, real_y1, real_x2, real_y2), fill=128)

        return np.asarray(img)
