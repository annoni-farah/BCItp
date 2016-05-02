import random

import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

from ScreenStart import *
from UISettingsScreen import *
from BCIMenu import *

from PreCalMenu import *
from PreCalStart import *
from CalStart import *

from CalMenu import *
from CalSettings import *

from ValMenu import *
from ValSettings import *

from GameMenu import *

class MyApp(App):

    def build(self):
            sm = ScreenManager()
            start_screen = StartScreen(name='start')
            settings_screen = UISettingsScreen(name='UISettings')
            bci_screen = BCIMenu(name='BCIMenu')

            precal_screen = PreCalMenu(name='PreCalMenu')
            precal_start_screen = PreCalStart(name='PreCalStart')

            cal_screen = CalMenu(name='CalMenu')
            cal_settings_screen = CalSettings(name='CalSettings')
            cal_start_screen = CalStart(name='CalStart')

            val_screen = ValMenu(name='ValMenu')
            val_settings_screen = ValSettings(name='ValSettings')

            game_screen = GameMenu(name='GameMenu')

            sm.add_widget(start_screen)
            sm.add_widget(settings_screen)
            sm.add_widget(bci_screen)

            sm.add_widget(precal_screen)
            sm.add_widget(precal_start_screen)

            sm.add_widget(cal_screen)
            sm.add_widget(cal_settings_screen)
            sm.add_widget(cal_start_screen)

            sm.add_widget(val_screen)
            sm.add_widget(val_settings_screen)

            sm.add_widget(game_screen)

            sm.current = 'start'
            return sm


# run app
if __name__ == "__main__":
    # stream_thread.start()

    MyApp().run()
 # join all items in a list into 1 big string