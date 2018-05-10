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
import os
from cv_bridge import CvBridge, CvBridgeError

found_msg = "None"

def turn_vision_on_call(data):
	global found_msg
	found_msg = "yes"

def convert(data):
	try:
		global found_msg
		while found_msg!="yes":
			1+1
		found_msg = "no"
		global filename
		if (sys.argv[1] == "jetson"):
			bridge = CvBridge()
			frame = bridge.imgmsg_to_cv2(data, "bgr8")		
		elif (sys.argv[1] == "pi"):
			cap = cv2.VideoCapture(0)
			ret, frame = cap.read()
		
		frame = imutils.resize(frame, width=frameWidth)
		test_img1 = frame;
		#cv2.imshow('frame',frame)
		#perform a prediction
		#out = cv2.imwrite('capture.jpg', frame)
		if (sys.argv[1] == "jetson"):
			out = cv2.imwrite('/home/nvidia/catkin_ws/src/vision/scripts/capture.jpg', frame)
			filename="/home/nvidia/catkin_ws/src/vision/scripts/capture.jpg"
		elif (sys.argv[1] == "pi"):
			out = cv2.imwrite('/home/nvidia/catkin_ws/src/vision/scripts/capture.jpg', frame)
			filename="/home/raspi3/catkin_ws/src/vision/scripts/capture.jpg"
		predicted_img1 = predict(test_img1)

		
	except CvBridgeError as e:
		print(e)
		
def predict(test_img):
	#make a copy of the image as we don't want to chang original image
	img = test_img.copy()
	#detect face from the image
	face, rect = detect_face(img)

	#predict the image using our face recognizer
	if not face is None:
		label, confidence = face_recognizer.predict(face)

		if (confidence < 75):
			print ("Unkown", label, confidence)
		else:
			label_text = subjects[label]
			# draw a rectangle around face detected
			#draw_rectangle(img, rect)
			# draw name of predicted person
			#draw_text(img, label_text, rect[0], rect[1] - 5)
			print (label_text)
			pub_face.publish(label_text)
	else:
		print ("No face detected")
		pub_ocr.publish(filename)

	return img
	
#def draw_text(img, text, x, y):
#	1+1

def detect_face(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	if (sys.argv[1] == "jetson"):
		face_cascade = cv2.CascadeClassifier('/home/nvidia/catkin_ws/src/vision/scripts/haarcascade_frontalface_alt.xml')
	elif (sys.argv[1] == "pi"):
		face_cascade = cv2.CascadeClassifier('/home/raspi3/catkin_ws/src/vision/scripts/haarcascade_frontalface_alt.xml')

	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

	if (len(faces) == 0):
		return None, None

	(x, y, w, h) = faces[0]

	return gray[y:y+w, x:x+h], faces[0]

#def draw_rectangle(img, rect):
#	1+1

filename = "None"
subjects = ["", "Lina", "Mazhar", "Obama"]
frameWidth = 600
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

if (sys.argv[1] == "jetson"):
	face_recognizer.read("/home/nvidia/catkin_ws/src/vision/scripts/weight.xml")
	rospy.Subscriber("/csi_cam/image_raw", Image, convert)
elif (sys.argv[1] == "pi"):
	face_recognizer.read("/home/raspi3/catkin_ws/src/vision/scripts/weight.xml")
	while True:
		convert("not supposed to appear")	

rospy.init_node('camera', anonymous=True)		
rospy.Subscriber("turn_vision_on", String, turn_vision_on_call)   
pub_face = rospy.Publisher('face_detected', String, queue_size=10)
pub_ocr = rospy.Publisher('ocr_file', String, queue_size=10)
rospy.spin()