############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty, \
                            ListProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget

# KV file:
Builder.load_file('screens/game/targetstart.kv')

# Generic:
import math
import random

# Project's:
from SampleManager import *
from standards import *
from approach import Approach
######################################################################

class TargetStart(Screen):

    bar_left_level = NumericProperty(0)
    bar_right_level = NumericProperty(0)

    label_on_toggle_button = StringProperty('Start')

    game = ObjectProperty(None)


    def __init__ (self, session_header,**kwargs):
        super (TargetStart, self).__init__(**kwargs)
        self.sh = session_header

        self.stream_flag = False

    # BUTTON CALLBACKS    
    # ----------------------
    def change_to_game(self,*args):

        self.manager.current = 'GameMenu'
        self.manager.transition.direction = 'right'

    def toogle_stream(self,*args):
        if self.stream_flag:
            self.stream_stop()
        else:
            self.stream_start()

    # ----------------------

    def stream_stop(self):
        # self.sm.stop_flag = True
        self.stream_flag = False
        # self.sm.join()
        self.label_on_toggle_button = 'Start'
        # self.clock_unscheduler()
        # self.set_bar_default()
        self.game.stop()

    def stream_start(self):
        # self.load_approach()
        # self.sm = SampleManager(self.sh.com_port, self.sh.baud_rate, self.sh.channels,
        #     self.sh.buf_len, daisy=self.sh.daisy, mode = self.sh.mode, path = self.sh.path_to_file)
        # self.sm.daemon = True  
        # self.sm.stop_flag = False
        # self.sm.start()
        self.label_on_toggle_button = 'Stop'
        self.stream_flag = True
        # self.clock_scheduler()
        self.game.start(None)


    def clock_scheduler(self):
        Clock.schedule_interval(self.get_probs, 1/2)

    def clock_unscheduler(self):
        Clock.unschedule(self.get_probs)


    def get_probs(self, dt):

        t, buf = self.sm.GetBuffData()

        if buf.shape[0] == self.sh.buf_len:

            p = self.ap.applyModelOnEpoch(buf.T, 'prob')[0]

            self.bar_left_level = int(math.floor(p[0] * 100))
            self.bar_right_level = int(math.floor(p[1] * 100))

    def set_bar_default(self):

        self.bar_left_level = 0
        self.bar_right_level = 0

    def load_approach(self):

        self.ap = Approach()
        self.ap.loadFromPkl(PATH_TO_SESSION + self.sh.name)



from kivy.uix.image import Image
from kivy.core.window import Window


class Game(Widget):

    player = ObjectProperty(None)
    target = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(None, self)
        if not self._keyboard:
            return

        self._keyboard.bind(on_key_down=self.on_keyboard_down)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            if self.player.center_x > 0:
                self.player.pos[0] -= 10
        elif keycode[1] == 'right':
            if self.player.center_x < int(self.parent.width):
                self.player.pos[0] += 10
        elif keycode[1] == 'up':
            if self.player.center_y < int(self.parent.height):
                self.player.pos[1] += 10
        elif keycode[1] == 'down':
            if self.player.center_y > 0:
                self.player.pos[1] -= 10
        else:
            return False

    def set_positions(self):

        max_width = int(self.parent.width)
        max_height = int(self.parent.height)

        self.target.pos = (random.randint(0,max_width), \
                               random.randint(0,max_height))

        self.player.pos = self.center


    def start(self, dt):

        self.target.t_color = [1,1,0,1]

        self.set_positions()

        Clock.schedule_interval(self.check_if_won, 1/2)

    def stop(self):
        Clock.unschedule(self.check_if_won)

    def check_if_won(self, dt):
        if self.player.collide_widget(self.target):
            print 'won'
            self.stop()
            self.target.t_color = [0,1,0,1]
            Clock.schedule_once(self.start, 1)



class GamePlayer(Widget):
    pass


class GameTarget(Widget):

    t_color = ListProperty([1,1,0,1])
        


    


        