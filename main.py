from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

import os
import sys
import inspect

FOLDERS = ['signal_processing', 'signal_processing/approaches', 'utils',
           'screens/settings', 'screens', 'screens/cal',
           'hardware', 'screens/ml', 'screens/precal',
           'screens/cal', 'screens/val', 'screens/game',
           'screens/game/ardrone', 'templates']

for i in range(len(FOLDERS)):
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(
        os.path.split(inspect.getfile(inspect.currentframe()))[0], FOLDERS[i])))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from settings import *

from ScreenStart import StartScreen
from GeneralSettings import GeneralSettings
from BCIMenu import BCIMenu

from AcquisitionSettings import AcquisitionSettings

from CalMenu import CalMenu
from CalSettings import CalSettings
from CalStart import CalStart

from mlmenu import MlMenu

from GameMenu import GameMenu
from GameSettings import GameSettings
from BarsStart import BarsStart
from TargetStart import TargetStart

from drone_menu import DroneMenu
from drone_settings import DroneSettings
from drone_start import DroneStart

from kivy.properties import StringProperty

from SessionInfo import SessionHeader


class MyApp(App):

    def build(self):
        sh = SessionHeader()

        sm = ScreenManager()
        start_screen = StartScreen(sh, name='start')
        settings_screen = GeneralSettings(sh, name='GeneralSettings')
        bci_screen = BCIMenu(sh, name='BCIMenu')

        acquisition_settings_screen = AcquisitionSettings(
            sh, name='AcquisitionSettings')

        cal_screen = CalMenu(sh, name='CalMenu')
        cal_settings_screen = CalSettings(sh, name='CalSettings')
        cal_start_screen = CalStart(sh, name='CalStart')

        ml_screen = MlMenu(sh, name='MlMenu')

        game_screen = GameMenu(sh, name='GameMenu')
        game_settings_screen = GameSettings(sh, name='GameSettings')
        bars_start_screen = BarsStart(sh, name='BarsStart')
        target_start_screen = TargetStart(sh, name='TargetStart')

        ardrone_menu_screen = DroneMenu(sh, name='DroneMenu')
        ardrone_settings_screen = DroneSettings(sh, name='DroneSettings')
        ardrone_start_screen = DroneStart(sh, name='DroneStart')

        sm.add_widget(start_screen)
        sm.add_widget(settings_screen)
        sm.add_widget(bci_screen)

        sm.add_widget(acquisition_settings_screen)

        sm.add_widget(cal_screen)
        sm.add_widget(cal_settings_screen)
        sm.add_widget(cal_start_screen)

        sm.add_widget(ml_screen)

        sm.add_widget(game_screen)
        sm.add_widget(game_settings_screen)
        sm.add_widget(bars_start_screen)
        sm.add_widget(target_start_screen)

        sm.add_widget(ardrone_menu_screen)
        sm.add_widget(ardrone_settings_screen)
        sm.add_widget(ardrone_start_screen)

        sm.current = 'start'

        return sm


# run app
if __name__ == "__main__":
    # stream_thread.start()

    MyApp().run()
