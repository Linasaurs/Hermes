#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
import numpy
import StringIO

def callback(data):
	data = float(data.data);
	rospy.loginfo(data)
	pub.publish(data)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('traverse_pid', anonymous=True)

    rospy.Subscriber("arduino", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
	pub = rospy.Publisher('state', Float64, queue_size=10)
	listener()
