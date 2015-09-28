#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray

def chamada(data):
	m=np.matrix(data.data)
	m.shape=(2,3)
	print(m)

def recebe():
	rospy.init_node('recebe', anonymous=True)
	rospy.Subscriber("mecanico",Float64MultiArray,chamada,queue_size=1)
	rospy.spin()

recebe()
