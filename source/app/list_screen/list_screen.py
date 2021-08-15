"""This module defines list screen which shows all word that are learned or are being learned"""

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from source.database.database_communicator import DatabaseCommunicator
from source.database.database_entry import Entry
from data import constants

Builder.load_file('source/app/list_screen/list_screen.kv')


class ListScreen(Screen):
    """
    List screen which lists all words from dictionary grouped by their level

    Attributes
    ----------
    results: ObjectProperty
        link to field which shows words of given group
    grid: ObjectProperty
        link to grid layout
    box: ObjectProperty
        link to box layout
    _communicator: DatabaseCommunicator
        communicator that controls databse
    """
    results = ObjectProperty(None)
    grid = ObjectProperty(None)
    box = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._communicator = DatabaseCommunicator('dictionary')
        Clock.schedule_once(lambda dt: self._bind_methods())
        Clock.schedule_once(lambda dt: self._build_buttons())

    def _bind_methods(self):
        self.results.bind(minimum_height=self.results.setter('height'))

    def _build_buttons(self):
        for i in range(15):
            btn = Button(
                text=str(i),
                color=constants.FONT_COLOR,
                background_color=constants.BUTTON_COLOR,
                on_press=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR),
                on_release=lambda instance, level=i: self.show_entries_by_level(instance, level)
            )
            btn.bind(on_release=lambda instance: self.change_button_color(instance, constants.BUTTON_COLOR))
            self.grid.add_widget(btn)

        box_layout = BoxLayout(orientation='horizontal', size_hint_y=1)
        btn = Button(
            text='15',
            color=constants.FONT_COLOR,
            background_color=constants.BUTTON_COLOR,
            on_press=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR),
            on_release=lambda instance: self.show_entries_by_level(instance, 15)
        )
        btn.bind(on_release=lambda instance: self.change_button_color(instance, constants.BUTTON_COLOR))
        box_layout.add_widget(btn)

        btn = Button(
            text='16',
            color=constants.FONT_COLOR,
            background_color=constants.BUTTON_COLOR,
            on_press=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR),
            on_release=lambda instance: self.show_entries_by_level(instance, 16)
        )
        btn.bind(on_release=lambda instance: self.change_button_color(instance, constants.BUTTON_COLOR))
        box_layout.add_widget(btn)

        btn = Button(
            text='Today',
            size_hint_x=3,
            color=constants.FONT_COLOR,
            background_color=constants.BUTTON_COLOR,
            on_press=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR),
            on_release=lambda instance: self.show_today_entries(instance)
        )
        btn.bind(on_release=lambda instance: self.change_button_color(instance, constants.BUTTON_COLOR))
        box_layout.add_widget(btn)

        self.box.add_widget(box_layout)

    def show_entries_by_level(self, instance, level):
        self.results.clear_widgets()
        entries = self._communicator.find_words_by_level(level)
        for entry in entries:
            btn = Button(
                text=entry.word,
                color=constants.FONT_COLOR,
                size_hint_y=None,
                height='50dp',
                on_release=lambda instance,
                entry=entry: App.get_running_app().change_to_edit(instance, entry),
                background_color=constants.BUTTON_COLOR,
                on_press=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR)
            )
            btn.bind(on_release=lambda instance: self.change_button_color(instance, constants.BUTTON_COLOR))
            self.results.add_widget(btn)
           
    def show_today_entries(self, instance):
        self.results.clear_widgets()
        entries = self._communicator.find_today_words()
        for entry in entries:
            btn = Button(
                text=entry.word,
                color=constants.FONT_COLOR,
                size_hint_y=None, height='50dp',
                on_release=lambda instance,
                entry=entry: App.get_running_app().change_to_edit(instance, entry),
                background_color=constants.BUTTON_COLOR,
                on_press=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR)
            )
            btn.bind(on_release=lambda instance: self.change_button_color(instance, constants.BUTTON_COLOR))
            self.results.add_widget(btn)
            
    def change_button_color(self, instance, color):
        instance.background_color = color