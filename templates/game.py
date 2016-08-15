__all__ = ('GameContainer', 'GameSidePanel', 'GameBottomPanel',
    'GamePlayGround', 'GameBar', 'GameButtonPanel', 'GameInfoPanel')

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.properties import (StringProperty, NumericProperty, OptionProperty,
                             BooleanProperty)
from kivy.uix.popup import Popup

from kivy.garden.bar import Bar

Builder.load_file('templates/game.kv')

class GameContainer(BoxLayout):
    pass

class GameSidePanel(BoxLayout):
    pass

class GameBottomPanel(BoxLayout):
    pass

class GamePlayGround(BoxLayout):
    pass

class GameBar(Bar):
    pass

class GameButtonPanel(GridLayout):
    pass

class GameInfoPanel(BoxLayout):
    pass

# class StdSettingItem(GridLayout):
#     title = StringProperty('<No title set>')
#     desc = StringProperty('')


# class StdSettingTitle(Label):
#     title = StringProperty('<No title set>')
#     desc = StringProperty('')


# class StdSettingBoolean(StdSettingItem):
#     button_text = StringProperty('')
#     value = BooleanProperty(False)


# class StdSettingString(StdSettingItem):
#     value = StringProperty('')



Factory.register('GameContainer',cls=GameContainer)

