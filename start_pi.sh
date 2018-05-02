#!/bin/bash
CMD="roscore"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 2
CMD="rosrun network communication.py $2 $3"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun speech tts.py"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun vision ocr.py"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun rosserial_python serial_node.py /dev/ttyACM0 _baud:=115200"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun traverse imu.py"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun imu_filter_madgwick imu_filter_node _use_mag:=false"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun traverse getyaw.py"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun pid controller _Kp:=$4 _Kd:=$5 _upper_limit:=126 _lower_limit:=-126"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
#Jetson, upstairs, kp=1.4, kd=4.0
#Pi, downstairs, kp=1.4, kd =3.2
sleep 0.5
CMD="rostopic pub /setpoint std_msgs/Float64 $6"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun traverse pid.py"
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun traverse control.py $7" #distance_threshold
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"
sleep 0.5
CMD="rosrun traverse move.py $8 $9 ${10}" #reverse, sides, speed
gnome-terminal --window-with-profile=keep -e "ssh -t $1@$2 source ~/.bashrc; echo '$CMD'; '$CMD'"

