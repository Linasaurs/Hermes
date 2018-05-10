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

cap = cv2.VideoCapture(1)
frameWidth = 900
rospy.Subscriber("/csi_cam/image_raw", Image, start)


def start(data):
	try:
		#bridge = CvBridge()
		#frame = bridge.imgmsg_to_cv2(data, "bgr8")
		ret, frame = cap.read()
		
		frame = imutils.resize(frame, width=frameWidth)
		test_img1 = frame;
		#cv2.imshow('frame',frame)
		#perform a prediction
		#out = cv2.imwrite('capture.jpg', frame)
		
		detectshape (frame)
		
	except CvBridgeError as e:
		print(e)
		
def detectshape (img):

	resized = imutils.resize(img, width=300)
	ratio = image.shape[0] / float(resized.shape[0])

	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the thresholded image and initialize the
	# shape detector
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()
	print (sd)

