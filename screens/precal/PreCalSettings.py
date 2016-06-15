from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

from utils import saveObjAsJson

from standards import *

class PreCalSettings(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (PreCalSettings, self).__init__(**kwargs)
        self.sh = session_header

        boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.5,
            padding=10, spacing=10, orientation='vertical')

        box_tt = BoxLayout(orientation = 'horizontal')
        label_tt = Label(text = 'Total Time (s)', font_size=FONT_SIZE)
        self.total_time = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='100', multiline=False)
        box_tt.add_widget(label_tt)
        box_tt.add_widget(self.total_time)
        box_top.add_widget(box_tt)

        box_rt = BoxLayout(orientation = 'horizontal')
        label_rt = Label(text = 'Time to set Max (s)', font_size=FONT_SIZE)
        self.relax_time = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='10', multiline=False)
        box_rt.add_widget(label_rt)
        box_rt.add_widget(self.relax_time)
        box_top.add_widget(box_rt)

        box_ch = BoxLayout(orientation = 'horizontal')
        label_ch = Label(text = 'Right - Channels used in Energy Calc:', font_size=FONT_SIZE)
        self.ch_energy_right = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                text= '0', multiline=False)
        box_ch.add_widget(label_ch)
        box_ch.add_widget(self.ch_energy_right)
        box_top.add_widget(box_ch)

        box_chl = BoxLayout(orientation = 'horizontal')
        label_chl = Label(text = 'Left - Channels used in Energy Calc:', font_size=FONT_SIZE)
        self.ch_energy_left = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
            text='1', multiline=False)
        box_chl.add_widget(label_chl)
        box_chl.add_widget(self.ch_energy_left)
        box_top.add_widget(box_chl)

        box_sd = BoxLayout(orientation = 'horizontal')
        label_sd = Label(text = 'Sign - left or right', font_size=FONT_SIZE)
        self.sign_direction = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
            text='left', multiline=False)
        box_sd.add_widget(label_sd)
        box_sd.add_widget(self.sign_direction)
        box_top.add_widget(box_sd)

        checkbox_plot = CheckBox()
        checkbox_plot.bind(active=self.enable_plot)

        label_plot = Label(text="Plot Data:", font_size=FONT_SIZE)
        box_checkbox = BoxLayout(orientation='horizontal')

        box_checkbox.add_widget(label_plot)
        box_checkbox.add_widget(checkbox_plot)

        box_top.add_widget(box_checkbox)

        boxg.add_widget(box_top)

        ## BOTTOM PART
        box_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.3, 
            padding=10, spacing=10, orientation='vertical')

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

        # Default Values:
        self.plot_flag = False

    def change_to_cal(self,*args):
        self.manager.current = 'PreCalMenu'
        self.manager.transition.direction = 'right'

    def enable_plot(self, checkbox, value):
        if value:
            self.plot_flag = True
        else:
            self.plot_flag = False

    def save_config(self,*args):

        self.sh.pc_ch_energy_left =  self.ch_energy_left.text
        self.sh.pc_ch_energy_right = self.ch_energy_right.text
        self.sh.pc_total_time =  self.total_time.text
        self.sh.pc_relax_time =  self.relax_time.text
        self.sh.pc_plot_flag =  self.plot_flag

        saveObjAsJson(self.sh, PATH_TO_SESSION + self.sh.name + '/' + 'session_info.txt')
        self.label_msg.text = "Settings Saved!"
