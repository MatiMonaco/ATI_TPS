from PyQt5.QtGui import QPixmap, QColor, QRgba64,QImage
from .filter import Filter
import qimage2ndarray
from time import process_time_ns
class NegativeFilter(Filter):

    def __init__(self):
        super().__init__()
     
          

    # Get negative image: T(r) = -r + L-1
    def apply(self,pixmap):
        t1_start = process_time_ns()
        img = pixmap.toImage()
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
        res_arr = -img_arr +self.L -1   
        pixmap = QPixmap.fromImage(qimage2ndarray.array2qimage(res_arr))  
        t1_stop = process_time_ns()
        print(f"Elapsed time: {t1_stop- t1_start}")
        return pixmap

    def apply2(self,pixmap):
        t1_start = process_time_ns()
        img = pixmap.toImage()
        for x in range(img.width()):
            for y in range(img.height()):
                color = img.pixelColor(x, y)
                r = - color.red() + self.L - 1
                g = - color.green() + self.L - 1
                b = - color.blue() + self.L - 1
                img.setPixelColor(x, y, QColor(
                    QRgba64.fromRgba(r, g, b, color.alpha())))
        pixmap = QPixmap.fromImage(img)
        t1_stop = process_time_ns()
        print(f"Elapsed time: {t1_stop- t1_start}")
        return pixmap
