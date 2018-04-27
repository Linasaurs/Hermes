#!/usr/bin/env python
import zmq
import rospy
import sys
from std_msgs.msg import String

context = zmq.Context()
socket_send = context.socket(zmq.PUB)
socket_rec = context.socket(zmq.SUB)

def send_target(data):
    global socket_send
    data.data = "target " + data.data
    rospy.loginfo("I sent: %s",data.data)
    socket_send.send("%s" % data.data)

def send_message(data):
    global socket_send
    data.data = "message " + data.data
    rospy.loginfo("I sent: %s",data.data)
    socket_send.send("%s" % data.data)

def send_status(data):
    global socket_send
    data.data = "status " + data.data
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
    elif words[0] == "status":
        pub_status.publish(received)

def listener(other_out):
    global socket_rec
    while True:
        message= socket_rec.recv()
        rec_func(message)
    
if __name__ == '__main__':
    global socket_send
    global socket_rec
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
    pub_status = rospy.Publisher('other_status', String, queue_size=10)

    rospy.Subscriber('my_target', String, send_target)
    rospy.Subscriber('my_message', String, send_message)
    rospy.Subscriber('my_status', String, send_status)

    listener(other_ip)
