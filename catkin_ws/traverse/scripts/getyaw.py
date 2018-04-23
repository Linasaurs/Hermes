#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
import tf
from tf import *
import numpy as np

global yaw

def callback(imu):
    explicit_quat = [imu.orientation.x, imu.orientation.y, imu.orientation.z, imu.orientation.w]
    roll, pitch, yaw = tf.transformations.euler_from_quaternion(explicit_quat)
    yaw = yaw *57.2958
    yaw = np.float64(yaw)
    pub.publish(yaw)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('imudatalistener', anonymous=True)
    rospy.Subscriber("imu/data", Imu, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    pub = rospy.Publisher('yaw_topic', Float64, queue_size=10)
    listener()

