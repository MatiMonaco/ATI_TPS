import numpy as np 

class SpatialDomain: 

    def __init__(self):
 
        return

    def mask_filtering(self, mask_size, pixmap):

        mask = self.generate_mask(mask_size)
        img = pixmap.toImage()

        new_pixmap = pixmap 


        return new_pixmap  

    def generate_mask(self, mask_size): 

        return np.random.rand(mask_size,mask_size)

    # complete borders repeating rows and columns 
    def complete_image(img):
        
        width = 3#img.width()
        height = 3#img.height()

        new_img = np.zeros((width+2,height+2))

        print( new_img[1:height-1][0]) 

        new_img[0][1:width+1] = img[height-1]       # first row = old last row 
        new_img[height+1][1:width+1] = img[0]       # last row  = old first row 
        new_img[1:height+1][0] = img[:][width-1]    # left col  = old right col 
        new_img[width][:] = img[:][0]               # right col = old left col

        print(new_img)


if __name__ == '__main__':

    #SpatialDomain.complete_image([[1,2,3], [4,5,6], [7,8,9]])
    width = 3#img.width()
    height = 3#img.height()
    matrix = [  [0,9,0,0,0],  
                [0,1,2,3,0], 
                [0,4,5,6,0], 
                [0,7,8,9,0], 
                [0,0,0,0,0]]

    print(matrix[:,0]) 