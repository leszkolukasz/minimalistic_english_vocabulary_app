import datetime
import math
import os
import pickle
import re

from data import constants
from .database_entry import Entry


class DatabaseCommunicatorSingleton(type):
    """Singleton metaclass for DatabaseCommunicator"""

    instance = None

    def __call__(self, dictionary_name):
        if DatabaseCommunicatorSingleton.instance is None:
            DatabaseCommunicatorSingleton.instance = super().__call__(dictionary_name)
        
        return DatabaseCommunicatorSingleton.instance


class DatabaseCommunicator(metaclass=DatabaseCommunicatorSingleton):
    """
    Extract pickled dictionary and create interface for easy communication with it

    Attributes
    ----------
    dictionary_name: str
        name of dictionary to be unpickled
    _dictionary: Set[Entry]
        unpickled dictionary
    """
    def __init__(self, dictionary_name):
        self.dictionary_name = dictionary_name
        self._load_dictionary()

    def __del__(self):
        self._export_dictionary()

    def _load_dictionary(self):
        with open(f'./data/{self.dictionary_name}.txt', 'rb') as file:
            self._dictionary = pickle.load(file)

    def export_dictionary(self):
        with open(f'./data/{self.dictionary_name}.txt', 'wb') as file:
            pickle.dump(self._dictionary, file)

    def find_words_by_regex(self, word_regex):
        list_of_entries = []
        for entry in self._dictionary:
            if re.fullmatch(word_regex, entry.word) is not None:
                list_of_entries.append(entry)
            if len(list_of_entries) > 1000:
                break
        list_of_entries = sorted(list_of_entries, key=lambda entry: entry.word)
        return list_of_entries

    def find_words_by_level(self, level):
        list_of_entries = []
        for entry in self._dictionary:
            if entry.level == level:
                list_of_entries.append(entry)
            
        list_of_entries = sorted(list_of_entries, key=lambda entry: entry.word)
        return list_of_entries

    def find_today_words(self):
        list_of_entries = []
        for entry in self._dictionary:
            if entry.last_updated == datetime.date.today():
                list_of_entries.append(entry)
            if len(list_of_entries) > 1000:
                break
        list_of_entries = sorted(list_of_entries, key=lambda entry: entry.word)
        return list_of_entries

    def update_word(self, entry):
        entry.last_updated = datetime.date.today()
        self._dictionary.remove(entry)
        self._dictionary.update([entry])

    def get_list_of_words(self):
        """
        Get lists of discovered and undiscovered words sorted according to the algorithm

        Algorithm
        ---------
        Word of level 0 are labeled as undiscovered. Words of level 16 are thought to be 
        known and are omitted. From the remaining words, chosen are those which were ment
        to be shown today or on the previous days (but were not shown).
        """
        discovered = []
        undiscovered = []

        for entry in self._dictionary:
            if entry.level == 0:
                undiscovered.append(entry)
            elif entry.level < 16 and (entry.last_updated
                + datetime.timedelta(days=constants.TIME_DELAY[entry.level])) <= datetime.date.today():
                discovered.append(entry)
        return (sorted(discovered), sorted(undiscovered))