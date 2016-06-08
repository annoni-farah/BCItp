import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

import os, sys, inspect

FOLDERS = ['bci_ml', 'utils', 'settings', 'screens','screens/cal',
 'screens/hardware', 'screens/ml', 'screens/precal',
 'screens/cal', 'screens/val', 'screens/game', ]

for i in range(len(FOLDERS)):
      cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],FOLDERS[i])))
      if cmd_subfolder not in sys.path:
            sys.path.insert(0, cmd_subfolder)

from ScreenStart import *
from UISettingsScreen import *
from BCIMenu import *

from AcquisitionSettings import *

from DataProcessingSettings import *

from PreCalMenu import *
from PreCalSettings import *
from PreCalStart import *

from CalMenu import *
from CalSettings import *
from CalStart import *

from ValMenu import *
from ValSettings import *
from ValStart import *

from MlMenu import *

from GameMenu import *

class MyApp(App):

    def build(self):
            sm = ScreenManager()
            start_screen = StartScreen(name='start')
            settings_screen = UISettingsScreen(name='UISettings')
            bci_screen = BCIMenu(name='BCIMenu')

            acquisition_settings_screen = AcquisitionSettings(name='AcquisitionSettings')

            data_processing_settings_screen = DataProcessingSettings(name='DataProcessingSettings')

            precal_screen = PreCalMenu(name='PreCalMenu')
            precal_start_screen = PreCalStart(name='PreCalStart')
            precal_settings_screen = PreCalSettings(name='PreCalSettings')

            cal_screen = CalMenu(name='CalMenu')
            cal_settings_screen = CalSettings(name='CalSettings')
            cal_start_screen = CalStart(name='CalStart')

            val_screen = ValMenu(name='ValMenu')
            val_settings_screen = ValSettings(name='ValSettings')
            val_start_screen = ValStart(name='ValStart')

            ml_screen = MlMenu(name='MlMenu')

            game_screen = GameMenu(name='GameMenu')

            sm.add_widget(start_screen)
            sm.add_widget(settings_screen)
            sm.add_widget(bci_screen)

            sm.add_widget(acquisition_settings_screen)

            sm.add_widget(data_processing_settings_screen)

            sm.add_widget(precal_screen)
            sm.add_widget(precal_settings_screen)
            sm.add_widget(precal_start_screen)

            sm.add_widget(cal_screen)
            sm.add_widget(cal_settings_screen)
            sm.add_widget(cal_start_screen)

            sm.add_widget(val_screen)
            sm.add_widget(val_settings_screen)
            sm.add_widget(val_start_screen)

            sm.add_widget(ml_screen)

            sm.add_widget(game_screen)

            sm.current = 'start'
            return sm


# run app
if __name__ == "__main__":
    # stream_thread.start()

    MyApp().run()
 # join all items in a list into 1 big string