#!/usr/bin/env python
import zmq
import rospy
import sys
from std_msgs.msg import String

def send_target(data):
	data.data = "target " + data.data
	rospy.loginfo("I sent: %s",data.data)
	socket_send.send("%s" % data.data)

def send_message(data):
	data.data = "message " + data.data
	rospy.loginfo("I sent: %s",data.data)
	socket_send.send("%s" % data.data)

def send_found(data):
	data.data = "found " + data.data
	rospy.loginfo("I sent: %s",data.data)
	socket_send.send("%s" % data.data)

def rec_func(data):
	rospy.loginfo("I heard: %s",data)
	words = data.split()
	received =  " ".join(words[1:])
	if words[0] == "target":
		pub_target.publish(received)
	elif words[0] == "message":
		pub_message.publish(received)
	elif words[0] == "found":
		pub_found.publish(received)

def listener():
	while True:
		message= socket_rec.recv()
		rec_func(message)
	
if __name__ == '__main__':
	context = zmq.Context()
	socket_send = context.socket(zmq.PUB)
	socket_rec = context.socket(zmq.SUB)
	my_ip = sys.argv[1]
	port_send= "4444"
	socket_send.bind("tcp://"+my_ip+":%s" % port_send)
	other_ip = sys.argv[2]
	port_rec ="4444"
	socket_rec.setsockopt(zmq.SUBSCRIBE, "")
	socket_rec.connect("tcp://"+other_ip+":%s" % port_rec)

	rospy.init_node('comm', anonymous=True)
  
	pub_target = rospy.Publisher('other_target', String, queue_size=10)
	pub_message = rospy.Publisher('other_message', String, queue_size=10)
	pub_found = rospy.Publisher('other_found', String, queue_size=10)

	rospy.Subscriber('my_target', String, send_target)
	rospy.Subscriber('my_message', String, send_message)
	rospy.Subscriber('my_found', String, send_found)

	listener()
