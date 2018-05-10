#!/usr/bin/env python
from PIL import Image
import rospy
from std_msgs.msg import String
import pytesseract
import argparse
import cv2
import os


#speaked = "None"

#def speak_done_call(data):
#	global speaked
#	speaked = "done"

def ocrfn(data):
	#global speaked
	#image = cv2.imread(data.data)
	image = cv2.imread(data.data)
	
	#image = cv2.VideoCapture(0)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	text = pytesseract.image_to_string(gray, lang='eng', boxes=False, config = '-c language_model_penalty_non_dict_word=1 -psm=5 -oem=0')

	#cv2.imshow("gray image", image)
	#text = pytesseract.image_to_string(image, lang='eng', boxes=False, config = '-c language_model_penalty_non_dict_word=1 -psm=5 -oem=0')
	
	if text != "":
	
		MessageAndTarget = text.split()
	
		target = MessageAndTarget[0]
		message = " ".join(MessageAndTarget[1:])
	
		#message = text
		#target = text
	
		print "Target: ", target
		print "Message: ", message
	
	
		pub_m.publish(message)
		pub_t.publish(target)
		
		#speaked = "not done"
		#while speaked != "done":
		#	1+1
		#rospy.sleep(3)

	else:
		print "Invalid msg"



def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('ocr', anonymous=True)

    rospy.Subscriber("ocr_file", String, ocrfn)   
    #rospy.Subscriber("speak_done", String, speak_done_call)   

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
	pub_m = rospy.Publisher('message_detected', String, queue_size=10)
	pub_t = rospy.Publisher('target_detected', String, queue_size=10)
	listener()
