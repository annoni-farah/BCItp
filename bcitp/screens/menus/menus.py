import os


from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from bcitp.utils.standards import PATH_TO_SESSION
from bcitp.screens.sizes import FONT_SIZE, BUTTON_SIZE

dir_path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(dir_path + '/menus.kv')


class StartScreen(Screen):
    # layout
    session_name = ObjectProperty(None)
    label_msg = StringProperty('')

    def __init__(self, session_header, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        self.sh = session_header

    def change_to_bci(self, *args):

        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'left'

    def save_session_name(self, *args):

        sname = self.session_name.text

        if not os.path.isdir(PATH_TO_SESSION):
            os.makedirs(PATH_TO_SESSION)

        if sname == '':
            # if no session_name is provided, use latest modified folder in
            # data/session
            all_subdirs = []
            for d in os.listdir(PATH_TO_SESSION + '.'):
                bd = os.path.join(PATH_TO_SESSION, d)
                if os.path.isdir(bd):
                    all_subdirs.append(bd)
            sname = max(all_subdirs, key=os.path.getmtime).split('/')[-1]

        self.sh.info.name = sname

        if os.path.isdir(PATH_TO_SESSION + sname):

            self.label_msg = "Session " + sname \
                + " already exists. Data will be overwritten"
            self.sh.loadFromPkl()

        else:
            os.makedirs(PATH_TO_SESSION + sname)
            self.sh.saveToPkl()
            self.label_msg = "Session Saved as: " + sname
            self.sh.info.flag = True


class CalMenu(Screen):
    # layout

    def __init__(self, session_header, **kwargs):
        super(CalMenu, self).__init__(**kwargs)

        self.sh = session_header

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.5,
                         padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="Calibration Menu", font_size=FONT_SIZE)

        button_start = Button(text="Start", size=BUTTON_SIZE)
        button_start.bind(on_press=self.change_to_acquisition)

        button_settings = Button(text="Settings", size=BUTTON_SIZE)
        button_settings.bind(on_press=self.change_to_calsettings)

        button_back = Button(text="Back", size=BUTTON_SIZE)
        button_back.bind(on_press=self.change_to_cal)

        box1.add_widget(self.label_msg)

        box1.add_widget(button_start)
        box1.add_widget(button_settings)
        box1.add_widget(button_back)

        self.add_widget(box1)

    def change_to_acquisition(self, *args):
        self.manager.current = 'CalStart'
        self.manager.transition.direction = 'left'

    def change_to_calsettings(self, *args):
        self.manager.current = 'CalSettings'
        self.manager.transition.direction = 'left'

    def change_to_cal(self, *args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'


class GameMenu(Screen):
    # layout

    def __init__(self, session_header, **kwargs):
        super(GameMenu, self).__init__(**kwargs)
        self.sh = session_header

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.5,
                         padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="Game Menu", font_size=FONT_SIZE)

        button_bars = Button(text="Bars", size=BUTTON_SIZE)
        button_bars.bind(on_press=self.change_to_bars)

        button_target = Button(text="Target", size=BUTTON_SIZE)
        button_target.bind(on_press=self.change_to_target)

        button_ardrone = Button(text="Ardrone", size=BUTTON_SIZE)
        button_ardrone.bind(on_press=self.change_to_ardrone)

        button_settings = Button(text="Settings", size=BUTTON_SIZE)
        button_settings.bind(on_press=self.change_to_gamesettings)

        button_back = Button(text="Back", size=BUTTON_SIZE)
        button_back.bind(on_press=self.change_to_bci)

        box1.add_widget(self.label_msg)

        box1.add_widget(button_bars)
        box1.add_widget(button_target)
        box1.add_widget(button_ardrone)
        box1.add_widget(button_settings)
        box1.add_widget(button_back)

        self.add_widget(box1)

    def change_to_target(self, *args):
        self.manager.current = 'TargetStart'
        self.manager.transition.direction = 'left'

    def change_to_bars(self, *args):
        self.manager.current = 'BarsStart'
        self.manager.transition.direction = 'left'

    def change_to_ardrone(self, *args):
        self.manager.current = 'DroneMenu'
        self.manager.transition.direction = 'left'

    def change_to_gamesettings(self, *args):
        self.manager.current = 'GameSettings'
        self.manager.transition.direction = 'left'

    def change_to_bci(self, *args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'


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


class BCIMenu(Screen):
    # layout

    def __init__(self, session_header, **kwargs):
        super(BCIMenu, self).__init__(**kwargs)
        self.sh = session_header

    def change_to_calibration(self, *args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'left'

    def change_to_ml(self, *args):
        self.manager.current = 'MlMenu'
        self.manager.transition.direction = 'left'

    def change_to_game(self, *args):
        self.manager.current = 'GameMenu'
        self.manager.transition.direction = 'left'

    def change_to_openbci(self, *args):
        self.manager.current = 'AcquisitionSettings'
        self.manager.transition.direction = 'left'

    def change_to_start(self, *args):
        self.manager.current = 'start'
        self.manager.transition.direction = 'right'
