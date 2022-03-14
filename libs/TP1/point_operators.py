from PyQt5.QtGui import QPixmap, QColor, QRgba64
# A Point Operator applies a transformation to a pixel r (input_pixel) and returns the transformed pixel s (output_pixel) --> s = T(r)

L = 256 # levels of colors amount

class PointOperator: 
    # TODO: para imagenes de grises --> QImage.allGray()
    # To apply contrast: T(r) = c * r^gamma

    @staticmethod
    def power_function_gamma(pixmap, gamma):
        
        if gamma == 1 or gamma < 0 or gamma > 2: 
            raise('Gamma must be between 0 and 2 and gamma != 1')

        c = (L-1)/(L-1)**gamma
        img = pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                color = img.pixelColor(x,y)
                r = int(c * color.red() ** gamma)
                g = int(c * color.green() ** gamma)
                b = int(c * color.blue() ** gamma)
                img.setPixelColor(x, y, QColor(QRgba64.fromRgba(r, g, b, color.alpha()))) 
        
        return QPixmap.fromImage(img)

    # Get negative image: T(r) = -r + L-1
    @staticmethod
    def negative(pixmap): 
        img = pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                color = img.pixelColor(x,y)
                r = - color.red() + L - 1
                g = - color.green() + L - 1
                b = - color.blue() + L - 1
                img.setPixelColor(x, y, QColor(QRgba64.fromRgba(r, g, b, color.alpha())))
        return QPixmap.fromImage(img)

    # Get binary image: T(r) = 0 if r<=u, else 255
    @staticmethod
    def thresholding(pixmap, threshold): 
        img = pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                color = img.pixelColor(x,y)
                colors = [color.red(), color.green(), color.blue()]
                out = []
                for clr in colors:
                    if clr < threshold: 
                        out.append(0)
                    else:
                        out.append(L-1)
                img.setPixelColor(x, y, QColor(QRgba64.fromRgba(out[0], out[1], out[2], color.alpha())))
        return QPixmap.fromImage(img)


