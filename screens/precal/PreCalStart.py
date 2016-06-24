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

from math import ceil, sin, isnan

from kivy.garden.graph import Graph, MeshLinePlot
Graph._with_stencilbuffer=False # to fix garden.graphs bug when using screens

from kivy.garden.bar import Bar

from standards import *

class PreCalStart(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (PreCalStart, self).__init__(**kwargs)
        self.sh = session_header


    # Top part
        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.7,padding=10, 
            spacing=10, orientation='horizontal')

        box_vleft = BoxLayout(size_hint_x=0.1)
        self.box_vmiddle = BoxLayout(size_hint_x=0.8, orientation='vertical')
        box_vright = BoxLayout(size_hint_x=0.1)

        self.s_right = Bar(orientation = 'bt', color=[0, 0, 1, 1])
        self.s_left = Bar(orientation = 'bt', color=[1, 0, 0, 1])

        box_vleft.add_widget(self.s_left)
        box_vright.add_widget(self.s_right)

        box_top.add_widget(box_vright, 0)
        box_top.add_widget(self.box_vmiddle, 1)
        box_top.add_widget(box_vleft, 2)
        

    # Bottom part

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, 
            spacing=10, orientation='vertical')

        button_back = Button(text="Back", size = BUTTON_SIZE)
        button_back.bind(on_press= self.change_to_precal)

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
    def change_to_precal(self,*args):

        self.manager.current = 'PreCalMenu'
        self.manager.transition.direction = 'right'

    def toogle_stream(self,*args):
        if self.stream_flag:
            self.stream_stop()
        else:
            self.stream_start()

    # ----------------------

    def stream_start(self):
        self.add_to_middle()
        self.label_info.text = "Managing Samples..."

        self.sm = SampleManager(self.sh.com_port, self.sh.baud_rate, self.sh.channels,
            daisy=self.sh.daisy, mode = self.sh.mode, path = self.sh.path_to_file)

        self.sm.CreateDataProcessing(self.sh.buf_len, self.sh.f_low, self.sh.f_high, self.sh.f_order)

        self.label_info.text = "Computing filters and creating buffers..."

        self.sm.daemon = True  
        self.sm.stop_flag = False
        self.label_info.text = "Now Streaming..."
        self.sm.start()
        self.stream_flag = True
        self.button_stream.text = 'Stop Streaming'
        self.clock_scheduler()


    def stream_stop(self):
        self.button_stream.text = 'Start Streaming'
        self.sm.stop_flag = True
        self.stream_flag = False
        self.label_info.text = ""
        self.sm.join()
        self.clock_unscheduler()
        self.remove_from_middle()
        self.sef_bar_default()


    def clock_scheduler(self):
        Clock.schedule_interval(self.get_energy_left, 1/8)
        Clock.schedule_interval(self.get_energy_right, 1/8)

        Clock.schedule_once(self.toogle_stream, self.sh.total_time)
        Clock.schedule_once(self.calc_bar_max, self.sh.relax_time)

        if self.sh.plot_flag:
            Clock.schedule_interval(self.update_graph, 1/4)


    def clock_unscheduler(self):
        Clock.unschedule(self.get_energy_left)
        Clock.unschedule(self.get_energy_right)
        Clock.unschedule(self.toogle_stream)
        Clock.unschedule(self.calc_bar_max)
        Clock.unschedule(self.update_graph)

    def get_energy_right(self, dt):

        energy = self.sm.ComputeEnergy(self.sh.ch_energy_right)
        if hasattr(self, 'bar_max_right'):

            # norm_energy = ceil(self.sm.CalcEnergyAverage(self.ch_energy_right))
            norm_energy = ceil(100 * energy / self.bar_max_right)            
            if norm_energy > 100:
                norm_energy = 100
            self.s_right.value = norm_energy

    def get_energy_left(self, dt):

        energy = self.sm.ComputeEnergy(self.sh.ch_energy_left)
        if hasattr(self, 'bar_max_left'):
            
            # norm_energy = ceil(self.sm.CalcEnergyAverage(self.ch_energy_left))
            norm_energy = ceil(100 * energy / self.bar_max_left)                       
            if norm_energy > 100:
                norm_energy = 100
            self.s_left.value = norm_energy

    def load_settings(self):
        self.load_session_config()
        self.load_dp_settings()
        self.load_acquisition_settings()
        self.load_precal_settings()

    def calc_bar_max(self, dt):
        max_right = self.sm.CalcEnergyAverage(self.sh.ch_energy_right)
        max_left = self.sm.CalcEnergyAverage(self.sh.ch_energy_left)

        print 'max right ', max_right 
        print 'max left ', max_left 

        self.bar_max_right = 2 * max_right
        self.bar_max_left = 2 * max_left

        # print 'max bar ', self.bar_max 

    def sef_bar_default(self):
        self.bar_max_left = 0.0
        self.bar_max_right = 0.0 
        self.s_left.value = 0
        self.s_right.value = 0

        del self.bar_max_left
        del self.bar_max_right

    def add_arrow(self):

        if self.sh.sign_direction == 'left':
            src = "data/resources/left.png"
        elif self.sh.sign_direction == 'right':
            src = "data/resources/right.png"

        self.image = AsyncImage(source=src, allow_stretch=False)

        self.box_vmiddle.add_widget(self.image)

    def add_graph(self):
        self.graph = Graph(xlabel='Samples', ylabel='Amplitude', x_ticks_minor=100,
            x_ticks_major=50, y_ticks_major=50,
            y_grid_label=True, x_grid_label=True, padding=5,
            x_grid=True, y_grid=True, ymin=-100, ymax=100)

        # self.graph = Graph(xlabel='X', ylabel='Y')
        self.plot_left = MeshLinePlot(color = [1,0,0,1])
        self.plot_right = MeshLinePlot(color = [0,0,1,1])
        # print plot.points
        # plot.points = (range(10),range(10))
        self.graph.add_plot(self.plot_left)
        self.graph.add_plot(self.plot_right)

        self.box_vmiddle.add_widget(self.graph)

    def add_to_middle(self):

        if self.sh.plot_flag:
            self.add_graph()

        # if self.mode != 'playback':
        #     self.add_arrow()

    def remove_from_middle(self):

        self.box_vmiddle.clear_widgets()

    def update_graph(self, dt):

        time, data = self.sm.GetBuffData(filt = True)

        # check if data is an array and therefore not a nan value
        if isinstance(data,np.ndarray):


            data_left = data[:,self.sh.ch_energy_left[0]]
            data_right = data[:,self.sh.ch_energy_right[0]]

            time_data_left = np.vstack((time, data_left)).T
            time_data_right = np.vstack((time, data_right)).T

            # print time[-1]

            self.graph.xmin = int(time[0])
            self.graph.xmax = int(time[-1])

            data_to_plot_left = tuple(map(tuple,time_data_left))
            data_to_plot_right = tuple(map(tuple,time_data_right))

            self.plot_left.points = data_to_plot_left
            self.plot_right.points = data_to_plot_right







    


        