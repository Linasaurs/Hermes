#!/bin/bash
trap "kill 0" EXIT
gnome-terminal --window-with-profile=keep -e "roscore"
sleep 2
gnome-terminal --window-with-profile=keep -e "roslaunch jetson_csi_cam jetson_csi_cam.launch width:=640 height:=360 fps:=16"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun rosserial_python serial_node.py /dev/ttyACM0 _baud:=115200"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun traverse imu.py"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun imu_filter_madgwick imu_filter_node _use_mag:=false"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun traverse getyaw.py"
#sleep 0.5
#gnome-terminal --window-with-profile=keep -e python "./miniproject_src/vision/newvision2.py"
sleep 0.5
rosparam set /pid_node/Kp $1
rosparam set /pid_node/Kd $2
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun pid controller"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rostopic pub /setpoint std_msgs/Float64 30"
sleep 0.5
gnome-terminal --window-with-profile=keep -e "rosrun test_python control.py"
echo "!!! end of startup.sh"
wait
