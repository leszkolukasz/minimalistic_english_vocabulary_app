"""This module defines list screen which shows all word that are learned or are being learned"""

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from source.database.database_communicator import DatabaseCommunicator
from source.database.batch_distributor import BatchDistributor
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
    scroll_view: Object Property
        link to scroll view
    _communicator: DatabaseCommunicator
        communicator that controls databse
    _batch_distributor: BatchDistributor
        object which divides list of entries into smaller batches
    """
    results = ObjectProperty(None)
    grid = ObjectProperty(None)
    box = ObjectProperty(None)
    scroll_view = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._communicator = DatabaseCommunicator('dictionary')
        self._batch_distributor = None
        Clock.schedule_once(lambda dt: self._bind_methods())
        Clock.schedule_once(lambda dt: self._build_buttons())

    def _bind_methods(self):
        self.results.bind(minimum_height=self.results.setter('height'))

    def _build_buttons(self):
        for i in range(15):
            self.grid.add_widget(self.button_builder(
                str(i),
                lambda instance, level=i: self.show_entries_by_level(instance, level)
                ))

        box_layout = BoxLayout(orientation='horizontal', size_hint_y=1)

        box_layout.add_widget(self.button_builder('15', lambda instance: self.show_entries_by_level(instance, 15)))
        box_layout.add_widget(self.button_builder('16', lambda instance: self.show_entries_by_level(instance, 16)))
        box_layout.add_widget(self.button_builder('Today', lambda instance: self.show_today_entries(instance), 3))

        self.box.add_widget(box_layout)

    def show_entries_by_level(self, instance, level):
        self._batch_distributor = BatchDistributor(self._communicator.find_words_by_level(level))
        self.update_results()
           
    def show_today_entries(self, instance):
        self._batch_distributor = BatchDistributor(self._communicator.find_today_words())
        self.update_results()

    def update_results(self):
        self.results.clear_widgets()
        entries = self._batch_distributor.get_batch()
        for entry in entries:
            btn = Button(
                text=entry.word,
                color=constants.FONT_COLOR,
                size_hint_y=None, height='50dp',
                on_release=lambda instance, entry=entry: App.get_running_app().change_to_edit(instance, entry),
                background_color=constants.BUTTON_COLOR,
                on_press=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR)
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

    def button_builder(self, text, on_release, size_hint_x=1):
        btn = Button(
                text=text,
                color=constants.FONT_COLOR,
                on_release=on_release,
                size_hint_x=size_hint_x,
                background_color=constants.BUTTON_COLOR,
                on_press=lambda instance: self.reset_button_color(instance)
            )
        btn.bind(on_release=lambda instance: self.change_button_color(instance, constants.BUTTON_PRESSED_COLOR))
        return btn
            
    def change_button_color(self, instance, color):
        instance.background_color = color

    def reset_button_color(self, instance):
        for widget in self.box.children:
            for inner_widget in widget.children:
                self.change_button_color(inner_widget, constants.BUTTON_COLOR)