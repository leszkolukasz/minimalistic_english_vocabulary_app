from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from source.database.database_communicator import DatabaseCommunicator
from source.database.database_entry import Entry

Builder.load_file('source/app/main_screen/main_screen.kv')

class MainScreen(Screen):
    scroll_box_layout = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        
        super().__init__(*args, **kargs)
        #self._communicator = DatabaseCommunicator('database')
        #self.discovered, self.undiscovered = self._communicator.get_list_of_words()
        self.total_viewed = 0
        self._build_box_layout()

    def _choose_entry(self):
        x = Entry('hello', 10)
        return x

    def _build_box_layout(self):
        entry = self._choose_entry()

        for i in range(100):
            self.scroll_box_layout.add_widget(Button(text=str(i), size_hint_y=None, height=40))
        
