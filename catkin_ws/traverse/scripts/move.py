#!/usr/bin/env python
import rospy
import random
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Int32

import serial
import time
import numpy
import StringIO
from numpy import interp
 
ser = serial.Serial('/dev/ttyS0', 19200, timeout = 1)
#rospy.init_node('move_dagu', anonymous=True)


class control:
	def __init__(self):
		self.move = 0
		self.cn = 7
		self.yaw = 0
		self.read_yaw = 0
		self.maxvalue = 400.0
		self.standardspeed = 60.0
		self.stp = 0;
		self.starting_yaw = 0
	
		rospy.init_node('move_dagu', anonymous=True)
		rospy.Subscriber("control_effort", Float64, self.bigfn)
		rospy.Subscriber("control_topic", Int32, self.control)
		rospy.Subscriber("yaw_topic", Float64, self.ret_yaw)
		rospy.Subscriber("debug_signal", String, self.get_debug_signal)

		#rospy.init_node('control', anonymous=True)
		#self.pub = rospy.Publisher('control_topic', Int32, queue_size=10)
		#rospy.Subscriber("distance_to_box", Int32, self.distance_to_box)
		#rospy.Subscriber("arrow_direction", Int32, self.arrow_direction)
		

 
	def backward(self, speed):
		command_left = chr(0xC2)
		command_right = chr(0xCA)
		ser.write(command_left)
		ser.write(chr(speed))
		ser.write(command_right)
		ser.write(chr(speed))
 
	def forward(self, speed_left,speed_right):
		if reverse == "1":
			command_left = chr(0xC2)
			command_right = chr(0xCA)				
		else:
			command_left = chr(0xC9)
			command_right = chr(0xC1)
		ser.write(command_left)
		ser.write(chr(speed_left))
		ser.write(command_right)
		ser.write(chr(speed_right))
 
	def stop(self):
		command_left = chr(0xC2)
		command_right = chr(0xCA)
		ser.write(command_left)
		ser.write(chr(0))
		ser.write(command_right)
		ser.write(chr(0))
 
	def rotate_left(self, speed):
		command_left = chr(0xC1)
		command_right = chr(0xCA)
		ser.write(command_left)
		ser.write(chr(speed))
		ser.write(command_right)
		ser.write(chr(speed))
 
	def rotate_right(self, speed):
		command_left = chr(0xC2)
		command_right = chr(0xC9)
		ser.write(command_left)
		ser.write(chr(speed))
		ser.write(command_right)
		ser.write(chr(speed))
 
	def turn_right(self, speed):
		command_left = chr(0xC1)
		command_right = chr(0xCA)
		ser.write(command_left)
		ser.write(chr(speed))
		ser.write(command_right)
		ser.write(chr(speed))

	def turn_left(self, speed):
		command_left = chr(0xC2)
		command_right = chr(0xC9)
		ser.write(command_left)
		ser.write(chr(speed))
		ser.write(command_right)
		ser.write(chr(speed))

	def bigfn(self, data):
		output = StringIO.StringIO()
		output.write(data);
		data = float(output.getvalue().split()[1]);
		self.move = data

	
	#	rospy.loginfo(str(cn))
	#	if cn == 0:

	def control(self, data):
		output = StringIO.StringIO()
		output.write(data);
		data = float(output.getvalue().split()[1]);
		self.cn = data

	def ret_yaw(self, data):		
		output = StringIO.StringIO()
		output.write(data);
		data = float(output.getvalue().split()[1]);
		self.yaw = data
		self.read_yaw =  1
		
	
	def get_debug_signal(self,data):
		if (data.data == "stop"):
			self.stp = 1;
	
	def move_forward(self):
		if self.move > 0:
			#self.move = -self.move
			#self.turn_left(int(self.standardspeed * self.move/self.maxvalue))
			speed = int(self.standardspeed)
			#turn = int(interp(self.move,[-126,0],[0,self.standardspeed] ))
			turn = int(interp(self.move,[0,126],[self.standardspeed,30] ))


			rospy.loginfo('Left ')
			rospy.loginfo('speed: ' +str(self.standardspeed))
			rospy.loginfo('Turn: ' + str(int(turn)))
			rospy.loginfo('Move: ' +str(self.move))

			self.forward(turn,speed)

		elif self.move < 0:				#Move forward towards box --Right
			#self.turn_right(int(self.standardspeed * self.move/self.maxvalue))
			speed = int(self.standardspeed)
			#turn = int(interp(self.move,[0,126],[self.standardspeed,0] ))
			turn = int(interp(self.move,[-126,0],[30,self.standardspeed] ))					

			rospy.loginfo('Right ')
			rospy.loginfo('Speed: ' +str(self.standardspeed))
			rospy.loginfo('Turn: ' +str(int(turn)))
			rospy.loginfo('Move: ' + str(self.move))
			
			self.forward(speed,turn)

		else :
			self.forward(int(self.standardspeed),int(self.standardspeed))
			rospy.loginfo('Move: ' +str(self.move))

	def yaw_turn(self,degrees,direction):	
		if direction == "counter":	
			if 180-self.starting_yaw<degrees:
				remaining =degrees-(180-self.starting_yaw)
				end = -180+remaining
				while yaw>0:
					1+1
				while yaw<=end:
					1+1		
			else:
				end = self.starting_yaw+degrees
				while yaw<=end:
					1+1

	def move_left(self):
		print self.starting_yaw
		self.rotate_left(35)
		self.yaw_turn(degrees,"counter")
		self.stop()
		#rospy.sleep(2)
		print self.yaw
		#rospy.sleep(3000)
		
		#while abs(self.yaw - self.starting_yaw) < 90.0:
			#print self.yaw
		#	self.rotate_left(50)
		'''				
		if 	self.starting_yaw<-135.0:
			while abs(self.yaw - self.starting_yaw) < 270.0:
				self.rotate_left(50)		
		else:
			while abs(self.yaw - self.starting_yaw) < 90.0:
				self.rotate_left(50)
		'''
		
		#rospy.loginfo('completed left turn')
		#print self.yaw

	def moving_right(self):
		print self.starting_yaw
		if self.yaw < 90 and self.yaw > 1:
			while self.yaw > 0 :
				self.rotate_right(35)
			while abs(self.yaw - 0) < 90 - abs(self.starting_yaw - 0) :
				self.rotate_right(35)
		elif self.yaw < -89 and self.yaw > -178:
			#while self.yaw > -177 and self.yaw < 0:
			while self.yaw < 0 :
				self.rotate_right(35)
			while abs(179 - self.yaw) < 90 - abs(179 + self.starting_yaw) :
				self.rotate_right(35)
		else :
			while abs(self.yaw - self.starting_yaw) < 90 :
				self.rotate_right(35)
		
		self.stop()
		#rospy.sleep(2)
		print self.yaw
		#rospy.sleep(3000)
		
		#while abs(self.yaw - self.starting_yaw) < 90.0:
			#print self.yaw
		#	self.rotate_left(50)
		'''				
		if 	self.starting_yaw<-135.0:
			while abs(self.yaw - self.starting_yaw) < 270.0:
				self.rotate_left(50)		
		else:
			while abs(self.yaw - self.starting_yaw) < 90.0:
				self.rotate_left(50)
		'''
		
		#rospy.loginfo('completed left turn')
		#print self.yaw
		#rospy.sleep(3000)

		#while abs(self.yaw - self.starting_yaw) < 87.0:
		#	self.rotate_left(50)
						
		#if 	self.starting_yaw>135.0:
		#	while self.yaw - self.starting_yaw < -270.0 or self.yaw>0:
		#		print self.yaw
		#		self.rotate_right(50)		
		#else:
		#	while abs(self.yaw - self.starting_yaw) < 90.0:
			#	self.rotate_right(50)

		
		#rospy.loginfo('completed right turn')
		#print self.yaw


	def run(self):
		self.cn = 2 #mazhar
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			if (self.stp == 1):
				self.stop()
				break
			rospy.loginfo('control signal: ' +str(self.cn))
			#while (self.read_yaw==0):
			#		xyzsdff=0
			self.starting_yaw = self.yaw
			if self.cn == 2:					#Move forward towards box --Left
				self.move_forward()

			elif self.cn == 4 :							#Rotate Left
				self.move_left()

			elif self.cn == 100 :							#Rotate Right
				self.move_right()

			else :
				self.stop()

		rate.sleep() 


	#def rotate_left(speed):
	#	command_left = chr(0xC2)
	#	command_right = chr(0xC9)
   	#	ser.write(command_left)
	#	ser.write(chr(speed))
	#	ser.write(command_right)
	#	ser.write(chr(speed))
 
	#def rotate_right(speed):
	#	command_left = chr(0xC1)
	#	command_right = chr(0xCA)
	#	ser.write(command_left)
	#	ser.write(chr(speed))
	#	ser.write(command_right)
   	#	ser.write(chr(speed))
 
	#def turn_right(speed):
	#	command_left = chr(0xC1)
	#	command_right = chr(0xCA)
   	#	ser.write(command_left)
  	#	ser.write(chr(speed))
   	#	ser.write(command_right)
   	#	ser.write(chr(speed))

	#def turn_left(speed):
	#	command_left = chr(0xC2)
	#	command_right = chr(0xC9)
	#	ser.write(command_left)
	#	ser.write(chr(speed))
	#	ser.write(command_right)
	#	ser.write(chr(speed))
 




#def control(data):
#	output = StringIO.StringIO()
#	output.write(data);
#	data = float(output.getvalue().split()[1]);
#	return data


#rospy.Subscriber("control_effort", Float64, bigfn)
#rospy.Subscriber("control_topic", Int32, control)
#rospy.spin()
 
if __name__ == '__main__':
	try:
		reverse = sys.argv[1]
		sides= sys.argv[2]
		y = control()
		y.run()
	except rospy.ROSInterruptException:
		pass

	

