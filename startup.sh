#!/bin/bash
roscore &
sleep 2
roslaunch jetson_csi_cam jetson_csi_cam.launch width:=640 height:=360 fps:=16 &
sleep 0.5
rosrun rosserial_python serial_node.py /dev/ttyACM0 _baud:=115200 &
sleep 0.5
python ./miniproject_src/imu/imuArepublisher.py &
sleep 0.5
rosrun imu_filter_madgwick imu_filter_node _use_mag:=false &
sleep 0.5
python ./miniproject_src/imu/getyaw.py &
sleep 0.5
python ./miniproject_src/vision/newvision2.py &
sleep 0.5
python ./miniproject_src/lidar_distance/lidar_distance.py &
sleep 0.5
rosparam set /pid_node/Kp 0.7 &
sleep 0.5
rosrun pid controller &
sleep 0.5
rostopic pub /setpoint std_msgs/Float64 0 &
sleep 0.5
rosrun test_python control.py &
echo "!!! end of startup.sh"
