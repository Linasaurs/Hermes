#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
import StringIO
import numpy as np

class control:
	def __init__(self):
		rospy.init_node('control', anonymous=True)
		rospy.Subscriber("vision_topic", Int32, self.vision)
		rospy.Subscriber("sonic_front", String, self.distance_to_wall)
		rospy.Subscriber("Name_in_msg", String, self.Message_recipient)
		rospy.Subscriber("Name_in_Vision", String, self.Vision_name)
		self.pub = rospy.Publisher('control_topic', Int32, queue_size=10)		





		#rospy.init_node('control', anonymous=True)
		#self.pub = rospy.Publisher('control_topic', Int32, queue_size=10)
		#rospy.Subscriber("distance_to_box", Int32, self.distance_to_box)
		#rospy.Subscriber("arrow_direction", Int32, self.arrow_direction)

 		self.distance = '0'
		self.detection = 2
		self.msg_recipient = None
		self.person_detected = None
		#self.yaw = 0
		#self.read_yaw = 0
		#self.maxvalue = 400.0
		#self.standardspeed = 50.0
		
		self.publish()

	def Message_recipient(self, data):
		self.msg_recipient = data.data


	def Vision_name(self, data):
		self.person_detected = data.data

	def distance_to_wall(self, data):
		#output = StringIO.StringIO()
		#output.write(data);
		#data = float(output.getvalue().split()[1]);
		self.distance=float(data.data)
		if self.distance < 5:
			self.distance = 300

	def vision(self, data):
		output = StringIO.StringIO()
		output.write(data);
		data = float(output.getvalue().split()[1]);
		self.detection=data

## detection = 0 : mailbox detected, reading message if there any
## detection = 1 : Face detected, read out message
## detection = 2 : Nothing detected



	def publish(self):

		x = 50
		while not rospy.is_shutdown():

			if self.distance > x and self.detection == 0:
				decision = 3
			elif self.distance > x and self.msg_recipient == self.person_detected:  #Use this or the commented elif depending on Lina's code whether she send the name of the person detected or a value 0 or 1
			#elif self.distance > x and self.detection == 1:
				decision = 1
			elif self.distance > x and self.detection == 2:
				decision = 2
			elif self.distance < x and self.detection == 2:
				decision = 4 #decision = 3 USE 4 for ROTATE; 3 MAKES IT STOP FOR TESTING PURPOSES
			elif self.distance > x:
				decision = 0

	# decision = "hello world %s" % rospy.get_time()
			rospy.loginfo("distance = " + str(self.distance))
			rospy.loginfo("detection = " + str(self.detection))
			rospy.loginfo(decision)
			self.pub.publish(decision)
			

## decision = 0 : Move Forward  pid   NOT USED
## decision = 1 : DON'T MOVE    Face detected read out msg
## decision = 2 : Move Forward     
## decision = 3 : DON'T MOVE	check mailbox   read msg and person
## decision = 4 : Rotate Left

if __name__ == '__main__':
	try:
		y= control()
	except rospy.ROSInterruptException:
		pass
