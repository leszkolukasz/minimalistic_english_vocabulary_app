"""This module defines search screen which allows to search for entries"""

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from data import constants
from source.database.database_communicator import DatabaseCommunicator
from source.database.batch_distributor import BatchDistributor

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
    scroll_view: Object Property
        link to scroll view
    _communciator: DatabaseCommunicator
        communicator for connection with database
    _batch_distributor: BatchDistributor
        object which divides list of entries into smaller batches
    """
    results = ObjectProperty(None)
    searched_word = ObjectProperty(None)
    scroll_view = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._communicator = DatabaseCommunicator('dictionary')
        self._batch_distributor = None
        Clock.schedule_once(lambda dt: self._bind_methods())

    def _bind_methods(self):
        self.searched_word.bind(text=self._search_for_words)
        self.results.bind(minimum_height=self.results.setter('height'))

    def _search_for_words(self, instance, word):
        if len(word) < 2:
            return

        self._batch_distributor = BatchDistributor(self._communicator.find_words_by_regex(f'{word}.*'))
        self.update_results()

    def update_results(self):
        self.results.clear_widgets()
        entries = self._batch_distributor.get_batch()
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

        if self._batch_distributor.is_batch():
            btn = Button(
                    text='More',
                    color=constants.FONT_COLOR,
                    size_hint_y=None, height='50dp',
                    on_release=lambda instance: self.update_results(),
                    background_color=constants.BUTTON_COLOR,
                    on_press=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR)
                )
            btn.bind(on_release=lambda instance: self.change_button_color(instance, constants.BUTTON_COLOR))
            self.results.add_widget(btn)
        self.scroll_view.scroll_y = 1

    def change_button_color(self, instance, color):
        instance.background_color = color