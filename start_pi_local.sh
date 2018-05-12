#!/bin/bash
# to ssh without password
# ssh-keygen
# ssh-copy-id remote_user@remote_ip
if [ $1 = "help" ]
then
    echo "my_ip other_ip kp kd side_distance front_distance reverse? sides forward_speed"
else
    CMD="rosrun network communication.py $1 $2"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="roslaunch usb_cam usb_cam-test.launch"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun vision shape.py pi"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun vision face_detect.py pi"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun speech tts.py"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun vision ocr.py"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun rosserial_python serial_node.py /dev/ttyACM0 _baud:=115200"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun traverse imu.py"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun imu_filter_madgwick imu_filter_node _use_mag:=false"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun traverse getyaw.py"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun pid controller _Kp:=$3 _Kd:=$4 _upper_limit:=126 _lower_limit:=-126"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    #Jetson, upstairs, kp=1.4, kd=4.0
    #Pi, downstairs, kp=1.4, kd =3.2
    sleep 0.5
    CMD="rostopic pub /setpoint std_msgs/Float64 $5"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun traverse pid.py"
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun traverse control.py $6" #distance_threshold
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
    sleep 0.5
    CMD="rosrun traverse move.py $7 $8 $9" #reverse, sides, speed
    gnome-terminal --window-with-profile=keep -e "echo '$CMD'; '$CMD'"
fi
