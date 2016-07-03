from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

from utils import saveObjAsJson

from standards import *

class AcquisitionSettings(Screen):
# layout
    def __init__ (self, session_header,**kwargs):
        super (AcquisitionSettings, self).__init__(**kwargs)
        self.sh = session_header

        self.bind(on_pre_enter=self.update_screen)

        boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        ## BOTTOM PART
        box_bottom = BoxLayout(size_hint = BUTTON_BOX_SIZE, 
            padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="", font_size=FONT_SIZE)
        
        button_save = Button(text="Save", size = BUTTON_SIZE)
        button_save.bind(on_press= self.save_config)

        button_back = Button(text="Back", size = BUTTON_SIZE)
        button_back.bind(on_press= self.change_to_cal)

        box_bottom.add_widget(self.label_msg)
        box_bottom.add_widget(button_save)
        box_bottom.add_widget(button_back)


        ## TOP PART

        box_top = BoxLayout(size_hint_x=1, size_hint_y=0.6,
            padding=10, spacing=10, orientation='vertical')

        self.box_text = BoxLayout(size_hint_x=1, size_hint_y=0.7,
            padding=10, spacing=10, )

        ## OPENBCI CONFIG
        self.box_text_openbci = BoxLayout(orientation='vertical')

        box_com = BoxLayout(orientation = 'horizontal')
        label_com = Label(text = 'COM Port', font_size=FONT_SIZE)
        self.com_port = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='/dev/ttyUSB0', multiline=False)
        box_com.add_widget(label_com)
        box_com.add_widget(self.com_port)

        box_baud = BoxLayout(orientation = 'horizontal')
        label_baud = Label(text = 'BaudRate', font_size=FONT_SIZE)
        self.baud_rate = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                        text='115200', multiline=False)
        box_baud.add_widget(label_baud)
        box_baud.add_widget(self.baud_rate)

        box_ch = BoxLayout(orientation = 'horizontal')
        label_ch = Label(text = 'Channels Labels', font_size=FONT_SIZE)
        self.ch_labels = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
                text='', multiline=False)
        box_ch.add_widget(label_ch)
        box_ch.add_widget(self.ch_labels)

        box_daisy = BoxLayout(orientation = 'horizontal')
        checkbox_daisy = CheckBox()
        checkbox_daisy.bind(active=self.enable_daisy)
        label_daisy = Label(text="Use Daisy:", font_size=FONT_SIZE)
        box_daisy.add_widget(label_daisy)
        box_daisy.add_widget(checkbox_daisy)
        self.box_text_openbci.add_widget(box_daisy)

        self.box_text_openbci.add_widget(box_com)
        self.box_text_openbci.add_widget(box_baud)
        self.box_text_openbci.add_widget(box_ch)

        ## SIMULATOR CONFIG
        self.box_text_simu = BoxLayout(orientation='vertical')

        box_ch2 = BoxLayout(orientation = 'horizontal')
        label_ch2 = Label(text = 'Channels Labels', font_size=FONT_SIZE)
        self.ch_labels2 = TextInput(font_size= FONT_SIZE,
                text='', multiline=True)
        box_ch2.add_widget(label_ch2)
        box_ch2.add_widget(self.ch_labels2)
        self.box_text_simu.add_widget(box_ch2)

        box_daisy = BoxLayout(orientation = 'horizontal')
        checkbox_daisy = CheckBox()
        checkbox_daisy.bind(active=self.enable_daisy)
        label_daisy = Label(text="Use Daisy:", font_size=FONT_SIZE)
        box_daisy.add_widget(label_daisy)
        box_daisy.add_widget(checkbox_daisy)
        self.box_text_simu.add_widget(box_daisy)

        ## PLAYBACK CONFIG
        self.box_text_playback = BoxLayout(orientation='vertical')

        box_path = BoxLayout(orientation = 'horizontal')
        label_path = Label(text = 'Path to EEG file', font_size=FONT_SIZE)
        self.path_to_file = TextInput(font_size= FONT_SIZE,
                text='', multiline=True)
        box_path.add_widget(label_path)
        box_path.add_widget(self.path_to_file)
        self.box_text_playback.add_widget(box_path)


        ## CHECK BOXES
        label_simu = Label(text="Simulator", font_size=FONT_SIZE)
        label_openbci = Label(text="OpenBCI", font_size=FONT_SIZE)
        label_playback = Label(text="Playback", font_size=FONT_SIZE)

        box_checkbox = BoxLayout(size_hint_x=1, size_hint_y=0.3,
                        padding=5, spacing=5, orientation='vertical')

        box_checkbox_top = BoxLayout(size_hint_x=1, size_hint_y=0.5,
                        padding=5, spacing=5, orientation='horizontal')

        box_checkbox_bottom = BoxLayout(size_hint_x=1, size_hint_y=0.5,
                        padding=5, spacing=5, orientation='horizontal')


        checkbox_simu = CheckBox()
        checkbox_simu.bind(active=self.enable_simu_config)

        checkbox_openbci = CheckBox()
        checkbox_openbci.bind(active=self.enable_openbci_config)

        checkbox_playback = CheckBox()
        checkbox_playback.bind(active=self.enable_playback_config)

        box_checkbox_bottom.add_widget(checkbox_simu)
        box_checkbox_bottom.add_widget(checkbox_openbci)
        box_checkbox_bottom.add_widget(checkbox_playback)

        box_checkbox_top.add_widget(label_simu)
        box_checkbox_top.add_widget(label_openbci)
        box_checkbox_top.add_widget(label_playback)

        box_checkbox.add_widget(box_checkbox_top)
        box_checkbox.add_widget(box_checkbox_bottom)

        box_top.add_widget(box_checkbox)
        box_top.add_widget(self.box_text)

        boxg.add_widget(box_top)
        boxg.add_widget(box_bottom)

        self.add_widget(boxg)

        self.daisy = False

    def change_to_cal(self,*args):
        self.manager.current = 'BCIMenu'
        self.manager.transition.direction = 'right'

    def enable_openbci_config(self, checkbox, value):
        if value:
            self.box_text.add_widget(self.box_text_openbci)
            self.mode = 'openbci'
        else:
            self.box_text.remove_widget(self.box_text_openbci)

    def enable_simu_config(self, checkbox, value):
        if value:
            self.box_text.add_widget(self.box_text_simu)
            self.mode = 'simu'
        else:
            self.box_text.remove_widget(self.box_text_simu)

    def enable_playback_config(self, checkbox, value):
        if value:
            self.box_text.add_widget(self.box_text_playback)
            self.mode = 'playback'
        else:
            self.box_text.remove_widget(self.box_text_playback)

    def enable_daisy(self, checkbox, value):
        if value:
            self.daisy = True
        else:
            self.daisy = False

    def save_config(self,*args):
        if self.daisy:
            self.sample_rate = 125.0
        else:
            self.sample_rate = 250.0

        self.sh.mode = self.mode
        self.sh.com_port = self.com_port.text
        self.sh.ch_labels = self.ch_labels.text
        self.sh.baud_rate = self.baud_rate.text
        self.sh.path_to_file = self.path_to_file.text
        self.sh.sample_rate = self.sample_rate
        self.sh.daisy = self.daisy

        self.sh.saveToPkl()
        self.label_msg.text = "Settings Saved!"

    def update_screen(self,*args):
        if self.sh.mode is not None:
            self.com_port.text = self.sh.com_port
            self.ch_labels.text = self.sh.ch_labels
            self.baud_rate.text = self.sh.baud_rate
            self.path_to_file.text = self.sh.path_to_file            

            if self.sh.daisy:
                self.enable_daisy



