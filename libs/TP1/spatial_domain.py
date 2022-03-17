import numpy as np 
import qimage2ndarray

class SpatialDomain: 

    def mask_filtering(self, mask_size, pixmap):

        img_arr = pixmap #TODO sacar
        mask = self.generate_mask(mask_size)
        
        #img = pixmap.toImage()
        #img_arr = qimage2ndarray.rgb_view(img).astype('int32')
        padding_size = int(np.floor(mask_size/2))

        extended_img = self.complete_image(img_arr, mask_size) 
        new_img = []
        for x in range(1,extended_img.shape[0]-1): 
            for y in range(1,extended_img.shape[1]-1):
                # cut img to size (floor(mask_size/2)) 
                sub_img = extended_img[x-padding_size:x+padding_size+1, y-padding_size:y+padding_size+1]
                new_pixel = np.sum(np.multiply(sub_img,mask))
                print(new_pixel)
                new_img[x,y] = new_pixel

        return new_img 

    def generate_mask(self, mask_size): 

        return np.zeros((mask_size,mask_size))+1/mask_size**2

    # complete borders repeating rows and columns 
    def complete_image(self, img, mask_size):
        
        width = img.shape[0]
        height = img.shape[1]

        padding_size = int(np.floor(mask_size/2))

        new_img = np.zeros((width+2*padding_size,height+2*padding_size))
      
        new_img[0,1:width+1] = img[height-1]       # first row = old last row 
        new_img[height+1,1:width+1] = img[0]       # last row  = old first row 
      
        new_img[1:height+1,0] = img[:,width-1]    # left col  = old right col 
        new_img[1:height+1,width+1] = img[:,0]    # right col = old left col

        new_img[1, 1:width+1] = img[0]
        new_img[2, 1:width+1] = img[1]
        new_img[3, 1:width+1] = img[2]

        return new_img



if __name__ == '__main__':

    width = 5#img.width()
    height = 5#img.height()
    #matrix = [  [0,0,0,0,0],  
    #            [0,1,2,3,0], 
    #            [0,4,5,6,0], 
    #            [0,7,8,9,0], 
    #            [0,0,0,0,0]]
               
    matrix = [  [1,2,3], 
                [4,5,6], 
                [7,8,9]] 
               

    SpatialDomain().mask_filtering(3, np.array(matrix)) 

    