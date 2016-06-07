from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from standards import *

class BCIMenu(Screen):
# layout
    def __init__ (self,**kwargs):
        super (BCIMenu, self).__init__(**kwargs)

        box1 = BoxLayout(size_hint_x=1, size_hint_y=0.7,padding=10, spacing=10, orientation='vertical')

        self.label_msg = Label(text="BCI Menu", font_size=FONT_SIZE)

        button_openbci = Button(text="Acquisition Settings")
        button_openbci.bind(on_press= self.change_to_openbci)

        button_dp = Button(text="Data Processing Settings")
        button_dp.bind(on_press= self.change_to_dp)

        button_precal = Button(text="Pre Calibration")
        button_precal.bind(on_press= self.change_to_precal)

        button_cal = Button(text="Calibration")
        button_cal.bind(on_press= self.change_to_calibration)

        button_val = Button(text="Validation")
        button_val.bind(on_press= self.change_to_validation)

        button_game = Button(text="Game")
        button_game.bind(on_press= self.change_to_game)

        button_back = Button(text="Back")
        button_back.bind(on_press= self.change_to_start)


        box1.add_widget(self.label_msg)

        box1.add_widget(button_openbci)
        box1.add_widget(button_dp)
        box1.add_widget(button_precal)
        box1.add_widget(button_cal)
        box1.add_widget(button_val)
        box1.add_widget(button_game)
        box1.add_widget(button_back)

        self.add_widget(box1)

    def change_to_precal(self,*args):
        self.manager.current = 'PreCalMenu'
        self.manager.transition.direction = 'left'

    def change_to_calibration(self,*args):
        self.manager.current = 'CalMenu'
        self.manager.transition.direction = 'left'

    def change_to_validation(self,*args):
        self.manager.current = 'ValMenu'
        self.manager.transition.direction = 'left'

    def change_to_game(self,*args):
        self.manager.current = 'GameMenu'
        self.manager.transition.direction = 'left'

    def change_to_openbci(self,*args):
        self.manager.current = 'AcquisitionSettings'
        self.manager.transition.direction = 'left'

    def change_to_dp(self,*args):
        self.manager.current = 'DataProcessingSettings'
        self.manager.transition.direction = 'left'

    def change_to_start(self,*args):
        self.manager.current = 'start'
        self.manager.transition.direction = 'right'