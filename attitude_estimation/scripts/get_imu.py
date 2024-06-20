#!/usr/bin/env python3

import rospy
from sensor_msgs_ext.msg import gyroscope, accelerometer, magnetometer
from geometry_msgs.msg import Vector3
from attitude_estimation.msg import ImuData
import message_filters

class ImuListener:
    def __init__(self):
        rospy.init_node('imu_listener', anonymous=True)
        rospy.loginfo("IMU Listener Node Initialized")

        self.acc_sub = message_filters.Subscriber("/imu/accelerometer", accelerometer)
        self.gyro_sub = message_filters.Subscriber("/imu/gyroscope", gyroscope)
        self.mag_sub = message_filters.Subscriber("/imu/magnetometer", magnetometer)

        self.ts = message_filters.ApproximateTimeSynchronizer(
            [self.acc_sub, self.gyro_sub, self.mag_sub], 
            queue_size=10, 
            slop=0.1,
            allow_headerless=True  # 允许无头消息
        )
        self.ts.registerCallback(self.callback)
        rospy.loginfo("Subscribers and Time Synchronizer Initialized")

        self.pub = rospy.Publisher('/imu_data', ImuData, queue_size=10)
        rospy.loginfo("Publisher Initialized")

    def callback(self, acc_data, gyro_data, mag_data):
        rospy.loginfo("Callback triggered")
        imu_data = ImuData()
        imu_data.acc = acc_data
        imu_data.gyro = gyro_data
        imu_data.mag = mag_data

        self.pub.publish(imu_data)
        rospy.loginfo("Published IMU Data")

if __name__ == '__main__':
    try:
        print("start collect datas")
        imu_listener = ImuListener()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

