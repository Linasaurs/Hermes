#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import StringIO
import numpy as np
import sys

class control:
	def __init__(self):
		rospy.init_node('control', anonymous=True)


		self.motion = "woke_up"
		self.state = "woke_up"
		self.state_after_speak = self.state
		self.target = "None"
		self.message = "None"
		self.other_target = "None"
		self.other_message = "None"
		self.distance_threshold = int(sys.argv[1])
		self.theMostRandomVariable = 0 #look at the target_detected and message_detected

		print "motion: ", self.motion
		print "state: ", self.state

		rospy.Subscriber("sonic_front", String, self.sonic_front_call)
		rospy.Subscriber("face_detected", String, self.face_detected_call)
		rospy.Subscriber("target_detected", String, self.target_detected_call)
		rospy.Subscriber("message_detected", String, self.message_detected_call)
		rospy.Subscriber("face_box_detected", String, self.read_request_call)
		rospy.Subscriber("message_box_detected", String, self.read_request_call)
		rospy.Subscriber("other_target", String, self.other_target_call)		
		rospy.Subscriber("other_message", String, self.other_message_call)
		rospy.Subscriber("other_status", String, self.other_status_call)
		rospy.Subscriber("speak_done", String, self.speak_done_call)
		rospy.Subscriber("state_debug", String, self.state_debug_call)
		

		self.pub_motion = rospy.Publisher('motion', String, queue_size=10)
		self.pub_target = rospy.Publisher('my_target', String, queue_size=10)
		self.pub_message = rospy.Publisher('my_message', String, queue_size=10)	
		self.pub_status = rospy.Publisher('my_status', String, queue_size=10)		
		self.pub_speak = rospy.Publisher('speak', String, queue_size=10)	


		rospy.spin()

	def state_debug_call(self,data):
		self.state = data.data
		print "state: " , self.state 

	def sonic_front_call(self, data):
		distance=float(data.data)
		if distance < 5:
			distance = 300
		if distance < self.distance_threshold and self.state == "searching":
			self.pub_motion.publish("turn_left")			
			print "motion: turn_left"
		elif self.state == "searching":
			print "distance: ", distance
			self.pub_motion.publish("forward")
			print "motion: forward"
		elif self.state == "pause":
			self.pub_motion.publish("pause")
			print "motion: pause"			

	def face_detected_call(self,data):
		if data.data == self.target:
			self.pub_status.publish("found")
			print "status: found"
			self.pub_motion.publish("pause")
			print "motion: pause"
			self.state_after_speak = "going_to_mailbox"
			self.state = "speaking"
			print "state: ", state
			self.pub_speak.publish("Hi " + self.target + ", " + self.message)
			self.target = "None" 
			self.message = "None"
		else:
			print "face detected not the target, continue the search"
			self.pub_motion.publish("forward")
			print "motion: forward"

	def target_detected_call(self,data):
		self.target = data.data
		print "target: ", self.target
		self.pub_target.publish(data.data)
		self.state_after_speak = "searching"
		self.state = "speaking"
		print "state: ", state
		self.pub_speak.publish("I will deliver to " + self.target)
		self.theMostRandomVariable = 1

	def message_detected_call (self,data):
		self.message = data.data
		print "message: ", self.message
		self.pub_message.publish(data.data)
		while (self.theMostRandomVariable != 1):
			1+1
		self.state_after_speak = "searching"
		self.state = "speaking"
		print "state: ", state
		self.pub_speak.publish(". The following message, " + self.message)
		self.theMostRandomVariable = 0
			
		
	def read_request_call(self,data):
		self.state = "reading"
		self.pub_motion.publish("pause")
		print "motion: pause"

	def other_target_call(self,data):
		self.other_target = data.data

	def other_message_call(self,data):
		self.other_message = data.data

	def other_status_call(self,data):
		1+1 #TODO

	def speak_done_call(self,data):
			self.state = state_before_speak
			print "state: " , state_before_speak

if __name__ == '__main__':
	try:
		y= control()
	except rospy.ROSInterruptException:
		pass
