"""This module defines search screen which allows to search for entries"""

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App

from source.database.database_communicator import DatabaseCommunicator

Builder.load_file('source/app/search_screen/search_screen.kv')

class SearchScreen(Screen):
    results = ObjectProperty(None)
    searched_word = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._communicator = DatabaseCommunicator('dictionary')
        Clock.schedule_once(lambda dt: self._bind_methods())

    def _bind_methods(self):
        self.searched_word.bind(text=self._search_for_words)
        self.results.bind(minimum_height=self.results.setter('height'))

    def _search_for_words(self, instance, word):
        if len(word) < 2:
            return

        entries = self._communicator.find_words(f'{word}.*')
        self.update_results(entries)

    def update_results(self, entries):
        self.results.clear_widgets()
        for entry in entries:
            self.results.add_widget(Button(text=entry.word, size_hint_y=None, height='50dp', on_release=lambda instance, entry=entry: App.get_running_app().change_to_edit(instance, entry)))