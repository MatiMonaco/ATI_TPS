# A Point Operator applies a transformation to a pixel r (input_pixel) and returns the transformed pixel s (output_pixel) --> s = T(r)

L = 256 # levels of colors amount

class PointOperator: 

    def __init__(self, input_pixel):
       
        self.input_pixel = input_pixel


    # T(r) = c * r^gamma
    def power_function_gamma(self,gamma):

        if gamma == 1 or gamma < 0 or gamma > 2: 
            raise('Gamma must be between 0 and 2 and gamma != 1')

        c = (L-1)/(L-1)**gamma

        output_pixel = c * self.input_pixel**gamma 

        return output_pixel

    # T(r) = -r + L-1
    def negative(self): 

        return -self.input_pixel + L - 1



