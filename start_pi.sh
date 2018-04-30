#!/bin/bash
gnome-terminal --window-with-profile=keep -e "roscore"
sleep 2
gnome-terminal --window-with-profile=keep -e "rosrun network communication.py $1 $2"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun speech tts.py"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun vision ocr.py"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun rosserial_python serial_node.py /dev/ttyACM0 _baud:=115200"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun traverse imu.py"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun imu_filter_madgwick imu_filter_node _use_mag:=false"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun traverse getyaw.py"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun pid controller _Kp:=$3 _Kd:=$4 _upper_limit:=126 _lower_limit:=-126"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rostopic pub /setpoint std_msgs/Float64 $5"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun traverse pid.py"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun traverse control.py $6"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun traverse move.py $7 $8 $9"

