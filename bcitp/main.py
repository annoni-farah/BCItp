#! /usr/bin/env python

from kivy.app import App
from kivy.lang import Builder

import re
import os

from kivy.uix.screenmanager import ScreenManager

from .data_headers.session_info import SessionHeader

import bcitp.screens.templates.settings_template

from .screens.menus.menus import StartScreen

from .screens.menus.menus import BCIMenu
from .screens.menus.menus import CalMenu
from .screens.menus.menus import GameMenu

from screens.settings.acquisition_settings import AcquisitionSettings

# from screens.settings.cal_settings import CalSettings
# from screens.cal.cal_start import CalStart

# from screens.ml.ml_screen import MlMenu

# from screens.game.game_settings import GameSettings
# from screens.game.bars_start import BarsStart
# from screens.game.target_start import TargetStart


# LOAD ALL KV FILES


def load_all_kv_files(start="screens/kv"):
    pattern = re.compile(r".*?\.kv")
    kv_files = []
    for root, dirs, files in os.walk(start):
        kv_files += [root + "/" +
                     file_ for file_ in files if pattern.match(file_)]

    for file_ in kv_files:
        Builder.load_file(file_)


class BCItp(App):

    def build(self):
        sh = SessionHeader()

        sm = ScreenManager()

        # CREATE SCREENS
        start_menu = StartScreen(sh, name='start')
        # settings_screen = GeneralSettings(sh, name='GeneralSettings')
        bci_screen = BCIMenu(sh, name='BCIMenu')

        acquisition_settings_screen = AcquisitionSettings(
            sh, name='AcquisitionSettings')

        cal_screen = CalMenu(sh, name='CalMenu')
        # cal_settings_screen = CalSettings(sh, name='CalSettings')
        # cal_start_screen = CalStart(sh, name='CalStart')

        # ml_screen = MlMenu(sh, name='MlMenu')

        game_screen = GameMenu(sh, name='GameMenu')
        # game_settings_screen = GameSettings(sh, name='GameSettings')
        # bars_start_screen = BarsStart(sh, name='BarsStart')
        # target_start_screen = TargetStart(sh, name='TargetStart')

        # ADD SCREENS TO SCREEN MANAGER
        sm.add_widget(start_menu)

        # sm.add_widget(settings_screen)
        sm.add_widget(bci_screen)

        sm.add_widget(acquisition_settings_screen)

        sm.add_widget(cal_screen)
        # sm.add_widget(cal_settings_screen)
        # sm.add_widget(cal_start_screen)

        # sm.add_widget(ml_screen)

        sm.add_widget(game_screen)
        # sm.add_widget(game_settings_screen)
        # sm.add_widget(bars_start_screen)
        # sm.add_widget(target_start_screen)

        sm.current = 'start'

        return sm

if __name__ == "__main__":
    # try:
        # load_all_kv_files()
        # MyApp().run()
    # except Exception as e:
    #     print(e)
    load_all_kv_files()
    BCItp().run()
