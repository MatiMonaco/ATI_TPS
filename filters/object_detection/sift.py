import cv2 
from filters.filter import Filter

class SIFT(Filter): 

    def __init__(self, update_callback, setupUI = True):
        super().__init__()
        self.update_callback = update_callback 
        self.current_filter = self.sobel_filter
       

    def apply():
        img = cv2.imread('/home/eugenia/ati/TEST.PGM')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to greyscale

        # Create SIFT feature extractor
        sift = cv2.xfeatures2d.SIFT_create()

        # Detect features from the image
        keypoints, descriptors = sift.detectAndCompute(img, None)

        # Draw the detected key points
        sift_image = cv2.drawKeypoints(gray, keypoints, img) 


        cv2.imshow('image', sift_image)
        
        cv2.imwrite("table-sift.jpg", sift_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    