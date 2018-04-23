#!/usr/bin/env python
import getch
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
from move import * 
from termios import tcflush, TCIFLUSH
import sys

ser = serial.Serial('/dev/ttyS0', 19200, timeout = 1)

hand = control()
cc = 'x'

while True:
    c = getch.getch()
    if  c == 'w' and c != cc:
        cc =c
        hand.move_forward()
    elif  c == 'w' and c != cc:
        cc =c
        hand.move_forward()
    elif  c == 'a' and c != cc:
        cc =c
        hand.move_left()
    elif  c == 'a' and c != cc:
        cc =c
        hand.move_right()
    elif  c == 's' and c != cc:
        cc =c
        hand.stop()
    elif  c == 'q' and c != cc:
        cc =c
        hand.stop()
        break
	elif c == 'b' and c!=cc:
		cc=c
		hand.backward(50)

