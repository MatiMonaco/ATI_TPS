import qimage2ndarray
from ..filter import Filter

class ThresholdingFilter(Filter):


    def __init__(self):
        super().__init__()
  
        
    def get_threshold(self, img_arr):
        pass
     

    def apply(self,img):
        img_arr = qimage2ndarray.rgb_view(img).astype('int32')[:,:,0:self.channels]
        height = img_arr.shape[0]
        width = img_arr.shape[1]
        print("img_arr:\n ",img_arr)
        print("channel:\n",img_arr[:,:,0])
        for channel in range(self.channels):

            channel_threshold = self.get_threshold(img_arr[:,:,channel])
          
            for x in range(height):
                for y in range(width):
                
                    if img_arr[x,y,channel] < channel_threshold:         
                        img_arr[x,y,channel] = 0   
                    else:  
                        img_arr[x,y,channel] = 255
    
        return img_arr

      