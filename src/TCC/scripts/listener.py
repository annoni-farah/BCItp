#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
dados=[]
def callback(data):
    global dados
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    print(data.data)
    dados=data.data

def animate(i):
    global dados
    ax1.clear()
    ax1.plot(dados)
    
def listener():
    global data
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("canal2", Float64MultiArray, callback,queue_size=10)
    #rospy.spin()
    ani = animation.FuncAnimation(fig, animate, interval=10)
    plt.show()
    



if __name__ == '__main__':
    listener()
