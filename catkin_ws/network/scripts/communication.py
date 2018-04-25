#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

#export ROS_IP=192.168.243.5
#export ROS_MASTER=192.168.243.5
#export ROS_MASTER_URI=http://$ROS_MASTER:11311

import rospy
import sys
from std_msgs.msg import String

def send_target(data):
    data.data = "target " + data.data
    rospy.loginfo("I sent: %s",data.data)
    pub_my_out.publish(data)

def send_message(data):
    data.data = "message " + data.data
    rospy.loginfo("I sent: %s",data.data)
    pub_my_out.publish(data)

def send_status(data):
    data.data = "status " + data.data
    rospy.loginfo("I sent: %s",data.data)
    pub_my_out.publish(data)

def rec_func(data):
    rospy.loginfo("I heard: %s",data.data)
    words = data.data.split()
    received =  " ".join(words[1:])
    if words[0] == "target":
        pub_target.publish(received)
    elif words[0] == "message":
        pub_message.publish(received)
    elif words[0] == "status":
        pub_status.publish(received)

def listener(other_out):

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.Subscriber(other_out, String, rec_func)

    rospy.Subscriber('my_target', String, send_target)
    rospy.Subscriber('my_message', String, send_message)
    rospy.Subscriber('my_status', String, send_status)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    if sys.argv[1]=="1":
        print ("Im master")
        my_out= "out_1"
        other_out= "out_2"
    else:
        print ("Im client")
        my_out= "out_2"
        other_out= "out_1"
        

    pub_my_out = rospy.Publisher(my_out, String, queue_size=10)
    
    pub_target = rospy.Publisher('other_target', String, queue_size=10)
    pub_message = rospy.Publisher('other_message', String, queue_size=10)
    pub_status = rospy.Publisher('other_status', String, queue_size=10)

    rospy.init_node('comm', anonymous=True)
    listener(other_out)
