# A Point Operator applies a transformation to a pixel r (input_pixel) and returns the transformed pixel s (output_pixel) --> s = T(r)

L = 256 # levels of colors amount

class PointOperator: 

    def __init__(self, input_pixel):
       
        self.input_pixel = input_pixel


    # To apply contrast: T(r) = c * r^gamma
    def power_function_gamma(self,gamma):

        if gamma == 1 or gamma < 0 or gamma > 2: 
            raise('Gamma must be between 0 and 2 and gamma != 1')

        c = (L-1)/(L-1)**gamma

        output_pixel = c * self.input_pixel**gamma 

        return output_pixel

    # Get negative image: T(r) = -r + L-1
    def negative(self): 

        return -self.input_pixel + L - 1

    # Get binaty image: T(r) = 0 if r<=u, else 255
    def thresholding(self, threshold ): 

        if self.input_pixel <= threshold: 
            return 0
        else:
            return L-1
    

