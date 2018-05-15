# Hermes

## Introduction

Hermes is a system for delivering messages to
individuals that exist in a certain environment, e.g. employees in their offices,
elderly in a nursing home, etc. The employees are identified by face by going through face detection of known faces database. The Dagus serves as a messenger that first receives a paper message from a mailbox which contains both the message
itself and the name of the receiver. Two Dagus will be responsible for finding the
intended recipient in the different rooms. The first to find the person informs the
other Dagu to stop searching, and then it proceeds to communicate the message to
the person. When the message is successfully delivered the Dagus return back to the
mailbox and wait for other messages.

## Sofware Requirments

1. Python 2
2. ROS Kinetic 
3. And the other pip packages

## ROS Topics List

**Nodes and Their Topics**

**Network, Communication**

Publishes

1. other\_target
2. other\_message
3. other\_found

Subscribes to

1. my\_target
2. my\_message
3. my\_found

**Speech, TTS**

Publishes

1. speak\_done

Subscribes to

1. speak

**Vision, Shape**

Publishes

1. face\_box\_detected

Subscribes to

1. /usb\_cam/image\_raw (Pi) or /csi\_cam/image\_raw (Jetson)

**Vision, Face Detect**

Publishes

1. face\_detected
2. ocr\_file

Subscribes to

1. /usb\_cam/image\_raw (Pi) or /csi\_cam/image\_raw (Jetson)

**Vision,  OCR**

Publishes

1. target\_detected
2. message\_detected

Subscribes to

1. ocr\_file

**Rosserial**

Publishes

1. sonic\_front
2. sonic\_right
3. imuArduino

Subscribes to: None

**Traverse, IMU**

Publishes

1. imu/data\_raw

Subscribes to

1. imuArduino

**IMU\_filter\_madgwick**

Publishes

1. imu/data

Subscribes to

1. imu/data\_raw
2. imu/mag (optional)

**Traverse, Getyaw**

Publishes

1. yaw\_topic

Subscribes to

1. imu/data

**PID, Controller**

Publishes

1. control\_effort

Subscribes to

1. setpoint
2. state
3. pid\_enable

**Traverse, PID**

Publishes

1. state

Subscribes to

1. sonic\_right

**Traverse, Control**

Publishes

1. motion
2. my\_target
3. my\_message
4. my\_found
5. speak
6. turn\_vision\_on

Subscribes to

1. sonic\_front
2. face\_detected
3. target\_detected
4. message\_detected
5. face\_box\_detected
6. message\_box\_detected (not used)
7. other\_target
8. other\_message
9. other\_found
10. speak\_done
11. state\_debug

**Traverse, Move**

Publishes: None

Subscribes to

1. control\_effort
2. motion
3. yaw\_topic
4. debug\_signal
