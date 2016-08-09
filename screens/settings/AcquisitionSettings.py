############################## DEPENDENCIES ##########################
# KIVY modules:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty, \
                            ListProperty, BooleanProperty
from kivy.lang import Builder

# KV file:
Builder.load_file('screens/settings/acquisitionsettings.kv')

# Generic:

# Project's:
from SampleManager import *
from standards import *
from approach import Approach
######################################################################


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


        self.m = ScreenManager()

        simu_screen = Simulator(name='simu')
        self.m.add_widget(simu_screen)
        self.m.current = 'simu'

        openbci_screen = OpenBCI(name='openbci')
        self.m.add_widget(openbci_screen)


        self.add_widget(self.m)

        # boxg = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # ## BOTTOM PART
        # box_bottom = BoxLayout(size_hint = BUTTON_BOX_SIZE, 
        #     padding=10, spacing=10, orientation='vertical')

        # self.label_msg = Label(text="", font_size=FONT_SIZE)
        
        # button_save = Button(text="Save", size = BUTTON_SIZE)
        # button_save.bind(on_press= self.save_config)

        # button_back = Button(text="Back", size = BUTTON_SIZE)
        # button_back.bind(on_press= self.change_to_cal)

        # box_bottom.add_widget(self.label_msg)
        # box_bottom.add_widget(button_save)
        # box_bottom.add_widget(button_back)


        # ## TOP PART

        # box_top = BoxLayout(size_hint_x=1, size_hint_y=0.6,
        #     padding=10, spacing=10, orientation='vertical')

        # self.box_text = BoxLayout(size_hint_x=1, size_hint_y=0.7,
        #     padding=10, spacing=10, )



        # ## PLAYBACK CONFIG
        # self.box_text_playback = BoxLayout(orientation='vertical')

        # box_path = BoxLayout(orientation = 'horizontal')
        # label_path = Label(text = 'Path to EEG file', font_size=FONT_SIZE)
        # self.path_to_file = TextInput(font_size= FONT_SIZE,
        #         text='', multiline=True)
        # box_path.add_widget(label_path)
        # box_path.add_widget(self.path_to_file)

        # box_labels = BoxLayout(orientation = 'horizontal')
        # label_labels = Label(text = 'Path to labels of playback file', font_size=FONT_SIZE)
        # self.path_to_labels_file = TextInput(font_size= FONT_SIZE,
        #         text='', multiline=True)
        # box_labels.add_widget(label_labels)
        # box_labels.add_widget(self.path_to_labels_file)

        # box_srate = BoxLayout(orientation = 'horizontal')
        # label_srate = Label(text = 'Sample Rate', font_size=FONT_SIZE)
        # self.srate = TextInput(font_size= FONT_SIZE,
        #         text='')
        # box_srate.add_widget(label_srate)
        # box_srate.add_widget(self.srate)

        # self.box_text_playback.add_widget(box_path)
        # self.box_text_playback.add_widget(box_labels)
        # self.box_text_playback.add_widget(box_srate)



        # self.daisy = False

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
        elif self.srate != '':
            self.sample_rate = float(self.srate.text)
        else:
            self.sample_rate = 250.0

        self.sh.mode = self.mode
        self.sh.com_port = self.com_port.text
        self.sh.ch_labels = self.ch_labels.text
        self.sh.baud_rate = self.baud_rate.text
        self.sh.path_to_file = self.path_to_file.text
        self.sh.path_to_labels_file = self.path_to_labels_file.text
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



class Simulator(Screen):
    pass
    # def __init__ (self, **kwargs):

    #     super (Simulator, self).__init__(**kwargs)

    # def build(self):
        
        # ## SIMULATOR CONFIG
        # box_ch2 = BoxLayout(orientation = 'horizontal')
        # label_ch2 = Label(text = 'Channels Labels', font_size=FONT_SIZE)
        # self.ch_labels2 = TextInput(font_size= FONT_SIZE,
        #         text='', multiline=True)
        # box_ch2.add_widget(label_ch2)
        # box_ch2.add_widget(self.ch_labels2)
        # self.add_widget(box_ch2)

        # box_daisy = BoxLayout(orientation = 'horizontal')
        # checkbox_daisy = CheckBox()
        # # checkbox_daisy.bind(active=self.enable_daisy)
        # label_daisy = Label(text="Use Daisy:", font_size=FONT_SIZE)
        # box_daisy.add_widget(label_daisy)
        # box_daisy.add_widget(checkbox_daisy)
        # self.add_widget(box_daisy)


class OpenBCI(Screen):
    pass
    # def __init__ (self, **kwargs):

    #     super (OpenBCI, self).__init__(**kwargs)

        # ## OPENBCI CONFIG
        # self.box_text_openbci = BoxLayout(orientation='vertical')

        # box_com = BoxLayout(orientation = 'horizontal')
        # label_com = Label(text = 'COM Port', font_size=FONT_SIZE)
        # self.com_port = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
        #                 text='/dev/ttyUSB0', multiline=False)
        # box_com.add_widget(label_com)
        # box_com.add_widget(self.com_port)

        # box_baud = BoxLayout(orientation = 'horizontal')
        # label_baud = Label(text = 'BaudRate', font_size=FONT_SIZE)
        # self.baud_rate = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
        #                 text='115200', multiline=False)
        # box_baud.add_widget(label_baud)
        # box_baud.add_widget(self.baud_rate)

        # box_ch = BoxLayout(orientation = 'horizontal')
        # label_ch = Label(text = 'Channels Labels', font_size=FONT_SIZE)
        # self.ch_labels = TextInput(size_hint=(1, 0.8), font_size= FONT_SIZE,
        #         text='', multiline=False)
        # box_ch.add_widget(label_ch)
        # box_ch.add_widget(self.ch_labels)

        # box_daisy = BoxLayout(orientation = 'horizontal')
        # checkbox_daisy = CheckBox()
        # checkbox_daisy.bind(active=self.enable_daisy)
        # label_daisy = Label(text="Use Daisy:", font_size=FONT_SIZE)
        # box_daisy.add_widget(label_daisy)
        # box_daisy.add_widget(checkbox_daisy)
        # self.box_text_openbci.add_widget(box_daisy)

        # self.box_text_openbci.add_widget(box_com)
        # self.box_text_openbci.add_widget(box_baud)
        # self.box_text_openbci.add_widget(box_ch)

        # self.add_widget(box_text_openbci)