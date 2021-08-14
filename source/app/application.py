from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition, SlideTransition
from kivy.properties import ObjectProperty

from .main_screen.main_screen import MainScreen
from .search_screen.search_screen import SearchScreen
from .edit_screen.edit_screen import EditScreen
from .list_screen.list_screen import ListScreen

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
    multi_screen = ObjectProperty(None)
    edit_screen = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def change_to_home(self):
        self.multi_screen.transition = FadeTransition() if (
            self.multi_screen.current == 'edit') else SlideTransition()
        self.multi_screen.transition.direction = 'right'
        self.multi_screen.current = 'main'

    def change_to_search(self):
        self.multi_screen.transition = FadeTransition() if (
            self.multi_screen.current == 'edit') else SlideTransition()
        self.multi_screen.transition.direction = 'left' if self.multi_screen.current == 'main' else 'right'
        self.multi_screen.current = 'search'

    def change_to_list(self):
        self.multi_screen.transition = FadeTransition() if (
            self.multi_screen.current == 'edit') else SlideTransition()
        self.multi_screen.transition.direction = 'left'
        self.multi_screen.current = 'list'

class Main(App):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.application = None

    def build(self):
        self.application = Area()
        return self.application

    def change_to_edit(self, instance, entry):
        self.application.edit_screen.current_entry = entry
        self.application.edit_screen.build_box_layout()
        self.application.multi_screen.transition = FadeTransition()
        self.application.multi_screen.current = 'edit'