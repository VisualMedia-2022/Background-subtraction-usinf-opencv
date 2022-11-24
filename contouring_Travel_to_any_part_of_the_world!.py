import cv2
import numpy as np

blur=21 #smoothness between background&foreground
canny_low=15 #the minimum intensity value along which edges will be drawn
canny_high = 150 #the maximum intensity value along which edges will be drawn
min_area = 0.0005 #the minimum area a contour in the foreground may occupy.(0~1)
max_area = 0.95 #the maximum area a contour in the foreground may occupy.
dilate_iter = 10 #the number of iterations of dilation will take place on the mask.
erode_iter = 10 #the number of iterations of erosion will take place on the mask.
mask_color = (0.0,0.0,0.0) #the color of the background once it is removed.

video=cv2.VideoCapture('/Users/USER/cat_mov.mp4')
img=cv2.imread("/Users/USER/ijypt.jpg")
img=cv2.resize(img,(1920,1080)) #make the background size same as video

while True:
    ret, frame = video.read()

    if ret == True:
            # Convert image to grayscale        
            image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Apply Canny Edge Dection
            edges = cv2.Canny(image_gray, canny_low, canny_high)

            #improve edges
            edges = cv2.dilate(edges, None)
            edges = cv2.erode(edges, None)

            #get the contours and their area
            contour_info=[]
            contours,hierarch=cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
            for con in contours: contour_info.append((con,cv2.contourArea(con)))

            #get the area of the image as a comparison
            image_area=frame.shape[0]*frame.shape[1]

            # calculate max and min areas in terms of pixels
            max_area = max_area * image_area
            min_area = min_area * image_area
            # Set up mask with a matrix of 0's
            mask = np.zeros(frame.shape, dtype = np.uint8)
            
            # Go through and find relevant contours and apply to mask
            for contour in contour_info:
                mask = cv2.fillConvexPoly(mask, contour[0], (255,255,255))
            # use dilate, erode, and blur to smooth out the mask
            mask = cv2.dilate(mask, None, iterations=dilate_iter)
            mask = cv2.erode(mask, None, iterations=erode_iter)
            mask = cv2.GaussianBlur(mask, (blur, blur), 0)

            #inversed colors mask
            inverse=np.zeros(frame.shape,dtype=np.uint8)
            inverse.fill(255)
            
            # #inverse mask
            inverse=cv2.bitwise_xor(mask,inverse)

            #mask backgrond image
            inverse=cv2.bitwise_and(inverse, img)
            
            #blend movie and background image
            mask=cv2.bitwise_and(mask,frame)

            #bundle all together
            mask=cv2.bitwise_or(mask,inverse)

            cv2.imshow("Foreground", mask)
            if cv2.waitKey(20)==27:break
    else:
        break
cv2.destroyAllWindows()
video.release()

