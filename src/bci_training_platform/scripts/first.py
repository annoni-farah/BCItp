#!/usr/bin/env python
from __future__ import division
import rospy
import numpy as np
import scipy.signal as sg
import random
from std_msgs.msg import Float64

def first():
    rospy.init_node('first', anonymous=True)
    pub=rospy.Publisher('canal1', Float64, queue_size=1)
    fs=250
    t=0.0
    freq=2*np.pi*8
    rate = rospy.Rate(fs)
    while not rospy.is_shutdown():
        sinal = np.sin(freq*t)
        #rospy.get_time()
        pub.publish(sinal)
	t=t+(1/fs)
        rate.sleep()

if __name__ == '__main__':
    try:
        first()
    except rospy.ROSInterruptException:
        pass
