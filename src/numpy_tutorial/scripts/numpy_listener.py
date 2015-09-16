#!/usr/bin/env python
PKG = 'numpy_tutorial'
import roslib; roslib.load_manifest(PKG)

import rospy
from std_msgs.msg import Float64MultiArray

def callback(data):
    print rospy.get_name(), "I heard %s"%str(data.data)

def listener():
    rospy.init_node('listener')
    rospy.Subscriber('canal', Float64MultiArray, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

