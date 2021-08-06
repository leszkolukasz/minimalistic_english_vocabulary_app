from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty

from .main_screen.main_screen import MainScreen
from .search_screen.search_screen import SearchScreen
from .view_screen.view_screen import ViewScreen

Builder.load_file('source/app/application.kv')

class MultiScreen(ScreenManager):
    pass

class HomeButton(BoxLayout):
    pass

class SearchButton(BoxLayout):
    pass

class ViewButton(BoxLayout):
    pass

class Area(BoxLayout):
    multi_screen = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def change_to_home(self):
        self.multi_screen.current = 'main'

    def change_to_search(self):
        self.multi_screen.current = 'search'

    def change_to_view(self):
        self.multi_screen.current = 'view'

class Main(App):
    def build(self):
        return Area()