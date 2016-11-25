import rospy
import tf
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates

from time import sleep
from math import pi
import sys
import matplotlib.pyplot as plt
import numpy as np

COMMAND_PERIOD = 10  # ms
Kp = 0.005

yaw_h = []
error_h = []
ctrl_h = []

REF = float(sys.argv[1])


def send_cmd(yaw):
    # The previously set command is then sent out periodically if the drone
    # is flying
    command = Twist()
    command.angular.z = yaw

    pub_vel.publish(command)


def get_nav_data(data):

    q_x = data.pose[10].orientation.x
    q_y = data.pose[10].orientation.y
    q_z = data.pose[10].orientation.z
    q_w = data.pose[10].orientation.w
    quaternion = (
        q_x,
        q_y,
        q_z,
        q_w)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    yaw = (euler[2] * 180 / pi) + 180  # offset to avoid - numbers

    yaw_h.append(yaw)
    print yaw
    generate_cmd(yaw)


def generate_cmd(pos):

    if (pos <= 90) and (REF >= 270):
        pos += 360

    error = REF - pos
    if abs(error) > 180:
        error = -error

    error_h.append(error)

    ctrl = Kp * (error)

    if ctrl > 1:
        ctrl = 1
    elif ctrl < -1:
        ctrl = -1

    ctrl_h.append(ctrl)
    send_cmd(ctrl)


def plot_data():
    ref = np.empty(len(yaw_h))
    ref[:] = REF
    plt.subplot(3, 1, 1)
    plt.plot(ref, label='Ref', linewidth=3.0)
    plt.plot(yaw_h, label='yaw')
    plt.grid(True)
    # plt.axis([0, len(ref), 0, 360])
    plt.legend(loc=0)

    plt.subplot(3, 1, 2)
    plt.plot(error_h, 'r', label='Error', linewidth=3.0)
    plt.grid(True)
    # plt.axis([0, len(ref), 0, 360])
    plt.legend(loc=0)

    plt.subplot(3, 1, 3)
    plt.plot(ctrl_h, 'g', label='Ctrl', linewidth=3.0)
    plt.grid(True)
    # plt.axis([0, len(ref), 0, 360])
    plt.legend(loc=0)

    plt.show()

rospy.init_node('pilot', anonymous=True)

pub_takeoff = rospy.Publisher(
    '/ardrone/takeoff', Empty, queue_size=1)
pub_land = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
pub_reset = rospy.Publisher('/ardrone/reset', Empty, queue_size=1)

pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rospy.Subscriber("/gazebo/model_states", ModelStates,
                 get_nav_data)

# pub_reset.publish()
send_cmd(0)

try:
    while not rospy.is_shutdown():
        pass
except Exception as e:
    raise
else:
    pass
finally:
    pub_land.publish()
    plot_data()
