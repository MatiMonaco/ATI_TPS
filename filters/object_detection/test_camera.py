from time import time
import cv2
from datetime import datetime

 
# Press SPACE to start
total_frames = 10
time_between_frames = 0.4 # seconds

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")
time_counter = time()
img_counter = 0
start = False
while True and img_counter < total_frames:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame) # For realtime 

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        start = True
        time_counter = time()
    #time.sleep(time_between_frames)
    if start and time() - time_counter > time_between_frames: 
        img_name = "camera{}.ppm".format(img_counter)
        cv2.imwrite(img_name, frame) 
      

        print("{} written!".format(img_name))
        img_counter += 1
        time_counter = time()

cam.release()

cv2.destroyAllWindows()