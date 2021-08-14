"""This module defines edit screen which is used to edit entries found by search screen"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from source.database.database_communicator import DatabaseCommunicator
from source.database.database_entry import Entry
from source.word_information.native_word_information_getter import NativeWordInformationGetter

Builder.load_file('source/app/edit_screen/edit_screen.kv')

class EditScreen(Screen):
    box_layout = ObjectProperty(None)
    word_name = ObjectProperty(None)
    word_translation = ObjectProperty(None)
    word_meaning = ObjectProperty(None)
    word_synonym = ObjectProperty(None)
    word_antonym = ObjectProperty(None)
    word_examples = ObjectProperty(None)
    level_input = ObjectProperty(None)
    submit_button = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._communicator = DatabaseCommunicator('dictionary')
        self._translator = NativeWordInformationGetter()
        self.current_entry = None
        Clock.schedule_once(lambda dt: self._bind_methods())

    def _bind_methods(self):
        self.box_layout.bind(minimum_height=self.box_layout.setter('height'))
        self.submit_button.bind(on_release=self.submit_level_change)

    def build_box_layout(self):
        self.word_name.text = self.current_entry.word
        self.word_translation.text = self._translator.get_translation(self.current_entry)
        self.word_meaning.text = self._translator.get_definition(self.current_entry)
        self.word_synonym.text = self._translator.get_synonym(self.current_entry)
        self.word_antonym.text = self._translator.get_antonym(self.current_entry)
        self.word_examples.text = self._translator.get_examples(self.current_entry)

    def submit_level_change(self, instance):
        value = self.level_input.text
        try:
            value = int(value)
        except Exception:
            self.level_input.text = 'Not number'
        else:
            if value < 0 or value > 16:
                self.level_input.text = 'Value must be in range [0, 16]'
            else:
                self.current_entry.level = value
                self._communicator.update_word(self.current_entry)
                self.level_input.text = 'Changed successfully'