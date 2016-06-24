from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from standards import *

class GeneralSettings(Screen):
# layout
    def __init__ (self, session_header, **kwargs):
        super (GeneralSettings, self).__init__(**kwargs)
        self.sh = session_header

        self.bind(on_pre_enter=self.update_screen)

        boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        ## TOP PART

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.7,
            padding=10, spacing=10, orientation='vertical')

        label_cal_path = Label(text = 'Path to Calibration Data: ', font_size=FONT_SIZE)
        self.cal_path = TextInput(font_size= FONT_SIZE,
                        text='', multiline=False)

        label_cal_path_ev = Label(text = 'Path to Calibration Events: ', font_size=FONT_SIZE)
        self.cal_path_ev = TextInput(font_size= FONT_SIZE,
                        text='', multiline=False)

        label_val_path = Label(text = 'Path to Validation Data: ', font_size=FONT_SIZE)
        self.val_path = TextInput(font_size= FONT_SIZE,
                        text='', multiline=False)

        label_val_path_ev = Label(text = 'Path to Validation Events: ', font_size=FONT_SIZE)
        self.val_path_ev = TextInput(font_size= FONT_SIZE,
                        text='', multiline=False)

        box_top.add_widget(label_cal_path)
        box_top.add_widget(self.cal_path)
        box_top.add_widget(label_cal_path_ev)
        box_top.add_widget(self.cal_path_ev)
        box_top.add_widget(label_val_path)
        box_top.add_widget(self.val_path)
        box_top.add_widget(label_val_path_ev)
        box_top.add_widget(self.val_path_ev)

        boxg.add_widget(box_top)

        ## BOTTOM PART
        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3, 
            padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=FONT_SIZE)
        
        button_save = Button(text="Save", size = BUTTON_SIZE)
        button_save.bind(on_press= self.save_config)

        button_back = Button(text="Back", size = BUTTON_SIZE)
        button_back.bind(on_press= self.change_to_start)

        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_save)
        box_bottom.add_widget(button_back)

        boxg.add_widget(box_bottom)


        self.add_widget(boxg)

    def change_to_start(self,*args):
        self.manager.current = 'start'
        self.manager.transition.direction = 'right'

    def save_config(self,*args):

        self.sh.data_cal_path = self.cal_path.text
        self.sh.events_cal_path = self.cal_path_ev.text
        self.sh.data_val_path = self.val_path.text 
        self.sh.events_val_path = self.val_path_ev.text

        self.sh.saveToPkl()
        self.label_msg.text = "Settings Saved!"

    def update_screen(self,*args):
        self.cal_path.text = self.sh.data_cal_path
        self.cal_path_ev.text = self.sh.events_cal_path
        self.val_path.text = self.sh.data_val_path
        self.val_path_ev.text = self.sh.events_val_path

