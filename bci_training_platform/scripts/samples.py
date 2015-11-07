#!/usr/bin/env python
from __future__ import division
from random import uniform
import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray, MultiArrayDimension, String

num_channels=8
on_control=False

def control(msg_received):
	global on_control
	if msg_received.data == "on_bloco1":
		on_control=True		
	
def testedatamanager():
	rospy.init_node('samples', anonymous=True)
	pub=rospy.Publisher('manager_smp', Float64MultiArray, queue_size=0)
	msg=Float64MultiArray()
	msg.data=np.arange(num_channels)
	t=np.float64(0.0)
	num=1
	rate = rospy.Rate(250)

	while num!=0:
		msg.data=np.array([0]*num_channels)
		pub.publish(msg)
		num-=1		
		rate.sleep()

	while not rospy.is_shutdown():
		msg.data=np.array([uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1)])
		pub.publish(msg)
		rate.sleep()

testedatamanager()
