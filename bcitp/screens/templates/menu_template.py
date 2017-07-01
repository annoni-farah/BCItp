from kivy.factory import Factory
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import (StringProperty, ObjectProperty)

__all__ = ('StdMenuContainer', 'StdMenuTitle')


class StdMenuContainer(GridLayout):
    pass


class StdMenuButton(Button):
    title = StringProperty('<No title set>')
    destination = ObjectProperty()


class StdMenuTitle(Label):
    title = StringProperty('<No title set>')
    desc = StringProperty('')


Factory.register('StdMenuContainer', cls=StdMenuContainer)
Factory.register('StdMenuTitle', cls=StdMenuTitle)
Factory.register('StdMenuButton', cls=StdMenuTitle)
