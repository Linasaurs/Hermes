#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
import numpy
import StringIO

'''cm_right_top =0
cm_right_bottom =0

def callback_right_top(data):
	global cm_right_top
	cm_right_top = float(data.data);

	
def callback_right_bottom(data):
	global cm_right_top
	global cm_right_bottom 
	cm_right_bottom = float(data.data);
	cm_average = (cm_right_top+cm_right_bottom)/2.0;
	rospy.loginfo("-----------");
	rospy.loginfo("TOP:" + str(cm_right_top));
	rospy.loginfo("BOTTOM:" + str(cm_right_bottom));
	rospy.loginfo("AVG:" + str(cm_average));
	pub.publish(cm_right_bottom)'''
	
def callback_right(data):
	pub.publish (float(data.data));

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('traverse_pid', anonymous=True)

    rospy.Subscriber("sonic_right", String, callback_right)   

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
	pub = rospy.Publisher('state', Float64, queue_size=10)
	listener()
