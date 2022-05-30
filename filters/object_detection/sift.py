import cv2 
from filters.filter import Filter

class SIFT(Filter): 

    def __init__(self, update_callback, setupUI = True):
        super().__init__()
        self.update_callback = update_callback
        self.matches_threshold = 0.7  
       

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

    def match_images(self, img1, img2): 
        img1 = cv2.imread('/home/eugenia/ati/sift/arco1.png') # Esta es la que quiero detectar dentro de la img2
        img2 = cv2.imread('/home/eugenia/ati/sift/arco2.png')  
        
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Create SIFT object
        sift = cv2.xfeatures2d.SIFT_create()

        # Detect SIFT features in both images
        keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

        # Create feature matcher
        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

        # Match descriptors of both images
        matches = bf.match(descriptors_1,descriptors_2)

        # sort matches by distance
        matches = sorted(matches, key = lambda x:x.distance)

        # Draw first 50 matches
        matched_img = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches[:50], img2, flags=2)

        print(f"Keypoints in First Img: {len(keypoints_1)}")
        print(f"Keypoints in Second Img: {len(keypoints_2)}")
        print(f"Keypoints Matched: {len(matches)}")

        min_keypoints = min(len(keypoints_1), len(keypoints_2))
        matched_percentage = len(matches) /min_keypoints 
        if matched_percentage > self.matches_threshold: 
            print(f"{matched_percentage} is acceptable ")
        else:
            print(f"{matched_percentage} is not acceptable ")

        
        cv2.imwrite("matched_images.jpg", matched_img)

    