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
      
        self.rho_param = {
            "param_name": "rho",
            "min": -200,
            "max": 200,
            "parts": 100
        }

        self.theta_param = {
            "param_name": "theta",
            "min": 0,
            "max": 179,
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

        self.figure_qty_slider.setMaximum(self.rho_param["parts"]*self.theta_param["parts"])

    def changeRhoParts(self, value):
        value  =int(value)
        self.rho_param["parts"] = value
        self.figure_qty_slider.setMaximum(self.theta_param["parts"]*value)
        print("Rho parts changed to ", value)

    def changeThetaParts(self, value):
        value  =int(value)
        self.theta_param["parts"] = value
        self.figure_qty_slider.setMaximum(self.rho_param["parts"]*value)
        print("Theta parts changed to ", value)

    def set_up_parameters(self, height, width):
        print("Setting up parameters")
        rho_range = math.sqrt(height**2 + width**2) # es la diagonal de la imagen
        self.rho_param["min"] = -rho_range
        self.rho_param["max"] = rho_range
        thetas = np.linspace(self.params[0]["min"], self.params[0]["max"], self.params[0]["parts"])
        rhos = np.linspace(self.params[1]["min"], self.params[1]["max"], self.params[1]["parts"])
        if not (0 in thetas):
            # para encontrar lineas verticales
            thetas = np.append(thetas,0)
            print("Addding 0º to theta values")
            self.theta_param["parts"]+=1
        if not (90 in thetas):
            # para encontrar lineas verticales
            thetas = np.append(thetas,90)
            print("Addding 90º to theta values")
            self.theta_param["parts"]+=1

        self.param_values.append(thetas)
        self.param_values.append(rhos)

        self.figure_qty_slider.setMaximum(self.rho_param["parts"]*self.theta_param["parts"])
       




    def accumulate(self,edge_points):
            thetas = self.param_values[0]
           
            rhos = self.param_values[1].reshape(self.params[1]["parts"],1)
      
         
            for edge_point in edge_points:
                x = edge_point[1]
                y = edge_point[0]
                # Calculo distancia a la linea para todos los Rhos
            
                epsilons = np.absolute(rhos - x*np.cos(thetas) - y*np.sin(thetas))
            
                # Me devuelve los indices de los Rhos que hacen que la distancia < epsilon
                indexes = np.argwhere(epsilons <= self.epsilon)
                # Para esos rhos y el theta, sumo 1 al acumulador
                self.accumulator[indexes[:,1],indexes[:,0]]+=1

               

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

            draw.line((real_x1, real_y1, real_x2, real_y2), fill="red")

        return np.asarray(img)
