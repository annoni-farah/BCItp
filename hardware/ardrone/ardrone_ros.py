import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates

from std_srvs.srv import Empty as srv_Empty

COMMAND_PERIOD = 100  # ms


class ARDrone():

    def __init__(self):

        rospy.init_node('pilot', anonymous=True)

        self.pub_takeoff = rospy.Publisher(
            '/ardrone/takeoff', Empty, queue_size=1)
        self.pub_land = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
        self.pub_reset = rospy.Publisher('/ardrone/reset', Empty, queue_size=1)

        # Gazebo Reset Simulator
        self.reset_world = rospy.ServiceProxy('/gazebo/reset_world', srv_Empty)

        rospy.Subscriber("/gazebo/model_states", ModelStates,
                         self.update_position)

        # self.pub_cmd = rospy.Publisher('/cmd_vel',Twist, 1)
        self.pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        self.command = Twist()
        self.commandTimer = rospy.Timer(rospy.Duration(
            COMMAND_PERIOD / 1000.0), self.send_cmd)

        self.pos_x = 0
        self.pos_y = 0

        rospy.on_shutdown(self.land)

    def takeoff(self):
        self.pub_takeoff.publish()

    def land(self):
        self.pub_land.publish()

    def reset(self):
        self.pub_reset.publish()
        self.reset_world()

    def set_cmd(self, pitch=0, turn=0):
        # Called by the main program to set the current command
        self.command.linear.x = pitch
        self.command.angular.z = turn

    def send_cmd(self, event):
        # The previously set command is then sent out periodically if the drone
        # is flying
        self.pub_vel.publish(self.command)

    def update_position(self, data):

        self.pos_x = data.pose[10].position.x
        self.pos_y = data.pose[10].position.y


if __name__ == '__main__':
    drone = ARDrone()
    drone.land()
    drone.set_cmd(1, 0)
    while True:
        print drone.pos_x
