from filters.spatial_domain.border_detection.second_derivative import SecondDerivativeFilter

class LaplacianOfGaussFilter(SecondDerivativeFilter):

    def __init__(self, update_callback):
        super().__init__(update_callback)