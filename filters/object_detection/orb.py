import cv2
from filters.object_detection.feature_detector import FeatureDetector

class ORB(FeatureDetector): 

    def __init__(self, update_callback=None,setupUI =False):
        super().__init__(update_callback=update_callback, setupUI=setupUI)
       
    def name(self):
        return "ORB"

    def create_detector(self):
        return cv2.ORB_create(nfeatures=10000)