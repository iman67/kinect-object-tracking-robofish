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
def getDepthMap(): 
        depth, timestamp = freenect.sync_get_depth()
        np.clip(depth, 0, 2**10 - 1, depth)
        depth >>= 2
        depth = depth.astype(np.uint8)
        #depth, timestamp = freenect.sync_get_depth()
        #gray = cv2.cvtColor(image,0, cv2.COLOR_BGR2GRAY)
        #rgb, timestamp = freenect.sync_get_rgb()
        #cv2.ShowImage('Depth', depth.astype(np.uint8))
        #cv2.ShowImage('RGB', rgb[:, :, ::-1].astype(np.uint8))
	return depth
#cv2.NamedWindow('Depth')
#cv2.NamedWindow('RGB') 
while True:

	#text_file = codecs.open("log2.txt", "a","utf-8-sig")
    #text_file.write(str(depth)+'\n')
    depth = getDepthMap()
    blur = cv2.GaussianBlur(depth, (5, 5), 0)
    #depth = imutils.resize(depth, width=200)
    image = (blur * 255).round().astype(np.uint8)
     
    #gray = cv2.cvtColor(depth, cv2.COLOR_BGRA2BGR)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #convert it to hsv    
    #blur.image_effect = 'colorswap'
    cv2.imshow('h',hsv)
    cnts = cv2.findContours(blur.copy(), cv2.RETR_EXTERNAL,
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
	     cv2.circle(depth, (int(x), int(y)), int(radius),
		 (0, 255, 255), 2)
	     cv2.circle(depth, center, 5, (0, 0, 255), -1)
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
		 cv2.line(depth, pts[i - 1], pts[i], (0, 0, 255), thickness)
 

             cv2.imshow('image', depth)
             cv2.waitKey(10)	
	
