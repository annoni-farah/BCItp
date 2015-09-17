#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray

tamanho_do_buffer = 1000     #define tamanho do buffer

class meubuffer:           #classe para criacao do buffer
    def __init__(self,tamanho_max): #inicializazao do buffer com seu tamanho maximo como argumento
        self.max = tamanho_max
        self.data = []
    def append(self,x):    #adiciona array de elementos ao buffer, elemento unitario necessita de []
        self.data=np.hstack((self.data,x))
        if len(self.data) > self.max:
            self.data = np.delete(self.data,np.arange(0,len(x)))
    def get(self):         #retorna os elementos do buffer
        return self.data 

def callback(data):        #callback do subscriber
    #global pub2
    buffer.append([data.data])
    #pub2.publish(data=buffer.get())

def second():
    #global pub2
    rospy.init_node('second', anonymous=True)
    rospy.Subscriber("canal1",Float64,callback,queue_size=1)
    pub2=rospy.Publisher('canal2', Float64MultiArray, queue_size=1)
    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        #rospy.get_time()
        pub2.publish(data=buffer.get())
	rate.sleep()
    rospy.spin()
    
if __name__ == '__main__':
    buffer = meubuffer(tamanho_do_buffer)    #cria o buffer para as amostras recebidas
    second()
