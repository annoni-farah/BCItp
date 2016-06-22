from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from utils import saveObjAsJson

from standards import *

class CalSettings(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (CalSettings, self).__init__(**kwargs)
        
        self.sh = session_header

        boxg = BoxLayout(padding=10, spacing=10, orientation='vertical')

        ## TOP PART

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, spacing=10, orientation='vertical')

        box_nt = BoxLayout(orientation = 'horizontal')
        label_nt = Label(text = 'Number of Trials', font_size=FONT_SIZE)
        self.n_trials = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='50', multiline=False)
        box_nt.add_widget(label_nt)
        box_nt.add_widget(self.n_trials)
        box_top.add_widget(box_nt)

        box_po = BoxLayout(orientation = 'horizontal')
        label_po = Label(text = 'Pause Offset (s)', font_size=FONT_SIZE)
        self.pause_offset = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='1', multiline=False)
        box_po.add_widget(label_po)
        box_po.add_widget(self.pause_offset)
        box_top.add_widget(box_po)

        box_co = BoxLayout(orientation = 'horizontal')
        label_co = Label(text = 'Cue Offset (s)', font_size=FONT_SIZE)
        self.cue_offset = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='3', multiline=False)
        box_co.add_widget(label_co)
        box_co.add_widget(self.cue_offset)
        box_top.add_widget(box_co)

        box_eto = BoxLayout(orientation = 'horizontal')
        label_eto = Label(text = 'End Of Trial Offset (s)', font_size=FONT_SIZE)
        self.end_trial_offset = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='8', multiline=False)
        box_eto.add_widget(label_eto)
        box_eto.add_widget(self.end_trial_offset)
        box_top.add_widget(box_eto)

        boxg.add_widget(box_top)

        ## BOTTOM PART

        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3,padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=FONT_SIZE)
        
        button_save = Button(text="Save", size = BUTTON_SIZE)
        button_save.bind(on_press= self.save_config)

        button_back = Button(text="Back", size = BUTTON_SIZE)
        button_back.bind(on_press= self.change_to_cal)

        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_save)
        box_bottom.add_widget(button_back)

        boxg.add_widget(box_bottom)

        self.add_widget(boxg)


    def change_to_cal(self,*args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'right'

    def save_config(self,*args):

        data_cal_path = PATH_TO_SESSION + self.sh.name + '/' + 'data_cal.txt'
        events_cal_path = PATH_TO_SESSION + self.sh.name + '/' + 'events_cal.txt'

        self.sh.n_trials = int(self.n_trials.text)
        self.sh.cue_offset = int(self.cue_offset.text)
        self.sh.pause_offset = int(self.pause_offset.text)
        self.sh.end_trial_offset = int(self.end_trial_offset.text)
        self.data_cal_path = data_cal_path
        self.events_cal_path = events_cal_path

        self.sh.saveToPkl()
        self.label_msg.text = "Settings Saved!"