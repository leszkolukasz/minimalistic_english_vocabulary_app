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
        """
        Parameters
        ----------
        language: str
            abbrevation for language which is used for word translation
        """
        self.language = language
        self.dictionary = PyDictionary.PyDictionary()
        super().__init__()

    def get_translation(self, entry):
        """
        Parameters
        ----------
        word: str
            word to be translated

        Returns
        -------
        str
            translated word
        """

        return self.dictionary.translate(entry.word, self.language)

    def get_definition(self, entry):
        """
        Parameters
        ----------
        word: str
            word to get definition for

        Returns
        -------
        List[str]
            definition of word
        """
        return self.dictionary.meaning(entry.word)

    def get_synonym(self, entry):
        """
        Parameters
        ----------
        word: str
            word to get synonyms for

        Returns
        -------
        List[str]
            synonyms of word
        """
        return self.dictionary.synonym(entry.word)

    def get_antonym(self, entry):
        """
        Parameters
        ----------
        word: str
            word to get antonyms for

        Returns
        -------
        List[str]
            antonyms of word
        """
        return self.dictionary.antonym(entry.word)