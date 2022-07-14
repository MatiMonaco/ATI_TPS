import cv2
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.ndimage.interpolation import rotate
import time
import os

def match_keypoints(detector, img1, img2, matched_img_name, matching_threshold=0.7, distance_threshold=2000): 
    
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    start = time.process_time()
    # Detect SIFT features in both images
    keypoints_1, descriptors_1 = detector.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = detector.detectAndCompute(img2,None)

    if(descriptors_1 is None or descriptors_2 is None): 
        return 0, [], 0, 0, 0

    # Create feature matcher
    if(detector.getDefaultName() == "Feature2D.SIFT"):
        distance_type = cv2.NORM_L2
    else:
        distance_type = cv2.NORM_HAMMING

    bf = cv2.BFMatcher(distance_type, crossCheck=True)

    # Match descriptors of both images
    matches = bf.match(descriptors_1,descriptors_2)
    end = time.process_time()
    
    # Sort matches by Distance
    matches = sorted(matches, key = lambda x:x.distance)

    # Get Outliers Amount
    distance_threshold = 0.7
    distances = list(map(lambda x:x.distance, matches))
    min_distance = min(distances) 
    interval = max(distances) - min_distance  
    if interval == 0.0:
        outliers = []
    else:
        distances = list(map(lambda x: (x - min_distance) / interval, distances))
        outliers = list(filter(lambda distance: distance > distance_threshold, distances))

    # Draw first 50 matches
    matched_img = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches[:50], img2, flags=2)

    # Print Metrics
    matched_keypoints = len(matches)
    print(f"Keypoints in First Img: {len(keypoints_1)}")
    print(f"Keypoints in Second Img: {len(keypoints_2)}")
    print(f"Keypoints Matched: {matched_keypoints}")
    
    min_keypoints = min(len(keypoints_1), len(keypoints_2))
    matched_percentage = matched_keypoints /min_keypoints 

    hit = 0
    if matched_percentage > matching_threshold: 
        print(f"{matched_percentage} is acceptable ")
        hit = 1
    else:
        print(f"{matched_percentage} is not acceptable ")
    
    cv2.imwrite(matched_img_name, matched_img)

    return matched_percentage, outliers, end-start, matched_keypoints, hit

def generate_rotated_dataset(img): 
    angles = []
    images = [] 

    if img is not None:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        for angle in range(30, 350, 30):
            rotated = rotate(gray_img, angle=angle)
            cv2.imwrite(f'{angle}.jpg', rotated)
            images.append(rotated)
            angles.append(angle)
    
    return images, angles

def generate_resized_dataset(img): 
    
    images = [] 
    percentages = []

    if img is not None:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        
        for percentage in range(10, 200, 10): 
            scale_percent = percentage  #percent by which the image is resized

            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)

            dsize = (width, height)
            resized_img = cv2.resize(gray_img, dsize)

            cv2.imwrite(f'resized_{percentage}.jpg',resized_img) 

            images.append(resized_img) 
            percentages.append(percentage)
    
    return images, percentages

def generate_noisy_dataset(img):

    images = [] 
    mean = 0
    stds = []

    if img is not None:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        for std in range(1, 20): 
         
            gauss_noise = np.random.normal(mean, std, gray_img.shape)
            noisy_img = gray_img + gauss_noise

            cv2.imwrite(f'noise_{std}.jpg', noisy_img)
            images.append(noisy_img.astype('uint8'))
            stds.append(std)

    return images, stds


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
        font={'size': 20} 
    )  

    fig.show()

def plot_hits(y_arr, detectors, dataset_name):
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=detectors, 
        y=y_arr
    ))

    fig.update_layout(
        title=f"Hits By Detector - {dataset_name}", 
        yaxis_title=f"Hits",
        xaxis_title=f"Detector", 
        font={'size': 20} 
    )  

    fig.show()
  

def get_keypoints_metrics(detectors, original_img, transformed_imgs, matched_img_name, distance_threshold): 

    matched_percentages_by_detector = []
    outliers_by_detector = []
    times_by_detector = []
    keypoints_by_detector = []
    hits_by_detector = []

    for detector in detectors: 
        
        matched_percentages = []
        outliers_amounts = []
        times = []
        keypoints = []
        hits = 0
        for img in transformed_imgs:        
            # Match Keypoints
            matched_percentage, outliers, elapsed_time, matched_keypoints, hit = match_keypoints(detector, original_img, img, matched_img_name, distance_threshold=distance_threshold)  
            outliers_amount = len(outliers)
            print(outliers_amount)          
            matched_percentages.append(matched_percentage)
            outliers_amounts.append(outliers_amount)
            times.append(elapsed_time)
            keypoints.append(matched_keypoints)
            hits += hit

        matched_percentages_by_detector.append(matched_percentages)
        outliers_by_detector.append(outliers_amounts)
        times_by_detector.append(times)
        keypoints_by_detector.append(keypoints)
        hits_by_detector.append(hits/len(transformed_imgs))

    return matched_percentages_by_detector, outliers_by_detector, times_by_detector, keypoints_by_detector, hits_by_detector

def get_3d_dataset(path: str):
   
    return [cv2.imread(f"{path}/{f}") for f in os.listdir(path) if os.path.isfile(f"{path}/{f}")]

if __name__ == '__main__':

    # Paths 
    original_img_path   = '/home/eugenia/ati/sift/alonso.jpg'
    #img2_path           = '/home/eugenia/ati/sift/autos_iluminada.png'
    matched_img_name    = 'matched_images.jpg'
    dataset_name        = 'Alonso'     

    # Create Detector Objects
    sift        = cv2.SIFT_create()
    orb         = cv2.ORB_create(nfeatures=10000)
    orb1000     = cv2.ORB_create(nfeatures=1000)
    akaze       = cv2.AKAZE_create()
    brisk       = cv2.BRISK_create()
    detectors   = [sift, orb, orb1000, akaze, brisk]
    detector_names = ['SIFT', 'ORB', 'ORB(1000)', 'AKAZE', 'BRISK']
    distance_threshold = 0.7

    # Generate dataset 
    original_img = cv2.imread(original_img_path) 
    transformed_imgs_rotated, angles = generate_rotated_dataset(original_img)
    transformed_imgs_resized, percentages = generate_resized_dataset(original_img)
    transformed_imgs_noisy, stds = generate_noisy_dataset(original_img)

    # Get Metrics
    ## Rotation Resistance  
    matched_percentages_by_detector, outliers_by_detector, times, keypoints_by_detector, hits_by_detector  = get_keypoints_metrics(detectors, original_img, transformed_imgs_rotated, matched_img_name, distance_threshold)
    plot_metric(angles, matched_percentages_by_detector, f"Rotation Resistance - {dataset_name} - Matched %", "Grades", "Matched Percentage", detector_names )
    plot_metric(angles, outliers_by_detector, f"Rotation Resistance - {dataset_name} - Outliers th:{distance_threshold}", "Grades", "Outliers Amount", detector_names )
    plot_metric(angles, times, f"Rotation Resistance - {dataset_name} - Time", "Grades", "Time (ms)", detector_names )
    plot_metric(angles, keypoints_by_detector, f"Rotation Resistance - {dataset_name}- Matched Keypoints", "Grades", "Keypoints", detector_names )
     
    plot_hits(hits_by_detector, detector_names, f"{dataset_name} Rotation - Th: {distance_threshold}" )
   
    ## Scale Resistance   
    matched_percentages_by_detector, outliers_by_detector, times, keypoints_by_detector, hits_by_detector  = get_keypoints_metrics(detectors, original_img, transformed_imgs_resized, matched_img_name, distance_threshold)
    plot_metric(percentages, matched_percentages_by_detector, f"Scale Resistance - {dataset_name} - Matched %", "Scale Percentage", "Matched Percentage", detector_names)
    plot_metric(percentages, outliers_by_detector, f"Scale Resistance - {dataset_name} - Outliers th:{distance_threshold}", "Scale Percentage", "Outliers Amount", detector_names )
    plot_metric(percentages, times, f"Scale Resistance - {dataset_name} - Time", "Scale Percentage", "Time (ms)", detector_names )
    plot_metric(percentages, keypoints_by_detector, f"Scale Resistance - {dataset_name}- Matched Keypoints", "Scale Percentage", "Keypoints", detector_names )

    plot_hits(hits_by_detector, detector_names, f"{dataset_name} Scale - Th: {distance_threshold}" )
   
    ## Gaussian Noise Resistance
    matched_percentages_by_detector, outliers_by_detector, times, keypoints_by_detector, hits_by_detector  = get_keypoints_metrics(detectors, original_img, transformed_imgs_noisy, matched_img_name, distance_threshold)
    plot_metric(stds, matched_percentages_by_detector, f"Gaussian Noise Resistance - {dataset_name} - Matched %", "Std", "Matched Percentage", detector_names )
    plot_metric(stds, outliers_by_detector, f"Gaussian Noise Resistance - {dataset_name} - Outliers th:{distance_threshold}", "Std", "Outliers Amount", detector_names )
    plot_metric(stds, times, f"Gaussian Noise Resistance - {dataset_name} - Time", "Std", "Time (ms)", detector_names )
    plot_metric(stds, keypoints_by_detector, f"Gaussian Noise Resistance - {dataset_name} - Matched Keypoints", "Std", "Keypoints", detector_names )
    
    plot_hits(hits_by_detector, detector_names, f"{dataset_name} Gauss - Th: {distance_threshold}" )
    ## 3D Resistance 
    original_img  = cv2.imread('/home/eugenia/ati/sift/ARCOTRIUNFO/arco_original.png' ) 
    transformed_imgs_3d = get_3d_dataset("/home/eugenia/ati/sift/ARCOTRIUNFO")
    total = list(range(1, len(transformed_imgs_3d) + 1))
    matched_percentages_by_detector, outliers_by_detector, times, keypoints_by_detector, hits_by_detector = get_keypoints_metrics(detectors, original_img, transformed_imgs_3d, matched_img_name, distance_threshold)
    plot_metric(total, matched_percentages_by_detector, f"3D Resistance - Matched %", "Image number", "Matched Percentage", detector_names )
    plot_metric(total, outliers_by_detector, f"3D Resistance- Outliers th:{distance_threshold}", "Image number", "Outliers Amount", detector_names )
    plot_metric(total, times, f"3D Resistance - Time", "Image number", "Time (ms)", detector_names )
    plot_metric(total, keypoints_by_detector, "3D Resistance- Matched Keypoints", "Image number", "Keypoints", detector_names )
#
    plot_hits(hits_by_detector, detector_names, f"Arco Triunfo - Th: {distance_threshold}" )