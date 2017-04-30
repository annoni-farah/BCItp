from kivy.factory import Factory
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import (StringProperty)

__all__ = ('StdMenuContainer', 'StdMenuItem', 'StdMenuTitle')


class StdMenuContainer(GridLayout):
    pass


class StdMenuItem(GridLayout):
    title = StringProperty('<No title set>')
    desc = StringProperty('')


class StdMenuTitle(Label):
    title = StringProperty('<No title set>')
    desc = StringProperty('')


Factory.register('StdMenuContainer', cls=StdMenuContainer)
Factory.register('StdMenuTitle', cls=StdMenuTitle)
