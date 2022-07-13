import cv2
from filters.object_detection.feature_detector import FeatureDetector

class AKAZE(FeatureDetector): 

    def __init__(self, update_callback=None,setupUI =False):
        super().__init__(update_callback=update_callback, setupUI=setupUI)
       
    def name(self):
        return "AKAZE"

    def create_detector(self):
        return cv2.AKAZE_create()
        
    def distance_method(self):
        return cv2.NORM_HAMMING