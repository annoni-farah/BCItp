from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from standards import FONT_SIZE, BUTTON_SIZE
import os


class DroneMenu(Screen):
    # layout

    def __init__(self, session_header, **kwargs):
        super(DroneMenu, self).__init__(**kwargs)

        self.sh = session_header

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.5,
                         padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(
            text="ARDrone Control Menu", font_size=FONT_SIZE)

        button_start = Button(text="Start", size=BUTTON_SIZE)
        button_start.bind(on_press=self.change_to_acquisition)

        button_simulator = Button(text="Start Simulator", size=BUTTON_SIZE)
        button_simulator.bind(on_press=self.start_simulator)

        button_settings = Button(text="Settings", size=BUTTON_SIZE)
        button_settings.bind(on_press=self.change_to_calsettings)

        button_back = Button(text="Back", size=BUTTON_SIZE)
        button_back.bind(on_press=self.change_to_cal)

        box1.add_widget(self.label_msg)

        box1.add_widget(button_start)
        box1.add_widget(button_simulator)
        box1.add_widget(button_settings)
        box1.add_widget(button_back)

        self.add_widget(box1)

    def change_to_acquisition(self, *args):
        self.manager.current = 'DroneStart'
        self.manager.transition.direction = 'left'

    def change_to_calsettings(self, *args):
        self.manager.current = 'DroneSettings'
        self.manager.transition.direction = 'left'

    def change_to_cal(self, *args):
        self.manager.current = 'GameMenu'
        self.manager.transition.direction = 'right'

    def start_simulator(self, *args):
        PATH_TO_ROS = '/home/rafael/codes/tum_simulator_ws/devel/setup.bash'

        os.system('roslaunch ardrone_tutorials \
            keyboard_controller_simu_goal.launch &')