# Background-subtraction-using-opencv
This is a repository of the final project for the Introduction to Visual Media Programming class of 2022-2 at Sogang university.

Team members: 20192017 Kothari Nandita Manish, 20220997 Kim Byul, 20221129 Choi Yunjeong

Professor: 서용덕 Seo Yeong Dok

How to use the code:

1. Original Video:

a. Conditions for a Normal video: 

- You could use any video that is stable and shot using a tripod. 
- There needs to be some seconds in the front and back of the video where the subject is absent, i.e. there is just the background. This will help the code to find the background of the video. 

b. Condiditions for chromakey video: You could also use a video shot with chroma key. 

2. Threshold value: 
- The threshold value in the line number 27 is set to 25. You could try changing this value to get better results. 
- If you are using CHROMA KEY, you should set the value to 1 and reduce the erosion and dilation to get a cleaner result. 

3. How to run the code:
- You could run the code in the terminal or any other application. When you run the code, it will ask you to input the file path name of the original video and path name of the new background image. To find the path name of the file, please follow the instructions below:

Finding path name in Mac: https://macpaw.com/how-to/get-file-path-mac
Finding path name in Windows: https://www.howtogeek.com/670447/how-to-copy-the-full-path-of-a-file-on-windows-10/

4. Saving the video: The final video will be automatically saved in the same folder where your python file is. You could change the name of the video in line number 55 (recorder = cv2.VideoWriter('no_background.mp4', fourcc, fps, (width,height)))

