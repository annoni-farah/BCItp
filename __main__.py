from kivy.app import App
from kivy.lang import Builder

import re
import os

from kivy.uix.screenmanager import ScreenManager

import screens.templates.settings_template

from utils.session_info import SessionHeader

from screens.start_screen import StartScreen
from screens.settings.general_settings import GeneralSettings
from screens.menus import BCIMenu, CalMenu, GameMenu, DroneMenu

from screens.settings.acquisition_settings import AcquisitionSettings

from screens.settings.cal_settings import CalSettings
from screens.cal.cal_start import CalStart

from screens.ml.ml_screen import MlMenu

from screens.game.game_settings import GameSettings
from screens.game.bars_start import BarsStart
from screens.game.target_start import TargetStart

from screens.game.drone_settings import DroneSettings
from screens.game.drone_start import DroneStart


def load_all_kv_files(start=os.path.dirname(__file__) + "/screens/kv"):
    print(start)
    pattern = re.compile(r".*?\.kv")
    kv_files = []
    for root, dirs, files in os.walk(start):
        kv_files += [root + "/" + file_ for file_ in files if pattern.match(file_)]

    for file_ in kv_files:
        Builder.load_file(file_)


class MyApp(App):

    def build(self):
        sh = SessionHeader()

        sm = ScreenManager()

        # CREATE SCREENS
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

        # ADD SCREENS TO SCREEN MANAGER
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

if __name__ == "__main__":
    load_all_kv_files()
    MyApp().run()
