#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray, MultiArrayDimension, String

num_channels=4
num_samples=250
X=np.matrix([[0]*num_channels]*num_samples).T

def callback(msg_received):
	global X
	X=np.hstack((X,np.matrix(msg_received.data).T))
	X=np.delete(X,0,1)
	
def bloco2():
	rospy.init_node('Buffer', anonymous=True)
	rospy.Subscriber('canal1',Float64MultiArray,callback,queue_size=1)
	pub=rospy.Publisher('canal2', Float64MultiArray, queue_size=1)
	print('Bloco2')
	msg_to_send = Float64MultiArray()
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		msg_to_send.data = X.A1
		pub.publish(msg_to_send)	
		rate.sleep()
	rospy.spin()

bloco2()
