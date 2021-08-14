"""This module defines main screen which is used for learning"""

import datetime

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock

from source.database.database_communicator import DatabaseCommunicator
from source.database.database_entry import Entry
from source.word_information.native_word_information_getter import NativeWordInformationGetter

Builder.load_file('source/app/main_screen/main_screen.kv')

class MainScreen(Screen):
    box_layout = ObjectProperty(None)
    word_name = ObjectProperty(None)
    word_translation = ObjectProperty(None)
    word_meaning = ObjectProperty(None)
    word_synonym = ObjectProperty(None)
    word_antonym = ObjectProperty(None)
    word_examples = ObjectProperty(None)
    know_button = ObjectProperty(None)
    not_know_button = ObjectProperty(None)
    previous_button = ObjectProperty(None)
    next_button = ObjectProperty(None)
    forget_button = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._communicator = DatabaseCommunicator('dictionary')
        self._translator = NativeWordInformationGetter()
        self.discovered, self.undiscovered = self._communicator.get_list_of_words()
        self.total_discovered_viewed = 0
        self.total_undiscovered_viewed = 0
        self.history = []
        self.current_entry = None
        Clock.schedule_once(lambda dt: self._bind_methods())
        Clock.schedule_once(lambda dt: self.build_box_layout())

    def _choose_entry(self):
        if (self.total_discovered_viewed + self.total_undiscovered_viewed + 1) % 50 == 0:
            if self.undiscovered:
                self.total_undiscovered_viewed += 1
                self.history.append('undiscovered')
                return self.undiscovered[self.total_undiscovered_viewed-1]
            elif self.discovered:
                self.total_discovered_viewed += 1
                self.history.append('discovered')
                return self.discovered[self.total_discovered_viewed-1]
            else:
                return Entry('No more words', 0)
        else:
            if self.discovered:
                self.total_discovered_viewed += 1
                self.history.append('discovered')
                return self.discovered[self.total_discovered_viewed-1]
            elif self.undiscovered:
                self.history.append('undiscovered')
                self.total_undiscovered_viewed += 1
                return self.undiscovered[self.total_undiscovered_viewed-1]
            else:
                return Entry('No more words', 0)

    def _bind_methods(self):
        self.know_button.bind(on_release=self.known_word_button)
        self.not_know_button.bind(on_release=self.unknown_word_button)
        self.previous_button.bind(on_release=self.previous_word)
        self.next_button.bind(on_release=self.next_word)
        self.forget_button.bind(on_release=self.forget_word)
        self.box_layout.bind(minimum_height=self.box_layout.setter('height'))

    def build_box_layout(self):
        self.current_entry = self._choose_entry()
        self.word_name.text = self.current_entry.word
        self.word_translation.text = self._translator.get_translation(self.current_entry)
        self.word_meaning.text = self._translator.get_definition(self.current_entry)
        self.word_synonym.text = self._translator.get_synonym(self.current_entry)
        self.word_antonym.text = self._translator.get_antonym(self.current_entry)
        self.word_examples.text = self._translator.get_examples(self.current_entry)
        
    def known_word_button(self, instance):
        self.current_entry.level += 1
        self.current_entry.last_updated = datetime.date.today()
        self._communicator.update_word(self.current_entry)
        self._communicator.export_dictionary()
        self.build_box_layout()

    def unknown_word_button(self, instance):
        self.current_entry.level = 1
        self.current_entry.last_updated = datetime.date.today()
        self._communicator.update_word(self.current_entry)
        self._communicator.export_dictionary()
        self.build_box_layout()

    def previous_word(self, instance):
        if len(self.history) == 1:
            return

        if self.history[-1] == 'discovered':
            self.total_discovered_viewed -= 1
        else:
            self.total_undiscovered_viewed -= 1
        self.history.pop()

        if self.history[-1] == 'discovered':
            self.total_discovered_viewed -= 1
        else:
            self.total_undiscovered_viewed -= 1
        self.history.pop()

        self.build_box_layout()

    def next_word(self, instance):
        self.build_box_layout()

    def forget_word(self, instance):
        self.current_entry.level = 16
        self.current_entry.last_updated = datetime.date.today()
        self._communicator.update_word(self.current_entry)
        self._communicator.export_dictionary()
        self.build_box_layout()
