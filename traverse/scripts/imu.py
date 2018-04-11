#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
import time
import subprocess

avg = [0.0,0.0,0.0,0.0,0.0,0.0]
n = 0.0
offsets = [1837.888211382114, -499.4298780487803, 16762.12499999997, 632.4268292682917, -1056.0264227642276, -731.7530487804876]
offsets2  = [0.018825897995472227, 0.02559175123121882, 9.64760500518690455, -0.0002963544882052582, 0.004527733771368361, 0.0007225744973561952]

def callback(data):
    global n
    global avg
    global offsets
    s = data.data.split()
    imu = Imu()
    imu.header.frame_id = "imu_link"
    imu.header.stamp = rospy.Time.now()
    imu.angular_velocity.x=((float(s[3])-offsets[3])*8.75*0.0174533/1000.0) - offsets2[3]
    imu.angular_velocity.y=((float(s[4])-offsets[4])*8.75*0.0174533/1000.0) - offsets2[4]
    imu.angular_velocity.z=((float(s[5])-offsets[5])*8.75*0.0174533/1000.0) - offsets2[5]
    imu.linear_acceleration.x=((float(s[0])-offsets[0])*9.80665*0.061/1000.0) - offsets2[0]
    imu.linear_acceleration.y=((float(s[1])-offsets[1])*9.80665*0.061/1000.0) - offsets2[1]
    imu.linear_acceleration.z=((float(s[2])-offsets[2])*9.80665*0.061/1000.0) - offsets2[2]
    imu.orientation_covariance[0]=-1
    pub.publish(imu)
   

    '''avg[0]=(avg[0]*n+float(s[0]))/(n+1.0)
    avg[1]=(avg[1]*n+float(s[1]))/(n+1.0)
    avg[2]=(avg[2]*n+float(s[2]))/(n+1.0)
    avg[3]=(avg[3]*n+float(s[3]))/(n+1.0)
    avg[4]=(avg[4]*n+float(s[4]))/(n+1.0)
    avg[5]=(avg[5]*n+float(s[5]))/(n+1.0)

    n=n+1

    print avg'''
    
    '''avg[0]=(avg[0]*n+imu.linear_acceleration.x)/(n+1.0)
    avg[1]=(avg[1]*n+imu.linear_acceleration.y)/(n+1.0)
    avg[2]=(avg[2]*n+imu.linear_acceleration.z)/(n+1.0)
    avg[3]=(avg[3]*n+imu.angular_velocity.x)/(n+1.0)
    avg[4]=(avg[4]*n+imu.angular_velocity.y)/(n+1.0)
    avg[5]=(avg[5]*n+imu.angular_velocity.z)/(n+1.0)

    n=n+1

    print avg'''

    #print imu.linear_acceleration.x,imu.linear_acceleration.y,imu.linear_acceleration.z,imu.angular_velocity.x, imu.angular_velocity.y, imu.angular_velocity.z 

 

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('imuListener', anonymous=True)

    rospy.Subscriber("imuArduino", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    pub = rospy.Publisher('imu/data_raw', Imu, queue_size=10)
    listener()
