#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import pygame, sys
from pygame.locals import *

def talker():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((100, 100))
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker2', anonymous=0)
    rate = rospy.Rate(120) # 10hz
    while not rospy.is_shutdown():
        w8_str = "Waiting... %s" % rospy.get_time()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_RIGHT or event.key == K_d):
                    cmd_str = "right"
                    rospy.loginfo(cmd_str)
                    pub.publish(cmd_str)
        rate.sleep()

def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass




              
