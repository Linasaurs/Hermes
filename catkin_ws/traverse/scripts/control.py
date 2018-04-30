#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import StringIO
import numpy as np

class control:
	def __init__(self):
		rospy.init_node('control', anonymous=True)
		
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

		self.pub_motion = rospy.Publisher('motion', String, queue_size=10)
		self.pub_target = rospy.Publisher('my_target', String, queue_size=10)
		self.pub_message = rospy.Publisher('my_message', String, queue_size=10)	
		self.pub_status = rospy.Publisher('my_status', String, queue_size=10)		
		self.pub_speak = rospy.Publisher('speak', String, queue_size=10)	

		self.motion = "woke_up"
		self.state = "woke_up"
		self.state_after_speak = state
		self.target = "None"
		self.message = "None"
		self.other_target = "None"
		self.other_message = "None"
		self.distance_threshold = 30
		self.theMostRandomVariable = 0 #look at the target_detected and message_detected

		rospy.spin()

	def sonic_front_call(self, data):
		distance=float(data.data)
		if distance < 5:
			distance = 300
		if distance < self.distance_threshold:
			pub_motion.publish("turn_left")			
			print "motion: turn_left"
		elif self.state == "searching":
			print "distance: ", distance
			pub_motion.publish("forward")
			print "motion: forward"

	def face_detected_call(self,data):
		if data.data == self.target:
			pub_status.publish("found")
			print "status: found"
			pub_motion.publish("pause")
			print "motion: pause"
			self.state_after_speak = "going_to_mailbox"
			self.state = "speaking"
			print "state: ", state
			pub_speak.publish(self.message)
			self.target = "None" 
			self.message = "None"
		else:
			print "face detected not the target, continue the search"
			pub_motion.publish("forward")
			print "motion: forward"

	def target_detected_call(self,data):
		self.target = data.data
		print "target: ", self.target
		pub_target.publish(data.data)
		self.state_after_speak = "searching"
		self.state = "speaking"
		print "state: ", state
		pub_speak.publish("I will deliver to " + self.target)
		self.theMostRandomVariable = 1

	def message_detected_call (self,data):
		self.message = data.data
		print "message: ", self.message
		pub_message.publish(data.data)
		while (self.theMostRandomVariable != 1):
			1+1
		self.state_after_speak = "searching"
		self.state = "speaking"
		print "state: ", state
		pub_speak.publish("The following message: " + self.message)
		self.theMostRandomVariable = 0
			
		
	def read_requested_call(self,data):
		self.state = "reading"
		pub_motion.publish("pause")
		print "motion: pause"

	def other_target(self,data):
		self.other_target = data.data

	def other_message(self,data):
		self.other_message = data.data

	def other_status(self,data):
		1+1 #TODO

	def speak_done_call(self,data):
			state = state_before_speak
			print "state: " , state_before_speak

if __name__ == '__main__':
	try:
		y= control()
	except rospy.ROSInterruptException:
		pass
