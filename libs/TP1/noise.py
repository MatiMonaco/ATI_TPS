from random import random
import enum
import numpy as np
from PyQt5.QtGui import QPixmap, QColor, QRgba64

class NoiseType(enum.Enum):
    GAUSS = 0
    RAYLEIGH = 1
    EXPONENTIAL = 3
    SALTPEPPER = 4

class Noise:
     
    @staticmethod
    def generate_noise(pixmap, noise_percentage, method): 
        
        # Select pixels to apply noise
        img = pixmap.toImage()
        
        # Select Noise Method
        #TODO: mezclar antes de recorrer para evitar que el ruido se apliqeu mayormente en los primeros pixeles
        for x in range(img.width()):
            for y in range(img.height()):

                if np.random.default_rng().normal(0, 1) < noise_percentage: 
                    color = img.pixelColor(x,y)

                    if method.get("type") == NoiseType.GAUSS: 
                        noise = Noise.gauss(method.get("params").get("mu"), method.get("params").get("sigma"))

                    elif method.get("type") == NoiseType.RAYLEIGH: 
                        noise = Noise.rayleigh(method.get("params").get("epsilon"))

                    elif method.get("type") == NoiseType.EXPONENTIAL: 
                        noise = Noise.exponential(method.get("params").get("lambda_"))

                    elif method.get("type") == NoiseType.SALTPEPPER:
                        noise = Noise.salt_and_pepper()
            
                    else: 
                        raise('Please enter a valid method')
                    img.setPixelColor(x, y, QColor(QRgba64.fromRgba(int(color.red()*noise), int(color.green()*noise), int(color.blue()*noise), color.alpha())))

        return QPixmap.fromImage(img)


    @staticmethod
    def gauss(mu, sigma):
        return np.random.default_rng().normal(mu, sigma)

    def rayleigh(epsilon): 
        return np.random.Generator.rayleigh(epsilon)

    def exponential(lambda_): 
        return np.random.Generator.exponential(1/lambda_)

    def salt_and_pepper(): 
        return 