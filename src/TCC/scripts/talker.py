#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy as np
import scipy.signal as sg
import random
from std_msgs.msg import Float64MultiArray

def talker():
    pub2 = rospy.Publisher('canal1', Float64MultiArray, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(0.5) # 10hz
    t=np.arange(0,0.5,0.004)
    fs = 250
    while not rospy.is_shutdown():
        f1 = random.randrange(0,9,1)
        f2 = random.randrange(15,30,2)
        sinal = np.sin(2*np.pi*f1*t)+np.sin(2*np.pi*f2*t)
        rospy.get_time()
        hello_str = Float64MultiArray(data=sinal) 
        pub2.publish(hello_str)
	#print(sinal)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
