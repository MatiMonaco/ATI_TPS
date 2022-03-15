from PyQt5.QtGui import QPixmap, QColor, QRgba64
from .filter import Filter


class NegativeFilter(Filter):

    def __init__(self):
        super().__init__()
     
          

    # Get negative image: T(r) = -r + L-1
    def apply(self,pixmap):
        img = pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                color = img.pixelColor(x,y)
                r = - color.red() + self.L - 1
                g = - color.green() + self.L - 1
                b = - color.blue() + self.L - 1
                img.setPixelColor(x, y, QColor(QRgba64.fromRgba(r, g, b, color.alpha())))
        return QPixmap.fromImage(img)
