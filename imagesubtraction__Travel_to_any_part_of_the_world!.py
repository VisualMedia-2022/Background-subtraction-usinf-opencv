import cv2 
import numpy as np

#function to resize image
#def resize(dst,img):
#	width = img.shape[1]
##	dim = (width, height)
#	resized = cv2.resize(dst, dim, interpolation = cv2.INTER_AREA)
#	return resized

#importing the video file

#use any static video where there is movement in the foreground. Results would be better if 
#the video has some seconds without any moving objects. 
stream = cv2.VideoCapture("/Users/nanditakothari/Desktop/Sogang 22-2/Visual Media/group project/cat.mov")

#import the background image that you want to put in place of the original background
bgimg = cv2.imread('/Users/nanditakothari/Desktop/Sogang 22-2/Visual Media/group project/pyramid.jpeg')
bgimg = cv2.resize(bgimg,[1920,1080])

#converting the image to grayscale
gray_bgimg = cv2.cvtColor(bgimg,cv2.COLOR_BGR2GRAY)

#getting the first frame as a reference to later resize the background image
success, ref_img = stream.read()
#bgimg = resize(bgimg,ref_img)

#creating variables to adjust the noise in the mask later
dilate_iter = 8
erode_iter = 8

#if there is no video file, it will exit the program
if not stream.isOpened():
    print("No stream :(")
    exit()

#create an empty list for getting the pixel values for the selected frame
frames = []

'''without the stream.get in the front, cv2.CAP_PROP_POS_FRAMES gives 7 as output 
    #and this somehow is the background image. I am not sure how it works. I wrote this code by mistake'''

for fid in range(cv2.CAP_PROP_POS_FRAMES): 
    stream.set(cv2.CAP_PROP_POS_FRAMES, fid) 
    ret, frame = stream.read() #reading each frame and getting the frame pixel information
    if not ret: # if no frames are returned, then exit the loop
        print("SOMETHING WENT WRONG")
        exit()
    frames.append(frame) #append the frame in frames list made above

#The median frame here is our background
median = np.median(frames, axis=0).astype(np.uint8) #find the median value of every pixel. Median value = background
median = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY) #convert median value to grayscale
median = cv2.GaussianBlur(median, (5,5), 0) #blur to reduce differences in pixel values in consequent frames


fps = stream.get(cv2.CAP_PROP_FPS) 
width = int(stream.get(3))
height = int(stream.get(4))

#setting the stream back to 0 frame
stream.set(cv2.CAP_PROP_POS_FRAMES, 0) 

while True:
    #reading the video file
    ret, frame = stream.read()
    
    #print(bgimg.shape, frame.shape)
    if not ret: # if no frames are returned
        print("No more stream :(")
        break
    
    '''subtracting background image from every frame by using absolute difference'''
    #coverting frame to grayscale
    mask_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #applying Gaussian Blur to remove noise
    mask_frame = cv2.GaussianBlur(mask_frame, (5,5), 0) #converting the video into grayscale
    #getting abs difference 
    dif_frame = cv2.absdiff(median, mask_frame) #getting the absolute difference value between median frame (background) and each frame
    
    '''setting the threshold for deciding whether to put the pixel in foreground
       more than threshold value or background (less than threshold value)'''
        
    threshold, mask = cv2.threshold(dif_frame, 25, 255,cv2.THRESH_BINARY) 

    #retouching the mask to remove holes and noise
    mask = cv2.dilate(mask, None, iterations=dilate_iter)
    mask = cv2.erode(mask, None, iterations=erode_iter)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    mask[mask>0]=255

    #inverting the mask to later use in the new background image
    inverted_mask = cv2.bitwise_not(mask)

    #creating foreground and background videos with the mask and inverted mask respectively
    foreground_vid = cv2.bitwise_and(frame,frame, mask=mask)
    background_vid = cv2.bitwise_and(bgimg, bgimg, mask = inverted_mask)
    
    #combining the new foreground and background videos
    finalvideo = cv2.bitwise_or(foreground_vid,background_vid)

    cv2.imshow('New video', finalvideo)
    cv2.imshow("Video!", frame)
    cv2.imshow("background", median)
    cv2.imshow("foreground with mask", foreground_vid)
    cv2.imshow("new background with mask",background_vid)
    
    cv2.waitKey(15)
    if cv2.waitKey(1) == ord('q'): # press "q" to quit
        break

#cleaning up
stream.release()
cv2.destroyAllWindows() 