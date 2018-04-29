#!/usr/bin/env python
import pyttsx
import rospy
from std_msgs.msg import String

def read(data):
	engine = pyttsx.init()
	engine.setProperty('rate', 100)
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[2].id) #change index to change voices
	engine.say(data.data)
	engine.runAndWait()	
	pub.publish ("done");

def listener():

    rospy.Subscriber("read_aloud", String, read)   
    rospy.spin()

if __name__ == '__main__':
	rospy.init_node('tts', anonymous=True)
	pub = rospy.Publisher('read_aloud_done', String, queue_size=10)
	listener()
