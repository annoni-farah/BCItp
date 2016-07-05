from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.image import AsyncImage

from kivy.uix.slider import Slider

from kivy.graphics import Rectangle, Color

from kivy.clock import Clock

# from threading import Thread
from SampleManager import *

from kivy.uix.widget import Widget

import math

from kivy.garden.graph import Graph, MeshLinePlot
Graph._with_stencilbuffer=False # to fix garden.graphs bug when using screens

from kivy.garden.bar import Bar

from standards import *

from approach import Approach

class BarsStart(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (BarsStart, self).__init__(**kwargs)
        self.sh = session_header


    # Top part
        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.7,padding=10, 
            spacing=10, orientation='horizontal')

        box_vleft = BoxLayout(size_hint_x=0.1)
        box_vright = BoxLayout(size_hint_x=0.1)

        self.s_right = Bar(orientation = 'bt', color=[0, 0, 1, 1])
        self.s_left = Bar(orientation = 'bt', color=[1, 0, 0, 1])

        box_vleft.add_widget(self.s_left)
        box_vright.add_widget(self.s_right)

        box_top.add_widget(box_vright, 0)
        box_top.add_widget(box_vleft, 2)
        

    # Bottom part

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, 
            spacing=10, orientation='vertical')

        button_back = Button(text="Back", size = BUTTON_SIZE)
        button_back.bind(on_press= self.change_to_game)

        self.button_stream = Button(text="Start Streaming", size = BUTTON_SIZE)
        self.button_stream.bind(on_press= self.toogle_stream)

        self.label_info = Label(text= 'Msg:')

        box_bottom.add_widget(self.label_info)

        box_bottom.add_widget(self.button_stream)
        box_bottom.add_widget(button_back)

    # Whole part

        boxg = BoxLayout(orientation='vertical', padding=10, 
            spacing=10)

        boxg.add_widget(box_bottom, 0)
        boxg.add_widget(box_top, 1)
        

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
        self.set_bar_default()

    def stream_start(self):
        self.load_approach()
        self.sm = SampleManager(self.sh.com_port, self.sh.baud_rate, self.sh.channels,
            self.sh.buf_len, daisy=self.sh.daisy, mode = self.sh.mode, path = self.sh.path_to_file)
        self.sm.daemon = True  
        self.sm.stop_flag = False
        self.sm.start()
        self.button_stream.text = 'Stop Streaming'
        self.stream_flag = True
        self.clock_scheduler()


    def clock_scheduler(self):
        Clock.schedule_interval(self.get_probs, 1/2)

    def clock_unscheduler(self):
        Clock.unschedule(self.get_probs)


    def get_probs(self, dt):

        t, buf = self.sm.GetBuffData()

        if buf.shape[0] == self.sh.buf_len:

            p = self.ap.applyModelOnEpoch(buf.T, 'prob')[0]

            self.s_left.value = int(math.floor(p[0] * 100))
            self.s_right.value = int(math.floor(p[1] * 100))

    def set_bar_default(self):

        self.s_left.value = 0
        self.s_right.value = 0

    def load_approach(self):

        self.ap = Approach()
        self.ap.loadFromPkl(PATH_TO_SESSION + self.sh.name)






    


        