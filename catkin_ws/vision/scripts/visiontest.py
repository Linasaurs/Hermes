#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from collections import deque
from sensor_msgs.msg import Image 
import argparse
import imutils
import cv2
import sys
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
cap = cv2.VideoCapture(1)


while True:
	ret, frame = cap.read()
	cv2.imshow( "Display window", frame )
	rospy.init_node('vision', anonymous=True)
	
def convert(data):
	1+1
