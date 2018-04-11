
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

ros::NodeHandle  nh;


std_msgs::String str_msg;
ros::Publisher chatter("arduino", &str_msg);
Ping s_TL = Ping(12,0,0);
Ping s_BL = Ping(13,0,0);
char buffer[80];

void setup()
{
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.advertise(chatter);
}

void loop()
{
  s_TL.fire();
  int cm_TL = s_TL.centimeters();
  snprintf(buffer,sizeof("TL "),"%s","TL ");
  snprintf(&buffer[3],sizeof(buffer),"%d",cm_TL);
  str_msg.data = buffer;
  chatter.publish( &str_msg );
  
  s_BL.fire();  
  int cm_BL = s_BL.centimeters();  
  snprintf(buffer,sizeof("BL "),"%s","BL ");
  snprintf(&buffer[3],sizeof(buffer),"%d",cm_BL);
  str_msg.data = buffer;
  chatter.publish( &str_msg );
  
  delay(100);
  nh.spinOnce();
}

