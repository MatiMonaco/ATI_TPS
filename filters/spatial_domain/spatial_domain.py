import numpy as np 
import qimage2ndarray
from PyQt5.QtGui import QPixmap
from ..filter import Filter

class SpatialDomainFilter(Filter): 

    def mask_filtering(self, mask_size, pixmap):

        #img_arr = pixmap #TODO sacar
        mask = self.generate_mask(mask_size)
        img = pixmap.toImage()
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')
     
        padding_size = int(np.floor(mask_size/2))

        extended_img = self.complete_image(img_arr, mask_size) 
        print(extended_img)
        new_img = []
        for x in range(padding_size,extended_img.shape[0]-padding_size):
            new_img.append([])
            for y in range(padding_size,extended_img.shape[1]-padding_size):
                # cut img to size (floor(mask_size/2)) 
                sub_img = extended_img[x-padding_size:x+padding_size+1, y-padding_size:y+padding_size+1]
                r = sub_img[:,:,0]
                g = sub_img[:,:,1]
                b = sub_img[:,:,2]
                # new_pixel = np.sum(np.multiply(sub_img,mask))
                # print(new_pixel)
                # print(f"IMG: {sub_img}\nR: {r}\nG:{g}\nB:{b} \n--------------")
                pixel = np.array([np.sum(np.multiply(r,mask)), np.sum(np.multiply(g,mask)), np.sum(np.multiply(b,mask))])
                new_img[x-padding_size].append(pixel)
        return np.array(new_img) 

    def generate_mask(self, mask_size): 

        return np.zeros((mask_size,mask_size))+1/mask_size**2

    # complete borders repeating rows and columns 
    def complete_image(self, img, mask_size):
        
        width           = img.shape[0]
        height          = img.shape[1]
        print(f"w,h: {width,height}")
        padding_size    = int(np.floor(mask_size/2))

        new_img     = np.zeros((width+2*padding_size,height+2*padding_size,3))
        ext_width   = new_img.shape[0]
        ext_height  = new_img.shape[1]
        print(f"new w,h: {ext_width,ext_height}")
        # n = padding_size
        # first n rows = old last n row
        new_img[0:padding_size,1:width+1]                                             = img[height-padding_size:height]      
        # last n row  = old first n row
        new_img[ext_height - padding_size: ext_height,1:width+1]                      = img[0:padding_size]   

        # left col  = old right col
        new_img[padding_size:padding_size + height, 0:padding_size]                   = img[:,width-padding_size:width]      
        # right col = old left col
        new_img[padding_size:padding_size + height, ext_width-padding_size:ext_width] = img[:,0:padding_size]              

        # complete middle 
        new_img[padding_size:ext_height - padding_size, padding_size:ext_width - padding_size] = img
      
       
        return new_img

    def apply(self,pixmap): 
      
        res_arr = self.mask_filtering(5, pixmap)
        # print(res_arr)
        return QPixmap.fromImage(qimage2ndarray.array2qimage(res_arr))