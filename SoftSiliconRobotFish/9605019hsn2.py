import freenect 
import cv2 
import numpy as np
import imutils
from collections import deque
import argparse
import imutils 
import time
import wiringpi
import Adafruit_ADXL345
accel = Adafruit_ADXL345.ADXL345()
ax, by, cz  = accel.read()

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT)
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period = 0.01


greenLower = (0,0,0) 
greenUpper = (127,127,127)
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
        #gray = cv2.cvtColor(, cv2.COLOR_GRAY2BGR)
        #rgb, timestamp = freenect.sync_get_rgb()
        #cv2.ShowImage('Depth', depth.astype(np.uint8))
        #cv2.ShowImage('RGB', rgb[:, :, ::-1].astype(np.uint8))
	return depth
#cv2.NamedWindow('Depth')
#cv2.NamedWindow('RGB') 
while True:
#    for pulse in range(70,150,1):
#                wiringpi.pwmWrite(18, pulse)
#                time.sleep(delay_period)
#    for pulse in range(150,70,-1): 
#                wiringpi.pwmWrite(18, pulse)
#                time.sleep(delay_period)

	#text_file = codecs.open("log2.txt", "a","utf-8-sig")
    #text_file.write(str(depth)+'\n')
    depth = getDepthMap()
    blur = cv2.GaussianBlur(depth, (5, 5), 0)
    #depth = imutils.resize(depth, width=200)
    #image = (blur * 255).round().astype(np.uint8)
     
    gray = cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR)
    
    hsv = cv2.cvtColor(gray, cv2.COLOR_BGR2HSV) #convert it to hsv    
    #blur.image_effect = 'colorswap'

    mask = cv2.inRange(hsv,greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

   # cv2.imshow('h',mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
         cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    print 'start'
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
	c = max(cnts, key=cv2.contourArea)
	((x, y), radius) = cv2.minEnclosingCircle(c)
	M = cv2.moments(c)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#	print 'start'
        if radius > 10:
	     # draw the circle and centroid on the frame, 
	     # then update the list of tracked points
	     cv2.circle(mask, (int(x), int(y)), int(radius),
		 (0, 255, 255), 2)
	     cv2.circle(mask, center, 5, (0, 0, 255), -1)
             pts.appendleft(center)
             print 'x'
             print x
             if x > 250:
                for pulse in range(70,110,2):
                   wiringpi.pwmWrite(18, pulse)
                   time.sleep(delay_period)
                for pulse in range(110,70,-2): 
                   wiringpi.pwmWrite(18, pulse)
                   time.sleep(delay_period)
             if x<250:
                for pulse in range(110,150,2):
                   wiringpi.pwmWrite(18, pulse)
                   time.sleep(delay_period)
                for pulse in range(150,110,-2): 
                   wiringpi.pwmWrite(18, pulse)
                   time.sleep(delay_period)
             if 0<y<63:
                   wiringpi.pwmWrite(13,97)      
             if 63<y<127:
                   wiringpi.pwmWrite(13,106)
             if 127<y<191:
                   wiringpi.pwmWrite(13,115)
             if 192<y<255:
                   wiringpi.pwmWrite(13,102)
             if 255<y<318:
                   wiringpi.pwmWrite(13,70) 
             if 318<y<382:
                   wiringpi.pwmWrite(13,58)
             if 382<y<446:
                   wiringpi.pwmWrite(13,66)
             if 446<y<550:
                   wiringpi.pwmWrite(13,73)                                         
             if y==0:
                   wiringpi.pwmWrite(13,93)
             if y==63:
                   wiringpi.pwmWrite(13,102)
             if y==127:
                   wiringpi.pwmWrite(13,111)
             if y==191:
                   wiringpi.pwmWrite(13,120)
             if y==255:
                   wiringpi.pwmWrite(13,85)
             if y==318:
                   wiringpi.pwmWrite(13,55)
             if y==382:
                   wiringpi.pwmWrite(13,62)
             if y==446:
                   wiringpi.pwmWrite(13,70)
             if y==550:
                   wiringpi.pwmWrite(13,77)     
                              
             print y 
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
 
          
             
             cv2.imshow('image', mask)
             cv2.imshow('h2',depth)
             cv2.waitKey(10)	
    else:
        if ax>120:
           wiringpi.pwmWrite(13,120)
        if ax<120:
           wiringpi.pwmWrite(13,55)  
        wiringpi.pwmWrite(13,55)
        for pulse in range(70,150,1):
                wiringpi.pwmWrite(18, pulse)
                time.sleep(delay_period)
        for pulse in range(150,70,-1):  
                wiringpi.pwmWrite(18, pulse)
                time.sleep(delay_period)		
