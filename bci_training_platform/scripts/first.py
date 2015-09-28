#!/usr/bin/env python
from __future__ import division
import rospy
import numpy as np
from std_msgs.msg import Float64

""" PARAMETROS """
FS   = 250                         
FREQ = 2*np.pi*12

""""""""""""""""""

def first():
	rospy.init_node('first', anonymous=True)
	pub=rospy.Publisher('canal1', Float64, queue_size=1)
	rate = rospy.Rate(FS)
	t=np.float64(0)
	while not rospy.is_shutdown():
		#sinal = np.sin(FREQ*rospy.get_time())
		sinal = np.sin(FREQ*t)
		pub.publish(sinal)
		t=t + 1/FS
		rate.sleep()
    
if __name__ == '__main__':
	try:
		first()
	except rospy.ROSInterruptException:
		pass
