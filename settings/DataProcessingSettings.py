from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from utils import saveObjAsJson

from standards import *

class DataProcessingSettings(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (DataProcessingSettings, self).__init__(**kwargs)
        self.sh = session_header

        boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label_msg = Label(text="", font_size=FONT_SIZE)
        ## BOTTOM PART (BUTTONS)

        box_bottom = BoxLayout(size_hint= BUTTON_BOX_SIZE,padding=10, spacing=10, orientation='vertical')

        button_save = Button(text="Save", size = BUTTON_SIZE)
        button_save.bind(on_press= self.save_config)

        button_back = Button(text="Back", size = BUTTON_SIZE)
        button_back.bind(on_press= self.change_to_cal)

        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_save)
        box_bottom.add_widget(button_back)

        boxg.add_widget(box_bottom)

        ## TOP PART

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.7,padding=10, spacing=10, orientation='vertical')

        # DATA CONFIG
        box_data = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, spacing=10, orientation='vertical')

        box_buf = BoxLayout(orientation = 'horizontal')
        label_buf = Label(text ='Circular Buffer Length', font_size=FONT_SIZE)
        self.buf_len = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE, text='500', multiline=False)
        box_buf.add_widget(label_buf)
        box_buf.add_widget(self.buf_len)

        box_ch = BoxLayout(orientation = 'horizontal')
        label_ch = Label(text = 'Channels idx used', font_size=FONT_SIZE)
        self.channels = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                text='0 1 2 3 4 5 6 7', multiline=False)
        box_ch.add_widget(label_ch)
        box_ch.add_widget(self.channels)

        box_data.add_widget(box_buf)
        box_data.add_widget(box_ch)

        box_top.add_widget(box_data)


        # FILTER CONFIG
        box_filter = BoxLayout(size_hint_x=1, size_hint_y=0.4,padding=10, spacing=10, orientation='vertical')

        # box_f_band = BoxLayout(size_hint_x=1,padding=10, spacing=10, orientation='vertical')

        box_high = BoxLayout(orientation = 'horizontal')
        label_high = Label(text = 'Upper cutoff freq (Hz)', font_size=FONT_SIZE)
        self.f_high = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE, text='30', multiline=False)
        box_high.add_widget(label_high)
        box_high.add_widget(self.f_high)

        box_low = BoxLayout(orientation = 'horizontal')
        label_low = Label(text = 'Lower cutoff freq (Hz)', font_size=FONT_SIZE)
        self.f_low = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE, text='8', multiline=False)
        box_low.add_widget(label_low)
        box_low.add_widget(self.f_low)

        box_filter.add_widget(box_low)
        box_filter.add_widget(box_high)
        # box_filter.add_widget(box_f_band)


        box_order = BoxLayout(orientation = 'horizontal')
        label_order = Label(text = 'Filter Order', font_size=FONT_SIZE)
        self.f_order = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE, text='7', multiline=False)
        box_order.add_widget(label_order)
        box_order.add_widget(self.f_order)

        box_filter.add_widget(box_order)

        box_top.add_widget(box_filter)

        boxg.add_widget(box_top, 2)

        self.add_widget(boxg)

    def change_to_cal(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def save_config(self,*args):

        self.sh.buf_len = self.buf_len.text
        self.sh.channels =  self.channels.text
        self.sh.f_low =  self.f_low.text
        self.sh.f_high =  self.f_high.text
        self.sh.f_order =  self.f_order.text
    
        saveObjAsJson(self.sh, PATH_TO_SESSION + self.sh.name + '/' + 'session_info.txt')
        self.label_msg.text = "Settings Saved!"
