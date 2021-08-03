import PyDictionary
from . import word_information_getter

class PyDictionaryWordInformationGetter():
    """
    Manage communication with PyDictionary module

    Attributes
    ----------
    language: str
        abbrevation for language which is used for word translation
    dictionary: PyDictionary
        dictionary which is used for making operations on words
    """
    
    def __init__(
        self, 
        language
        ):
        """
        Parameters
        ----------
        language: str
            abbrevation for language which is used for word translation
        """
        self.language = language
        self.dictionary = PyDictionary.PyDictionary()
        super().__init__()

    def get_translation(self, word):
        """
        Get translation of word

        Parameters
        ----------
        word: str
            word to be translated

        Returns
        -------
        str
            translated word
        """

        return self.dictionary.translate(word, self.language)

    def get_definition(self, word):
        """
        Get definition of word

        Parameters
        ----------
        word: str
            word to get definition for

        Returns
        -------
        List[str]
            definition of word
        """
        return self.dictionary.definition(word)

    def get_synonym(self, word):
        """
        Get synonyms of word

        Parameters
        ----------
        word: str
            word to get synonyms for

        Returns
        -------
        List[str]
            synonyms of word
        """
        return self.dictionary.synonym(word)

    def get_antonym(self, word):
        """
        Get antonyms of word

        Parameters
        ----------
        word: str
            word to get antonyms for

        Returns
        -------
        List[str]
            antonyms of word
        """
        return self.dictionary.antonym(word)