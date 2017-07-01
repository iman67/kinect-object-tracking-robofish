import freenect 
import cv2 
import numpy as np
import imutils
from collections import deque
import argparse
import imutils 
greenLower = (30, 150, 50) 
greenUpper = (255, 255, 180)
""" Grabs a depth map from the Kinect sensor and creates an image from it. """ 
properties=["CV_CAP_PROP_FRAME_WIDTH",# Width of the frames in the video stream.
            "CV_CAP_PROP_FRAME_HEIGHT",# Height of the frames in the video stream.
            "CV_CAP_PROP_BRIGHTNESS",# Brightness of the image (only for cameras).
            "CV_CAP_PROP_CONTRAST",# Contrast of the image (only for cameras).
            "CV_CAP_PROP_SATURATION",# Saturation of the image (only for cameras).
            "CV_CAP_PROP_GAIN",# Gain of the image (only for cameras).
            "CV_CAP_PROP_EXPOSURE"] 
pts = deque(maxlen=32)
camera = cv2.VideoCapture(0)
#while True:
	#text_file = codecs.open("log2.txt", "a","utf-8-sig")
    #text_file.write(str(depth)+'\n')
   # depth = getDepthMap()
   # blur = cv2.GaussianBlur(depth, (5, 5), 0)
    #depth = imutils.resize(depth, width=200)
    #hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) #convert it to hsv    
    #blur.image_effect = 'colorswap'
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
 
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
   # if args.get("video") and not grabbed:
	#break
 
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
         cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
	c = max(cnts, key=cv2.contourArea)
	((x, y), radius) = cv2.minEnclosingCircle(c)
	M = cv2.moments(c)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
	     # draw the circle and centroid on the frame, 
	     # then update the list of tracked points
	     cv2.circle(frame, (int(x), int(y)), int(radius),
		 (0, 255, 255), 2)
	     cv2.circle(frame, center, 5, (0, 0, 255), -1)
             pts.appendleft(center)

             # loop over the set of tracked points
	     for i in xrange(1, len(pts)):
	         # if either of the tracked points are None, ignore
	         # them
	         if pts[i - 1] is None or pts[i] is None:
		     continue
                 # otherwise, compute the thickness of the line and
	 	 # draw the connecting lines
		 thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
		 cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 

             cv2.imshow('image', frame)
             cv2.waitKey(10)	
	
