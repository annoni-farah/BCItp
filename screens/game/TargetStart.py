from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.image import AsyncImage

from kivy.uix.slider import Slider

from kivy.graphics import Rectangle, Color

from kivy.clock import Clock

from kivy.properties import NumericProperty

# from threading import Thread
from SampleManager import *

from kivy.uix.widget import Widget

import math

from kivy.garden.graph import Graph, MeshLinePlot
Graph._with_stencilbuffer=False # to fix garden.graphs bug when using screens

from kivy.garden.bar import Bar

from standards import *

from approach import Approach

import random

class TargetStart(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (TargetStart, self).__init__(**kwargs)
        self.sh = session_header
    

    # Top part
        box_top = RelativeLayout(size_hint = (1, 0.7))

        self.goal = Goal(size_hint=(None, None), size=(50,50), pos = (100,100))
        box_top.add_widget(self.goal)

        self.ball = Ball(size_hint=(None, None), size=(20,20), pos = (300,300))
        box_top.add_widget(self.ball)

        
    # Bottom part

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, 
            spacing=10, orientation='vertical')

        button_back = Button(text="Back", size = BUTTON_SIZE)
        button_back.bind(on_press= self.change_to_game)

        self.button_stream = Button(text="Start Streaming", size = BUTTON_SIZE)
        self.button_stream.bind(on_press= self.toogle_stream)

        box_bottom.add_widget(self.button_stream)
        box_bottom.add_widget(button_back)

        Clock.schedule_interval(self.check_if_won, 1/2)

    # Whole part
        boxg = BoxLayout(orientation='vertical', padding=10, 
            spacing=10)

        boxg.add_widget(box_top)

        boxg.add_widget(box_bottom)

        self.add_widget(boxg) 

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
        self.sm.stop_flag = True
        self.stream_flag = False
        self.sm.join()
        self.button_stream.text = 'Start Streaming'
        self.clock_unscheduler()

    def stream_start(self):
        self.load_approach()
        self.sm = SampleManager(self.sh.com_port, self.sh.baud_rate, self.sh.channels,
            self.sh.buf_len, daisy=self.sh.daisy, mode = self.sh.mode, path = self.sh.path_to_file)
        self.sm.daemon = True  
        self.sm.stop_flag = False
        self.sm.start()
        self.button_stream.text = 'Stop Streaming'
        self.stream_flag = True
        Clock.schedule_once(self.clock_scheduler, 0)


    def clock_scheduler(self,dt):
        Clock.schedule_interval(self.check_if_won, 1/2)
        Clock.schedule_interval(self.get_probs, 1/2)
        Clock.schedule_interval(self.check_if_streaming, 2)


    def clock_unscheduler(self):
        Clock.unschedule(self.get_probs)
        Clock.unschedule(self.check_if_streaming)

    def check_if_streaming(self, dt):
        print 'stopped', self.sm.Stopped()
        print 'flag', self.stream_flag
        if self.sm.Stopped() and self.stream_flag:
            self.toogle_stream()

    def get_probs(self, dt):

        t, buf = self.sm.GetBuffData()

        if buf.shape[0] == self.sh.buf_len:

            p = self.ap.applyModelOnEpoch(buf.T, 'prob')[0]

            self.map_prob(p)

    def map_prob(self, prob):

        if prob[1] > prob[0]:
            self.ball.move('left')
        else:
            self.ball.move('right')

    def load_approach(self):

        self.ap = Approach()
        self.ap.loadFromPkl(PATH_TO_SESSION + self.sh.name)

    def check_if_won(self, dt):
        if self.ball.collide_widget(self.goal):
            Clock.unschedule(self.check_if_won)
            self.goal.r, self.goal.g = 0,1
            Clock.schedule_once(self.ball.reset, 2)
            Clock.schedule_once(self.goal.reset, 2)
            Clock.schedule_once(self.clock_scheduler, 2)


from kivy.uix.image import Image
from kivy.core.window import Window

class Ball(Widget):
    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(None, self)
        if not self._keyboard:
            return

        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self.bind(pos=self.update_rect)

        with self.canvas:
            Color(0, 0, 1.)
            # Add a rectangle
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.velocity = [0.5, 0.5]

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.x -= 10
        elif keycode[1] == 'right':
            self.x += 10
        elif keycode[1] == 'up':
            self.y += 10
        elif keycode[1] == 'down':
            self.y -= 10
        else:
            return False

        return True

    def move(self, direction):

        if direction == 'left':
            self.x -= self.velocity[0]
        if direction == 'right':
            self.x += self.velocity[0]
        if direction == 'down':
            self.y -= self.velocity[1]
        if direction == 'up':
            self.y += self.velocity[1]

    def reset(self, dt):
        pos_x=random.randint(0,self.parent.width)
        pos_y=random.randint(0,self.parent.height)
        self.pos = (pos_x,pos_y)

    def update_rect(self, *args):
        if self.pos[0] < 0:
            self.pos[0] = 0

        if self.pos[0] > self.parent.width:
           self.pos[0] = self.parent.width

        if self.pos[1] < 0:
            self.pos[1] = 0

        if self.pos[1] > self.parent.height:
           self.pos[1] = self.parent.height

        self.rect.pos = self.pos


class Goal(Widget):

    r = NumericProperty(1)
    g = NumericProperty(0)
    b = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Goal, self).__init__(**kwargs)   

        self.bind(r = self.update_rect)
        self.bind(g = self.update_rect)
        self.bind(b = self.update_rect)
        self.bind(pos=self.update_rect)
        
        self.update_rect()

    def update_rect(self, *args):

        with self.canvas:
            self.canvas.clear()
            # Add a red color
            Color(self.r, self.g, self.b)
            # Add a rectangle
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def reset(self, dt):
        self.r, self.g, self.b = 1,0,0
        pos_x=random.randint(0,self.parent.width)
        pos_y=random.randint(0,self.parent.height)
        self.pos = (pos_x,pos_y)
        


    


        