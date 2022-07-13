import cv2
from filters.object_detection.feature_detector import FeatureDetector

class SIFT(FeatureDetector): 

    def __init__(self, update_callback=None,setupUI =False):
        super().__init__(update_callback=update_callback, setupUI=setupUI)
       
    def name(self):
        return "SIFT"

    def create_detector(self):
        return cv2.SIFT_create()

    def distance_method(self):
        return cv2.NORM_L2
    