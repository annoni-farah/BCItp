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
	pub=rospy.Publisher('manager_smp', Float64MultiArray, queue_size=3000)
	msg=Float64MultiArray()
	msg.data=np.arange(num_channels)
	zero_time = rospy.Time()
	t=np.float64(0.0)
	num=1
	rate = rospy.Rate(250)

	while num!=0:
		msg.data=np.array([0]*num_channels)
		pub.publish(msg)
		num-=1		
		rate.sleep()
		valor=0
	while not rospy.is_shutdown():
		#msg.data=np.array([uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1),uniform(-0.1,0.1)])
		msg.data=np.array([valor,valor,valor,valor,valor,valor,valor,valor])
		valor+=1
		if valor == 250*9:
			valor=0		
		pub.publish(msg)
		rate.sleep()

testedatamanager()
