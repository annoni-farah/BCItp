#!/usr/bin/env python
from __future__ import division
import rospy
import numpy as np
import scipy.signal as sg
from std_msgs.msg import Float64MultiArray

from threading import Thread as Th
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fs=250
n_order=100
f1_2=[8,30]
b = sg.firwin(n_order,f1_2,pass_zero=False,window='blackman',nyq=fs/2) 

temp1=[]
temp2=[]
flag=0
plot=0
def callback(data):
    global temp1,temp2,flag,pub3
    temp1 = sg.convolve(data.data,b,mode='full')
    if flag==0:
        flag=1
        temp2=temp1
        pub3.publish(data=temp2)
	flag=0

def third():
    global pub3
    rospy.init_node('third', anonymous=True)
    rospy.Subscriber('canal2', Float64MultiArray, callback,queue_size=1)
    pub3=rospy.Publisher('canal3', Float64MultiArray, queue_size=1)
    rospy.spin()
    

if __name__ == '__main__':
    third()







