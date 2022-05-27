from cmath import pi
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
            "max": 180,
            "parts": 181
        }
        self.params = [self.theta_param, self.rho_param]
        self.params_len = len(self.params)
        self.setupUI()

    def setupUI(self):
        super().setupUI()
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout3 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.verticalLayout.addLayout(self.horizontalLayout3)

        self.theta_label = QtWidgets.QLabel(self.groupBox)
        self.theta_label.setText(
            "<html><head/><body><span>&theta; parts</span></body></html>")
        self.theta_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.theta_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.theta_label)

        self.theta_line_edit = QtWidgets.QLineEdit(self.groupBox)
        onlyInt = QIntValidator()
        
        self.theta_line_edit.setValidator(onlyInt)
        self.theta_line_edit.editingFinished.connect(
            lambda: self.changeThetaParts(self.theta_line_edit.text()))
        self.horizontalLayout2.addWidget(self.theta_line_edit)

        # line = QtWidgets.QFrame(self.groupBox)
        # line.setFrameShape(QtWidgets.QFrame.VLine)
        # line.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.horizontalLayout2.addWidget(line)

        self.theta_min_label = QtWidgets.QLabel(self.groupBox)
        self.theta_min_label.setText(
            "<html><head/><body><span>Theta min</span></body></html>")
        self.theta_min_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.theta_min_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.theta_min_label)

        self.theta_min_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.theta_min_line_edit.setValidator(onlyInt)
        self.theta_min_line_edit.editingFinished.connect(
            lambda: self.changeThetaMin(self.theta_min_line_edit.text()))
        self.horizontalLayout2.addWidget(self.theta_min_line_edit)

        self.theta_max_label = QtWidgets.QLabel(self.groupBox)
        self.theta_max_label.setText(
            "<html><head/><body><span>Theta max</span></body></html>")
        self.theta_max_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.theta_max_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout2.addWidget(self.theta_max_label)
        self.theta_max_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.theta_max_line_edit.setValidator(onlyInt)
        self.theta_max_line_edit.editingFinished.connect(
            lambda: self.changeThetaMax(self.theta_max_line_edit.text()))
        self.horizontalLayout2.addWidget(self.theta_max_line_edit)

        

        self.rho_label = QtWidgets.QLabel(self.groupBox)
        self.rho_label.setText(
            "<html><head/><body><span>&rho; parts</span></body></html>")
        self.rho_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.rho_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout3.addWidget(self.rho_label)

        self.rho_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.rho_line_edit.setValidator(onlyInt)
        self.rho_line_edit.editingFinished.connect(
            lambda: self.changeRhoParts(self.rho_line_edit.text()))
        self.horizontalLayout3.addWidget(self.rho_line_edit)


        self.rho_min_label = QtWidgets.QLabel(self.groupBox)
        self.rho_min_label.setText(
            "<html><head/><body><span>Rho min</span></body></html>")
        self.rho_min_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.rho_min_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout3.addWidget(self.rho_min_label)

        self.rho_min_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.rho_min_line_edit.setValidator(onlyInt)
        self.rho_min_line_edit.editingFinished.connect(
            lambda: self.changeRhoMin(self.rho_min_line_edit.text()))
        self.horizontalLayout3.addWidget(self.rho_min_line_edit)

        self.rho_max_label = QtWidgets.QLabel(self.groupBox)
        self.rho_max_label.setText(
            "<html><head/><body><span>Rho max</span></body></html>")
        self.rho_max_label.setStyleSheet(
            "font-weight: bold;\ncolor:rgb(255, 255, 255);")
        self.rho_max_label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout3.addWidget(self.rho_max_label)
        self.rho_max_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.rho_max_line_edit.setValidator(onlyInt)
        self.rho_max_line_edit.editingFinished.connect(
            lambda: self.changeRhoMax(self.rho_max_line_edit.text()))
        self.horizontalLayout3.addWidget(self.rho_max_line_edit)

        self.rho_line_edit.setText(str(self.rho_param["parts"]))
        self.theta_line_edit.setText(str(self.theta_param["parts"]))
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 3)

        self.figure_qty_slider.setMaximum(
            self.rho_param["parts"]*self.theta_param["parts"])
        self.rho_min_line_edit.setText(str(self.rho_param["min"]))
        self.rho_max_line_edit.setText(str(self.rho_param["max"]))
        self.theta_min_line_edit.setText(str(self.theta_param["min"]))
        self.theta_max_line_edit.setText(str(self.theta_param["max"]))
       

    def changeRhoParts(self, value):
        value = int(value)
        self.rho_param["parts"] = value
        self.calculate_param_parts()
        print("Rho parts changed to ", value)

    def changeThetaParts(self, value):
        value = int(value)
        self.theta_param["parts"] = value
        self.calculate_param_parts()
        print("Theta parts changed to ", value)

    def changeThetaMin(self, value):
        value = float(value)
        self.theta_param["min"] = value
        self.calculate_param_parts()
        print("Theta min changed to ", value)


    def changeThetaMax(self, value):
            value = float(value)
            self.theta_param["max"] = value
            self.calculate_param_parts()
            print("Theta max changed to ", value)

    def changeRhoMin(self, value):
        value = float(value)
        self.rho_param["min"] = value
        self.calculate_param_parts()
        print("Rho min changed to ", value)


    def changeRhoMax(self, value):
            value = float(value)
            self.rho_param["max"] = value
            self.calculate_param_parts()
            print("Rho max changed to ", value)

    def calculate_param_parts(self):
        self.param_values = list()
        thetas = np.linspace(
            self.params[0]["min"], self.params[0]["max"], self.params[0]["parts"])
        rhos = np.linspace(
            self.params[1]["min"], self.params[1]["max"], self.params[1]["parts"])
        # if not (0 in thetas):
        #     # para encontrar lineas verticales
        #     thetas = np.append(thetas, 0)
        #     print("Addding 0º to theta values")
        #     self.theta_param["parts"] += 1
        # if not (90 in thetas):
        #     # para encontrar lineas verticales
        #     thetas = np.append(thetas, 90)
        #     print("Addding 90º to theta values")
        #     self.theta_param["parts"] += 1

        self.param_values.append(thetas)
        self.param_values.append(rhos)
        print("thetas: ", thetas)
  

        self.figure_qty_slider.setMaximum(
            self.rho_param["parts"]*self.theta_param["parts"])
        self.accumulator = self.calculate_accumulator()


    def set_up_parameters(self, height, width):
    #     print("Setting up parameters")
    #     # es la diagonal de la imagen
    #     rho_range = math.sqrt(height**2 + width**2)
       
    #     self.rho_param["min"] = -rho_range
    #     self.rho_param["max"] = rho_range
  
    #     self.params = [self.theta_param, self.rho_param]
    
        self.calculate_param_parts()
        
       

    def accumulate(self, edge_points):
        thetas = self.param_values[0]

        print("self.params: ",self.params)
        rhos = self.param_values[1].reshape(self.params[1]["parts"], 1)

        for edge_point in edge_points:
            x = edge_point[1]
            y = edge_point[0]
            # Calculo distancia a la linea para todos los Rhos

            epsilons = np.absolute(rhos - x*np.cos(thetas*np.pi/180) - y*np.sin(thetas*np.pi/180))

            # Me devuelve los indices de los Rhos que hacen que la distancia < epsilon
            indexes = np.argwhere(epsilons <= self.epsilon)
            # Para esos rhos y el theta, sumo 1 al acumulador
            self.accumulator[indexes[:, 1], indexes[:, 0]] += 1

    def straight_line_y(self, x, theta, rho):
        if theta == 0:
            return math.inf
        theta = theta*np.pi/180
        
        y = (rho - x*math.cos(theta)) / math.sin(theta)
        return y

    def straight_line_x(self, y, theta, rho):
        theta = theta*np.pi/180
        x = (rho - y*math.sin(theta))/math.cos(theta)
        return x

    def draw_figure(self, img_arr, param_indexes):
        # line = [ theta, rho]
 
        if self.isGrayScale:
            img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1]))
            img_arr = np.repeat(img_arr[:, :, np.newaxis], 3, axis=2)


        img = Image.fromarray(img_arr.astype(np.uint8), 'RGB')

        draw = ImageDraw.Draw(img)
        width = img_arr.shape[1]
        height = img_arr.shape[0]
        theta_min = 1*np.pi/180
        for line in param_indexes:

            theta = self.param_values[0][line[0]]

            rho = self.param_values[1][line[1]]
            print(f"theta: {theta} , rho = {rho}")

           

            # borde vertical izquierdo
            k = 0
            Xs = []
            Ys = []
            y1 = self.straight_line_y(0, theta, rho)
            if y1 >= 0 and y1 <= height:
                k+=1
                Xs.append(0)
                Ys.append(y1)

            y2 = self.straight_line_y(width-1, theta, rho)

            if y2 >= 0 and y2 <= height:
                k+=1
                Xs.append(width-1)
                Ys.append(y2)
            print(f"y1: {y1}, y2: {y2}")
            if k < 2:
                x1 = self.straight_line_x(0, theta, rho)
                if x1 >= 0 and x1 <= width:
                    k+=1
                    Xs.append(x1)
                    Ys.append(0)
                x2 = self.straight_line_x(height-1, theta, rho)
                if k < 2:
                    if x2 >= 0 and x2 <= width:
                        k+=1
                        Xs.append(x2)
                        Ys.append(height-1)
                # # Encontre horizontal
                # if y1 >= 0 and y1 <= height and y2 >= 0 and y2 <= height:
                #     real_y1, real_x1 = y1, 0
                #     real_y2, real_x2 = y2, width-1
                # else:
                #     x1 = self.straight_line_x(0, theta, rho)
                #     x2 = self.straight_line_x(height-1, theta, rho)
                #     # Me quedo con el borde en y valida
                #     real_y1, real_x1 = (y1, 0) if y1 >= 0 and y1 <= height else (y2, width-1)
                #     # Me quedo con el borde en x valida
                #     real_y2, real_x2 = (0, x1) if x1 >= 0 and x1 <= width else (height-1, x2)
            print("K = ",k)
            print("Xs: ",Xs)
            print("Ys: ",Ys)
            
            draw.line((Xs[0], Ys[0], Xs[1], Ys[1]), fill="red")

        return np.asarray(img)
