#!/usr/bin/env python
PKG = 'numpy_tutorial'
import roslib; roslib.load_manifest(PKG)

import rospy
from numpy_tutorial.msg import float64 
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Float64MultiArray
import numpy

def talker():
    pub = rospy.Publisher('canal', float64,queue_size=10)
    rospy.init_node('talker', anonymous=True)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub.publish([1,2,3])
        r.sleep()

if __name__ == '__main__':
    talker()
