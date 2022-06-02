import cv2

base_path = "/home/euge/ati/"
filenames = ["TEST.PGM"]

i=0
for filename in filenames:
    path = base_path + filename
    img = cv2.imread(path) 
    if img is not None:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        
        # rotate 90º 180º & 270º   
        cv2.imwrite('90.pgm',cv2.rotate(gray_img, cv2.ROTATE_90_CLOCKWISE))
        cv2.imwrite('180.pgm',cv2.rotate(gray_img, cv2.ROTATE_180))
        cv2.imwrite('270.pgm',cv2.rotate(gray_img, cv2.ROTATE_90_COUNTERCLOCKWISE))

        # flip 
        cv2.imwrite('flipV.pgm',cv2.flip(gray_img, 0))
        cv2.imwrite('flipH.pgm',cv2.flip(gray_img, 1))

        #resize 
      
        scale_percent = 50   #percent by which the image is resized

        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)

        dsize = (width, height)
        output = cv2.resize(gray_img, dsize)

        cv2.imwrite('resize.pgm',output) 