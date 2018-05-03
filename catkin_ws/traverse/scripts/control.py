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
		self.message_list = []
		self.distance_threshold = int(sys.argv[1])
		self.last_target_read = "None"
		self.last_target_received = "None"

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
		rospy.Subscriber("other_found", String, self.other_found_call)
		rospy.Subscriber("speak_done", String, self.speak_done_call)
		rospy.Subscriber("state_debug", String, self.state_debug_call)
		

		self.pub_motion = rospy.Publisher('motion', String, queue_size=10)
		self.pub_target = rospy.Publisher('my_target', String, queue_size=10)
		self.pub_message = rospy.Publisher('my_message', String, queue_size=10)	
		self.pub_found = rospy.Publisher('my_found', String, queue_size=10)		
		self.pub_speak = rospy.Publisher('speak', String, queue_size=10)	


		rospy.spin()

	def state_debug_call(self,data):
		self.state = data.data
		print "state: " , self.state 
		if self.state == "pause":
			self.pub_motion.publish("pause")
			print "motion: pause"

	def sonic_front_call(self, data):
		distance=float(data.data)
		if distance < 5:
			distance = 300
		if distance < self.distance_threshold and self.state == "roaming":
			self.pub_motion.publish("turn_left")			
			print "motion: turn_left"
		elif self.state == "roaming":
			print "distance: ", distance
			self.pub_motion.publish("forward")
			print "motion: forward"			

	def remove_target_from_list(self,target):
		for index, message in enumerate(self.message_list)		
			if message[0] == target:
				message_to_process = message
				self.message_list.pop(index)
				print "Message removed:", message
				self.state_after_speak = "continue_list"
				self.state = "speaking"
				print "state: ", state
				self.pub_speak.publish("Hi " + self.target + ", message for you, "+ self.message)
				while self.state != "continue_list":
					1+1		
		self.state = "roaming"
		print "state: ", state					

	def face_detected_call(self,data):
		self.pub_found(data.data)
		self.remove_target_from_list(self,data.data)

	def add_message_to_list(self,target, message):
		self.message_list.append([target,message])
		print "Message added:", [target,message]

	def target_detected_call(self,data):
		self.add_target_to_list(data.data)
		print "target: ", self.target
		self.pub_target.publish(data.data)
		self.state_after_speak = "speaking"
		self.state = "speaking"
		print "state: ", state
		self.pub_speak.publish("I will deliver to " + self.target)
		self.last_target_read = data.data

	def message_detected_call (self,data):
		self.add_message_to_list(self.last_target_read, data.data)				
		self.message = data.data
		print "message: ", self.message
		self.pub_message.publish(data.data)
		while (self.last_target_read == "None"):
			1+1
		self.state_after_speak = "roaming"
		self.state = "speaking"
		print "state: ", state
		self.pub_speak.publish("The following message, " + self.message)
		self.last_target_read = "None"
			
		
	def read_request_call(self,data):
		self.state = "reading"
		self.pub_motion.publish("pause")
		print "motion: pause"

	def other_target_call(self,data):
		self.last_target_received = data.data

	def other_message_call(self,data):
		self.add_message_to_list(self.last_target_received, data.data)		

	def other_found_call(self,data):
		self.remove_target_from_list(self,data.data):

	def speak_done_call(self,data):
			self.state = state_after_speak
			print "state: " , state_after_speak

if __name__ == '__main__':
	try:
		y= control()
	except rospy.ROSInterruptException:
		pass
