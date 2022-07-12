import cv2
import matplotlib.pyplot as plt

def match_keypoints(detector, img1_path, img2_path, matched_img_name, matching_threshold=0.7): 

    img1 = cv2.imread(img1_path) # Esta es la que quiero detectar dentro de la img2
    img2 = cv2.imread(img2_path)  
    
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

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
 

if __name__ == '__main__':

    # Paths 
    original_img_path   = '/home/eugenia/ati/sift/autos0.png'
    img2_path           = '/home/eugenia/ati/sift/autos_iluminada.png'
    matched_img_name    = 'akaze_matched_images.jpg'

    # Create Detector Objects
    orb     = cv2.ORB_create()
    sift    = cv2.SIFT_create()
    akaze   = cv2.AKAZE_create()

    # Generate dataset 


    # Get Metrics
    matched_percentage = match_keypoints(orb, original_img_path, img2_path, matched_img_name)