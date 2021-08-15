"""This module implements basic app layout"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, SwapTransition

from .edit_screen.edit_screen import EditScreen
from .list_screen.list_screen import ListScreen
from .main_screen.main_screen import MainScreen
from .search_screen.search_screen import SearchScreen

Builder.load_file('source/app/application.kv')


class MultiScreen(ScreenManager):
    pass


class HomeButton(BoxLayout):
    pass


class SearchButton(BoxLayout):
    pass


class ListButton(BoxLayout):
    pass


class Area(BoxLayout):
    """
    Main container which controlls position and behaviour of other widgers

    Attributes
    ----------
    multi_screen: ObjectProperty
        link to screen manager
    edit_screen: ObjectProperty
        link to edit screen
    """
    multi_screen = ObjectProperty(None)
    edit_screen = ObjectProperty(None)

    def change_to_home(self):
        self.multi_screen.transition = SwapTransition() if (
            self.multi_screen.current == 'edit') else SlideTransition()
        self.multi_screen.transition.direction = 'right'
        self.multi_screen.current = 'main'

    def change_to_search(self):
        self.multi_screen.transition = SwapTransition() if (
            self.multi_screen.current == 'edit') else SlideTransition()
        self.multi_screen.transition.direction = 'left' if self.multi_screen.current == 'main' else 'right'
        self.multi_screen.current = 'search'

    def change_to_list(self):
        self.multi_screen.transition = SwapTransition() if (
            self.multi_screen.current == 'edit') else SlideTransition()
        self.multi_screen.transition.direction = 'left'
        self.multi_screen.current = 'list'


class Main(App):
    """
    Main application

    Attributes
    ----------
    application: Area
        container which defines layout and behaviour of the app
    """
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.application = None

    def build(self):
        self.application = Area()
        return self.application

    def change_to_edit(self, instance, entry):
        self.application.edit_screen.current_entry = entry
        self.application.edit_screen.build_box_layout()
        self.application.multi_screen.transition = SwapTransition()
        self.application.multi_screen.current = 'edit'