import cv2
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def match_keypoints(detector, img1, img2, matched_img_name, matching_threshold=0.7): 

    #img1 = cv2.imread(img1_path) # Esta es la que quiero detectar dentro de la img2
    #img2 = cv2.imread(img2_path)  
    
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Create ORB object
    #orb = cv2.ORB_create()

    # Detect SIFT features in both images
    keypoints_1, descriptors_1 = detector.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = detector.detectAndCompute(img2,None)

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
    if matched_percentage > matching_threshold: 
        print(f"{matched_percentage} is acceptable ")
    else:
        print(f"{matched_percentage} is not acceptable ")
    
    cv2.imwrite(matched_img_name, matched_img)

    return matched_percentage


def generate_rotated_dataset(img): 
    
    images = [] 

    if img is not None:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        
        # rotate 90º 180º & 270º   
        cv2.imwrite('90.jpg',cv2.rotate(gray_img, cv2.ROTATE_90_CLOCKWISE))
        cv2.imwrite('180.jpg',cv2.rotate(gray_img, cv2.ROTATE_180))
        cv2.imwrite('270.jpg',cv2.rotate(gray_img, cv2.ROTATE_90_COUNTERCLOCKWISE))

        images.append(cv2.rotate(gray_img, cv2.ROTATE_90_CLOCKWISE))
        images.append(cv2.rotate(gray_img, cv2.ROTATE_180))
        images.append(cv2.rotate(gray_img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    
    return images

def generate_resized_dataset(img): 
    
    images = [] 

    if img is not None:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        
        for percentage in range(10, 90, 10): 
            scale_percent = percentage  #percent by which the image is resized

            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)

            dsize = (width, height)
            resized_img = cv2.resize(gray_img, dsize)

            cv2.imwrite(f'resized_{percentage}.jpg',resized_img) 

            images.append(resized_img) 
    
    return images

def plot_metric(feature_x_arr, y_arr_by_detector, title, x_label, y_label, detectors):
    
    fig = go.Figure()

    for i in range(0, len(detectors)):
        fig.add_trace(go.Scatter(
            x=feature_x_arr, 
            y=y_arr_by_detector[i], 
            mode='lines+markers',
            name=detectors[i],
        ))

    fig.update_layout(
        title=f"{title}", 
        yaxis_title=f"{y_label}",
        xaxis_title=f"{x_label}", 
        font={'size': 18} 
    )  

    fig.show()

def get_keypoints_metrics(detectors, original_img, transformed_imgs, matched_img_name): 

    matched_percentages_by_detector = []
    for detector in detectors: 

        matched_percentages = []
        for img in transformed_imgs:        
            # Match Keypoints
            matched_percentages.append(match_keypoints(detector, original_img, img, matched_img_name))

        matched_percentages_by_detector.append(matched_percentages)

    return matched_percentages_by_detector

if __name__ == '__main__':

    # Paths 
    original_img_path   = '/home/eugenia/ati/sift/autos0.png'
    #img2_path           = '/home/eugenia/ati/sift/autos_iluminada.png'
    matched_img_name    = 'matched_images.jpg'

    # Create Detector Objects
    sift        = cv2.SIFT_create()
    orb         = cv2.ORB_create()
    akaze       = cv2.AKAZE_create()
    detectors   = [sift, akaze]

    # Generate dataset 
    original_img = cv2.imread(original_img_path) 
    transformed_imgs_rotated = generate_rotated_dataset(original_img)
    transformed_imgs_resized = generate_resized_dataset(original_img)

    # Get Metrics
    ## Rotation Resistance  
    matched_percentages_by_detector = get_keypoints_metrics([sift, orb, akaze], original_img, transformed_imgs_rotated, matched_img_name)
    plot_metric(['90', '180', '270'], matched_percentages_by_detector, "Rotation Resistance", "Grades", "Matched Percentage", ['SIFT','ORB', 'AKAZE'] )

    ## Scale Resistance   
    # TODO Por alguna razon orb no funca con resize..
    matched_percentages_by_detector = get_keypoints_metrics([sift, akaze], original_img, transformed_imgs_resized, matched_img_name)
    plot_metric(['10', '20', '30', '40', '50', '60','70', '80', '90'], matched_percentages_by_detector, "Scale Resistance", "Scale Percentage", "Matched Percentage", ['SIFT', 'AKAZE'] )

    ## 3D Resistance 

    ## Gaussian Noise Resistance