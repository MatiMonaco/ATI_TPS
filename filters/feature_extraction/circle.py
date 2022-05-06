from PyQt5.QtGui import QPixmap
import qimage2ndarray
import numpy as np
import math
from PIL import Image, ImageDraw
from filters.feature_extraction.hough_transform import HoughTransform


# Override la funcion del circle
class HoughTransformCircle(HoughTransform):

    def __init__(self, update_callback):
        super().__init__(update_callback)
        print("IN CIRCLE")
        self.a_param = {
            "param_name": "center_x",
            "min": 0,
            "max": 50,
            "parts": 25
        }

        self.b_param = {
            "param_name": "center_y",
            "min": 0,
            "max": 50,
            "parts": 25
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

            draw.ellipse((center_x+radius,  center_y+radius, center_x-radius,  center_y-radius), fill = None, outline ='blue')
        
        return np.asarray(img)

    def setupUI(self):
        super().setupUI()