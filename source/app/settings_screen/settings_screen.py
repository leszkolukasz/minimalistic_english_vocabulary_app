"""This module defines settings screen which allows to export and import dictonary"""

import os
import shutil
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

from data import constants
from source.database.database_communicator import DatabaseCommunicator

Builder.load_file('source/app/settings_screen/settings_screen.kv')


class SettingsScreen(Screen):
    """
    Settings screen which allows to import and export dictionary

    Attributes
    ----------
    export_button: ObjectProperty
        link to button which exports dictionary
    import_button: Object property
        link to button which imports dictionary
    message: ObjectProperty
        link to field which display information for user
    """
    export_button = ObjectProperty(None)
    import_button = ObjectProperty(None)
    message = ObjectProperty(None)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._communicator = DatabaseCommunicator('dictionary')
        Clock.schedule_once(lambda dt: self._bind_methods())

    def _bind_methods(self):
        self.export_button.bind(on_release=lambda instance: self.export_dictionary(instance))
        self.import_button.bind(on_release=lambda instance: self.import_dictionary(instance))

    def import_dictionary(self, instance):
        if platform != 'android':
            return
        try:
            shutil.copy('/storage/emulated/0/dictionary.txt', './data/')
        except Exception as e:
            self.message.text = str(e)
        else:
            self.message.text = 'App will exit shortly'
            Clock.schedule_once(lambda: App.get_running_app().stop(), 3)

    def export_dictionary(self, instance):
        if platform != 'android':
            return
        try:
            shutil.copy('./data/dictionary.txt', '/storage/emulated/0/')
        except Exception as e:
            self.message.text = str(e)
        else:
            self.message.text = 'Exported successfully'
