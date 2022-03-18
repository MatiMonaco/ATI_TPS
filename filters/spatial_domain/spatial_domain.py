 
import numpy as np
import qimage2ndarray
from PyQt5.QtGui import QPixmap
from ..filter import Filter
from enum import Enum

class MaskType(Enum):
    MEAN_MASK = 0,
    GAUSS_MASK = 1,
    MEDIAN_MASK = 2,
    WEIGHTED_MEDIAN_MASK = 3,
    BORDER_MASK = 4
     


class SpatialDomainFilter(Filter):

    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback
        

    def mask_filtering(self, mask_size, pixmap):

        
        img = pixmap.toImage()
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')

        padding_size = int(np.floor(mask_size/2))

        mask = self.generate_mask(mask_size)
        

        extended_img = self.complete_image(img_arr, mask_size)
        
        new_img = []
        for x in range(padding_size, extended_img.shape[0]-padding_size):
            new_img.append([])
            for y in range(padding_size, extended_img.shape[1]-padding_size):
                # cut img to size (floor(mask_size/2))
                sub_img = extended_img[x-padding_size:x +
                                       padding_size+1, y-padding_size:y+padding_size+1]
                r = sub_img[:, :, 0]
                g = sub_img[:, :, 1]
                b = sub_img[:, :, 2]
              
                pixel = np.array([np.sum(np.multiply(r, mask)), np.sum(
                    np.multiply(g, mask)), np.sum(np.multiply(b, mask))])
                new_img[x-padding_size].append(pixel)

        return np.array(new_img)

    def generate_mask(self, mask_size):
        
        pass
        
        #return self.get_mean_mask(mask_size)
 
    # complete borders repeating rows and columns
    def complete_image(self, img, mask_size):

        width = img.shape[0]
        height = img.shape[1]
        padding_size = int(np.floor(mask_size/2))

        new_img = np.zeros((width+2*padding_size, height+2*padding_size, 3))
        ext_width = new_img.shape[0]
        ext_height = new_img.shape[1]
        # n = padding_size
        # first n rows = old last n row
        new_img[0:padding_size, 1:width+1] = img[height-padding_size:height]
        # last n row  = old first n row
        new_img[ext_height - padding_size: ext_height,
                1:width+1] = img[0:padding_size]

        # left col  = old right col
        new_img[padding_size:padding_size + height,
                0:padding_size] = img[:, width-padding_size:width]
        # right col = old left col
        new_img[padding_size:padding_size + height, ext_width -
                padding_size:ext_width] = img[:, 0:padding_size]

        # complete middle
        new_img[padding_size:ext_height - padding_size,
                padding_size:ext_width - padding_size] = img

        return new_img

    def apply(self, pixmap):

        res_arr = self.mask_filtering(5, pixmap)
        # print(res_arr)
        return QPixmap.fromImage(qimage2ndarray.array2qimage(res_arr))

    def get_mean_mask(self,mask_size): 
        return np.zeros((mask_size, mask_size))+1/mask_size**2
        
    def get_median_mask(self, mask_size):
        pass
    
    def get_weighted_median_mask(self, mask_size):
        pass

    def get_gauss_mask(self, mask_size):
        pass

    def get_border_mask(self, mask_size):
        pass
    