#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from collections import deque
from sensor_msgs.msg import Image 
import argparse
import imutils
import cv2
import sys
import numpy as np
import time
from cv_bridge import CvBridge, CvBridgeError
from shapedetector import ShapeDetector

#cap = cv2.VideoCapture(1)
frameWidth = 1024
white_lower= np.uint8([[[177,178,183 ]]])
white_higher=np.uint8([[[190,188,193]]])
hsvlower= cv2.cvtColor(white_lower,cv2.COLOR_BGR2HSV)
hsvupper=cv2.cvtColor(white_higher,cv2.COLOR_BGR2HSV)
print hsvlower, hsvupper
lower_range = np.array([0, 0, 200], dtype=np.uint8) ##55 and 80
upper_range = np.array([180, 255, 255], dtype=np.uint8)


def start(data):
	try:
		bridge = CvBridge()
		frame = bridge.imgmsg_to_cv2(data, "bgr8")
		#ret, frame = cap.read()
		
		frame = imutils.resize(frame, width=frameWidth)
		test_img1 = frame;
		#cv2.imshow('frame',frame)
		#perform a prediction
		#out = cv2.imwrite('capture.jpg', frame)
		
		detectshape (frame)
		
	except CvBridgeError as e:
		print(e)
		
def detectshape (img):
	
	resized = imutils.resize(img, width=600)
	ratio = img.shape[0] / float(resized.shape[0])


	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	#hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
	#hue ,saturation ,value = cv2.split(hsv)
	#mask = cv2.inRange(hsv,  lower_range, upper_range)
	#res = cv2.bitwise_and(resized,resized, mask= mask)
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	edges = cv2.Canny(thresh,100,200)
	out = cv2.imwrite('capture3.jpg',resized )
	
	# find contours in the thresholded image and initialize the
	# shape detector
	cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()
	for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
		M = cv2.moments(c)
		if M["m00"] != 0 and ratio != 0:
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)
			shape = sd.detect(c)
			c = c.astype("float")
			c *= ratio
			c = c.astype("int")
			cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
			cv2.putText(img, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (255, 255, 255), 2)
	#out2 = cv2.imwrite('capture2.jpg',img )
	print shape

	
rospy.init_node('shape', anonymous=True)			
rospy.Subscriber("/csi_cam/image_raw", Image, start)
rospy.spin()
