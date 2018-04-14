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
		self.cn = 70
		self.yaw = 0
		self.read_yaw = 0
		self.maxvalue = 400.0
		self.standardspeed = 50.0
		self.stp = 0;
	
		rospy.init_node('move_dagu', anonymous=True)
		rospy.Subscriber("control_effort", Float64, self.bigfn)
		rospy.Subscriber("control_topic", Int32, self.control)
		rospy.Subscriber("yaw_topic", Float64, self.ret_yaw)
		rospy.Subscriber("debug_signal", String, self.get_debug_signal)

		#rospy.init_node('control', anonymous=True)
		#self.pub = rospy.Publisher('control_topic', Int32, queue_size=10)
		#rospy.Subscriber("distance_to_box", Int32, self.distance_to_box)
		#rospy.Subscriber("arrow_direction", Int32, self.arrow_direction)
		
		self.run()
 
	def backward(self, speed):
		command_left = chr(0xC2)
		command_right = chr(0xCA)
		ser.write(command_left)
		ser.write(chr(speed))
		ser.write(command_right)
		ser.write(chr(speed))
 
	def forward(self, speed):
		command_left = chr(0xC1)
		command_right = chr(0xC9)
		ser.write(command_left)
		ser.write(chr(speed))
		ser.write(command_right)
		ser.write(chr(speed))
 
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
	
	def run(self):
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			if (self.stp == 1):
				self.stop()
				break
			rospy.loginfo('control signal: ' +str(self.cn))
			#while (self.read_yaw==0):
			#		xyzsdff=0
			starting_yaw = self.yaw
			if self.cn == 0:					#Move forward towards box --Left
				if self.move < 0:
					#self.move = -self.move
					#self.turn_left(int(self.standardspeed * self.move/self.maxvalue))
					speed = int(self.standardspeed)
					turn = int(self.standardspeed + interp(self.move,[-126,0],[0,50] ))


					rospy.loginfo('Left ')
					rospy.loginfo('speed: ' +str(self.standardspeed))
					rospy.loginfo('Turn: ' + str(int(turn)))
					rospy.loginfo('Move: ' +str(self.move))
		
					command_left = chr(0xC1)
					command_right = chr(0xC9)
					ser.write(command_left)
					ser.write(chr(speed))
					ser.write(command_right)
					ser.write(chr(turn))

				elif self.move > 0:				#Move forward towards box --Right
					#self.turn_right(int(self.standardspeed * self.move/self.maxvalue))
					speed = int(self.standardspeed)
					turn = int(self.standardspeed + interp(self.move,[0,126],[50,255] ))
					
					rospy.loginfo('Right ')
					rospy.loginfo('Speed: ' +str(self.standardspeed))
					rospy.loginfo('Turn: ' +str(int(turn)))
					rospy.loginfo('Move: ' + str(self.move))
		
					command_left = chr(0xC1)
					command_right = chr(0xC9)
					ser.write(command_left)
					ser.write(chr(turn))
					ser.write(command_right)
					ser.write(chr(speed))

				else :
					self.forward(int(self.standardspeed))
					rospy.loginfo('Move: ' +str(self.move))

			elif self.cn == 1 :							#Rotate Left
				print starting_yaw
				if self.yaw > -90 and self.yaw < -1:
					while self.yaw < 0 :
						self.rotate_left(35)
					while  abs(self.yaw - 0) < 90 - abs(starting_yaw-0) :
						self.rotate_left(35)
				elif self.yaw > 89 and self.yaw < 179 :
					#while self.yaw < 179 or self.yaw > 0 :
					while self.yaw > 0 :
						self.rotate_left(35)
					
					while abs(self.yaw + 179) < 90 - abs(179 - starting_yaw) :
						self.rotate_left(35)
				else :
					while abs(self.yaw - starting_yaw) < 90 :
						self.rotate_left(35)

				self.stop()
				#rospy.sleep(2)
				print self.yaw
				#rospy.sleep(3000)
				
				#while abs(self.yaw - starting_yaw) < 90.0:
					#print self.yaw
				#	self.rotate_left(50)
				'''				
				if 	starting_yaw<-135.0:
					while abs(self.yaw - starting_yaw) < 270.0:
						self.rotate_left(50)		
				else:
					while abs(self.yaw - starting_yaw) < 90.0:
						self.rotate_left(50)
				'''
				
				#rospy.loginfo('completed left turn')
				#print self.yaw

			elif self.cn == 2 :							#Rotate Right


				print starting_yaw
				if self.yaw < 90 and self.yaw > 1:
					while self.yaw > 0 :
						self.rotate_right(35)
					while abs(self.yaw - 0) < 90 - abs(starting_yaw - 0) :
						self.rotate_right(35)
				elif self.yaw < -89 and self.yaw > -178:
					#while self.yaw > -177 and self.yaw < 0:
					while self.yaw < 0 :
						self.rotate_right(35)
					while abs(179 - self.yaw) < 90 - abs(179 + starting_yaw) :
						self.rotate_right(35)
				else :
					while abs(self.yaw - starting_yaw) < 90 :
						self.rotate_right(35)
				
				self.stop()
				#rospy.sleep(2)
				print self.yaw
				#rospy.sleep(3000)
				
				#while abs(self.yaw - starting_yaw) < 90.0:
					#print self.yaw
				#	self.rotate_left(50)
				'''				
				if 	starting_yaw<-135.0:
					while abs(self.yaw - starting_yaw) < 270.0:
						self.rotate_left(50)		
				else:
					while abs(self.yaw - starting_yaw) < 90.0:
						self.rotate_left(50)
				'''
				
				#rospy.loginfo('completed left turn')
				#print self.yaw
				#rospy.sleep(3000)

				#while abs(self.yaw - starting_yaw) < 87.0:
				#	self.rotate_left(50)
								
				#if 	starting_yaw>135.0:
				#	while self.yaw - starting_yaw < -270.0 or self.yaw>0:
				#		print self.yaw
				#		self.rotate_right(50)		
				#else:
				#	while abs(self.yaw - starting_yaw) < 90.0:
					#	self.rotate_right(50)

				
				#rospy.loginfo('completed right turn')
				#print self.yaw
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
		y = control()
	except rospy.ROSInterruptException:
		pass

	

