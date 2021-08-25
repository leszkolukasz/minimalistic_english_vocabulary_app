"""This module defines class which extracts information about a single word using PyDictionary"""

import PyDictionary

from .word_information_getter import WordInformationGetter

class PyDictionaryWordInformationGetter(WordInformationGetter):
    """
    Manage communication with PyDictionary module

    Attributes
    ----------
    language: str
        abbrevation for language which is used for word translation
    dictionary: PyDictionary
        dictionary which is used for making operations on words
    """
    
    def __init__(self, language):
        self.language = language
        self.dictionary = PyDictionary.PyDictionary()
        super().__init__()

    def get_translation(self, entry):
        return self.dictionary.translate(entry.word, self.language)

    def get_definition(self, entry):
        return self.dictionary.meaning(entry.word)

    def get_synonym(self, entry):
        return self.dictionary.synonym(entry.word)

    def get_antonym(self, entry):
        return self.dictionary.antonym(entry.word)