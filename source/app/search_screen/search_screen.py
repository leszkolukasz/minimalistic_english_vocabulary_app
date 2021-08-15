"""This module defines search screen which allows to search for entries"""

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from data import constants
from source.database.database_communicator import DatabaseCommunicator

Builder.load_file('source/app/search_screen/search_screen.kv')


class SearchScreen(Screen):
    """
    Search screen which allows to search for words and edit them

    Attributes
    ----------
    results: ObjectProperty
        link to field which displays searched words
    searched_words: Object property
        link to text field which describes searched word
    _communciator: DatabaseCommunicator
        communicator for connection with database
    """
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

        entries = self._communicator.find_words_by_regex(f'{word}.*')
        self.update_results(entries)

    def update_results(self, entries):
        self.results.clear_widgets()
        for entry in entries:
            btn = Button(
                text=entry.word,
                size_hint_y=None,
                height='50dp',
                color=constants.FONT_COLOR,
                background_color=constants.BUTTON_COLOR,
                on_press=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR),
                on_release=lambda instance, entry=entry: App.get_running_app().change_to_edit(instance, entry)
            )
            btn.bind(on_release=lambda instance: self.change_button_color(instance, constants.BUTTON_COLOR))
            self.results.add_widget(btn)

    def change_button_color(self, instance, color):
        instance.background_color = color