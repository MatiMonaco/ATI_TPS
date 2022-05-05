from PyQt5.QtGui import QPixmap 
import qimage2ndarray
import numpy as np
import math
from filters.feature_extraction.hough_transform import HoughTransform
from PIL import Image, ImageDraw

# Override la funcion de la recta

class HoughTransformStraightLine(HoughTransform):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        rho_range = math.sqrt(2)* max(200, 200)
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
        

    def accumulate(self,x,y):

        for i in range(self.param_values_len[0]): # theta 
            theta = self.param_values[0][i]
            for j in range(self.param_values_len[1]): # rho 
                rho = self.param_values[1][j]
                dist_to_line = self.calculate_distance_to_line(x,y,theta,rho)
                if dist_to_line < self.epsilon:
                    self.accumulator[i,j] +=1


    def calculate_distance_to_line(self,x,y,theta,rho):
        # y*sen(theta) + x*cos(theta) = rho
        return abs(rho - x*math.cos(theta) - y*math.sin(theta))
    
    def straight_line(self, x, theta, rho): 
        y = (rho - x*math.cos(theta)) / math.sen(theta)
        return y

    def draw_figure(self, img_arr, lines): 
        # line = [ theta, rho] 
        print(img_arr)
        img = Image.fromarray(img_arr.astype(np.uint8))
        
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

            draw.line((x1,y1, x2,y2), fill=128)
        
        return  Image.getdata(img) 