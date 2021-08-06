import math
import pickle
import re
import datetime
from data import constants
from . import database_entry

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
        """
        Parameters
        ----------
        directory_name: str
            name of directory to be unpickled
        """
        self.dictionary_name = dictionary_name
        self._load_dictionary()

    def __del__(self):
        self._export_dictionary()

    def _load_dictionary(self):
        with open(f'/data/{dictionary_name}', 'rb') as file:
            self._dictionary = pickle.load(file)

    def _export_dictionary(self):
        with open(f'/data/{dictionary_name}', 'wb') as file:
            pickle.dump(self._dictionary, file)

    def find_words(self, word_regex):
        """
        Parameters
        ----------
        word_regex: str
            word in regex form to find in dictionary

        Returns
        -------
        List[Entry]:
            list of entries fitting the word's regex
        """

        list_of_entries = []
        for entry in self._dictionary:
            if re.fullmatch(word_regex, entry.word) is not None:
                list_of_entries.append(entry)

        return list_of_entries

    def update_word(self, entry):
        """
        Parameters
        ----------
        entry: str
            entry which you want to change
        """

        self._dictionary.remove(entry)
        self._dictionary.update(entry)

    def get_list_of_words(self):
        """
        Get lists of discovered and undiscovered words sorted according to the algorithm

        Returns
        -------
        Tuple[List[Entry], List[Entry]]:
            first element of the tuple is a list of discovered words, second element is a list of undiscovered words
        """
        
        discovered = []
        undiscovered = []

        for entry in self._dictionary:
            if entry.level == 0:
                undiscovered.append(entry)

            elif entry.level < 16 and entry.last_updated + datetime.timedelta(days=constants.TIME_DELAY[entry.level]) <= datetime.date.today():
                discovered.append(entry)

        return (sorted(discovered), sorted(undiscovered))