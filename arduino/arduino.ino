
#include <ros.h>

/*
The sensor outputs provided by the library are the raw
16-bit values obtained by concatenating the 8-bit high and
low accelerometer and gyro data registers. They can be
converted to units of g and dps (degrees per second) using
the conversion factors specified in the datasheet for your
particular device and full scale setting (gain).

Example: An LSM6DS33 gives an accelerometer Z axis reading
of 16276 with its default full scale setting of +/- 2 g. The
LA_So specification in the LSM6DS33 datasheet (page 15)
states a conversion factor of 0.061 mg/LSB (least
significant bit) at this FS setting, so the raw reading of
16276 corresponds to 16276 * 0.061 = 992.8 mg = 0.9928 g.
*/
#include <std_msgs/String.h>
#include <Ping.h>

#include <Wire.h>
#include <LSM6.h>

LSM6 imu;


ros::NodeHandle  nh;


std_msgs::String str_msg;
ros::Publisher pub_front("sonic_front", &str_msg);
ros::Publisher pub_right("sonic_right", &str_msg);
ros::Publisher imu_pub("imuArduino", &str_msg);
Ping s_front = Ping(12,0,0);
Ping s_right = Ping(13,0,0);
char buffer[80];

void setup()
{
  Wire.begin();

  if (!imu.init())
  {
    while (1);
  }
  imu.enableDefault();  
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.advertise(pub_front);
  nh.advertise(pub_right);
  nh.advertise(imu_pub);  
}

void loop()
{
  s_front.fire();
  int cm_front = s_front.centimeters();
  snprintf(buffer,sizeof(buffer),"%d",cm_front);
  str_msg.data = buffer;
  pub_front.publish( &str_msg );
  
  s_right.fire();  
  int cm_right = s_right.centimeters();  
  snprintf(buffer,sizeof(buffer),"%d",cm_right);
  str_msg.data = buffer;
  pub_right.publish( &str_msg );
  
  imu.read();

  snprintf(buffer, sizeof(buffer), "%6d %6d %6d %6d %6d %6d",
    imu.a.x, imu.a.y, imu.a.z,
    imu.g.x, imu.g.y, imu.g.z);
  str_msg.data = buffer;
  imu_pub.publish( &str_msg );
  
  delay(100);
  nh.spinOnce();
}

