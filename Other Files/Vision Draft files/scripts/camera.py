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
from cv_bridge import CvBridge, CvBridgeError

def convert(data):
	try:
		bridge = CvBridge()
		frame = bridge.imgmsg_to_cv2(data, "bgr8")

		
		frame = imutils.resize(frame, width=frameWidth)
		test_img1 = frame;

		#perform a prediction
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

        if (confidence > 75):
            print ("Unkown")
        else:
            label_text = subjects[label]
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, label_text, rect[0], rect[1] - 5)
            print (label_text)
            pub.publish(label_text)
    else:
        print ("Unkown")

    return img
    
def draw_text(img, text, x, y):
    1+1

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('/home/nvidia/catkin_ws/src/vision/scripts/haarcascade_frontalface_alt.xml')

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    if (len(faces) == 0):
        return None, None

    (x, y, w, h) = faces[0]

    return gray[y:y+w, x:x+h], faces[0]

def draw_rectangle(img, rect):
    1+1

subjects = ["", "Lina", "Mazhar", "Obama"]
frameWidth = 900
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("/home/nvidia/catkin_ws/src/vision/scripts/weight.xml")

rospy.init_node('camera', anonymous=True)		
pub = rospy.Publisher('face_detected', String, queue_size=10)
rospy.Subscriber("/csi_cam/image_raw", Image, convert)
rospy.spin()
