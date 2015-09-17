#!/usr/bin/env python
import rospy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from std_msgs.msg import Float64MultiArray

dados = []
def callback(data):        #callback do subscriber
    global dados
    dados=data.data

def animate(i):
    global dados
    ax1.clear()
    ax1.plot(dados)

def fourth():
    rospy.init_node('fourth', anonymous=True)
    rospy.Subscriber("canal3",Float64MultiArray,callback,queue_size=1)
    ani = animation.FuncAnimation(fig, animate, interval=400)
    plt.show()
    
if __name__ == '__main__':
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    fourth()
