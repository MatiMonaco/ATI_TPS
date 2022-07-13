import cv2
from cv2 import KeyPoint
import numpy as np
from filters.filter import Filter 
import plotly.graph_objects as go

class FeatureDetector(Filter): 

    def __init__(self, update_callback=None, setupUI: bool=False, matches_threshold: float=0.7, keypoint_descriptor: int=0):
        super().__init__()
        self.update_callback = update_callback
        self.matches_threshold = matches_threshold
        self.keypoint_descriptor = keypoint_descriptor 

    def create_detector(self):
        pass

    def distance_method(self):
        pass

    def apply(self,img_arr):
        img_arr = img_arr.astype(np.uint8)
    
        if self.isGrayScale:
            
            img_arr = img_arr.reshape((img_arr.shape[0], img_arr.shape[1]))
            img_arr = np.repeat(img_arr[:, :, np.newaxis], 3, axis=2)
        
        gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)

        # Create detector feature extractor
        detector = self.create_detector()
        # Detect features from the image
        keypoints, descriptors = detector.detectAndCompute(img_arr, None)
        keypoints_responses = list(map(lambda keypoint: keypoint.response ,keypoints))
        max_response = max(keypoints_responses)
        min_response = min(keypoints_responses)
        medium=max_response/2
        colors = list(map(lambda response: (255,0,0) if response < medium else (0,0,255) ,keypoints_responses))
        print("colors = ",colors)
       
        print("max = ",max_response)
        print("min = ",min_response)

        # Draw the detected key points
        detector_image = cv2.drawKeypoints(gray, keypoints, img_arr ,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 


        #cv2.imshow('image', sift_image)
        
        #cv2.imwrite("table-sift.jpg", sift_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        print(descriptors[self.keypoint_descriptor])
        self.plot_descriptor(descriptors[self.keypoint_descriptor])

        return img_arr


    def match_images(self,img1, img2): 
        img1 = img1.astype(np.uint8)
        img2 = img2.astype(np.uint8)
        # img1 = cv2.imread('/home/eugenia/ati/sift/arco1.png') # Esta es la que quiero detectar dentro de la img2
        # img2 = cv2.imread('/home/eugenia/ati/sift/arco2.png')  
        
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

        # Create detector object
        detector = self.create_detector()

        # Detect detector features in both images
        keypoints_1, descriptors_1 = detector.detectAndCompute(img1,None)
        keypoints_2, descriptors_2 = detector.detectAndCompute(img2,None)

        # Create feature matcher
        bf = cv2.BFMatcher(self.distance_method(), crossCheck=True)

        # Match descriptors of both images
        matches = bf.match(descriptors_1,descriptors_2)

        # sort matches by distance
        matches = sorted(matches, key = lambda x:x.distance)

        # Draw first 50 matches
        matched_img = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches[:100], img2, flags=2)
        keypoints_1_len = len(keypoints_1)
        keypoints_2_len = len(keypoints_2)
        matches_len = len(matches)

        print(f"Keypoints in First Img: {keypoints_1_len}")
        print(f"Keypoints in Second Img: {keypoints_2_len}")
        print(f"Keypoints Matched: {matches_len}")

        min_keypoints = min(len(keypoints_1), len(keypoints_2))
        matched_percentage = len(matches) /min_keypoints 
        acceptable = matched_percentage > self.matches_threshold
        if acceptable: 
            print(f"{matched_percentage} is acceptable ")
        else:
            print(f"{matched_percentage} is not acceptable ")

        
        #cv2.imwrite("matched_images.jpg", matched_img)


        return matched_img,keypoints_1_len,keypoints_2_len,matches_len,matched_percentage,acceptable
        

    def plot_descriptor(self, descriptor): 
        #descriptor /= sum(descriptor) TODO segun J son freq relativas pero no parece... 
        orientations = []

        for i in  range(len(descriptor)):
            orientations.append(i) #TODO poner bien las orientaciones  

        fig = go.Figure([go.Bar(x=orientations, y=descriptor)])

        fig.update_layout(
            title=f"{self.name()} Descriptor for keypoint {self.keypoint_descriptor}",
            xaxis_title="Orientations",
            yaxis_title="Amount", 
            font= { 'size': 18 }
        )
    
        fig.show()