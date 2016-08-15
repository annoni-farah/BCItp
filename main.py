import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

import os, sys, inspect

FOLDERS = ['bci_ml', 'bci_ml/approaches', 'utils', 'screens/settings', 'screens','screens/cal',
 'screens/hardware', 'screens/ml', 'screens/precal',
 'screens/cal', 'screens/val', 'screens/game', 'templates']

for i in range(len(FOLDERS)):
      cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],FOLDERS[i])))
      if cmd_subfolder not in sys.path:
            sys.path.insert(0, cmd_subfolder)

from settings import *

from ScreenStart import *
from GeneralSettings import *
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
from ValStart import *

from MlMenu import *

from GameMenu import *
from GameSettings import *
from BarsStart import *
from TargetStart import *

from kivy.properties import StringProperty

from SessionInfo import SessionHeader

class MyApp(App):

      def build(self):
            sh = SessionHeader()

            sm = ScreenManager()
            start_screen = StartScreen(sh, name='start')
            settings_screen = GeneralSettings(sh, name='GeneralSettings')
            bci_screen = BCIMenu(sh, name='BCIMenu')

            acquisition_settings_screen = AcquisitionSettings(sh, name='AcquisitionSettings')

            data_processing_settings_screen = DataProcessingSettings(sh, name='DataProcessingSettings')

            precal_screen = PreCalMenu(sh, name='PreCalMenu')
            precal_start_screen = PreCalStart(sh, name='PreCalStart')
            precal_settings_screen = PreCalSettings(sh, name='PreCalSettings')

            cal_screen = CalMenu(sh, name='CalMenu')
            cal_settings_screen = CalSettings(sh, name='CalSettings')
            cal_start_screen = CalStart(sh, name='CalStart')

            val_screen = ValMenu(sh, name='ValMenu')
            val_start_screen = ValStart(sh, name='ValStart')

            ml_screen = MlMenu(sh, name='MlMenu')

            game_screen = GameMenu(sh, name='GameMenu')
            game_settings_screen = GameSettings(sh, name='GameSettings')
            bars_start_screen = BarsStart(sh, name='BarsStart')
            target_start_screen = TargetStart(sh, name='TargetStart')

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
            sm.add_widget(val_start_screen)

            sm.add_widget(ml_screen)

            sm.add_widget(game_screen)
            sm.add_widget(game_settings_screen)
            sm.add_widget(bars_start_screen)
            sm.add_widget(target_start_screen)

            sm.current = 'start'

            return sm


# run app
if __name__ == "__main__":
    # stream_thread.start()

    MyApp().run()
 # join all items in a list into 1 big string