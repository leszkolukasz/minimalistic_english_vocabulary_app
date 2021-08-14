from .word_information_getter import WordInformationGetter

class NativeWordInformationGetter(WordInformationGetter):
    """
    Manage communication with PyDictionary module

    Attributes
    ----------
    language: str
        abbrevation for language which is used for word translation
    dictionary: PyDictionary
        dictionary which is used for making operations on words
    """
    
    def __init__(self):
        """
        Parameters
        ----------
        language: str
            abbrevation for language which is used for word translation
        """
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

        return str(entry.translation)

    def get_definition(self, entry):
        if entry.definition is None:
            return ''
        else:
            result = []
            for word_type in entry.definition:
                paragraph = word_type + ':\n'
                definitions = []
                for definition in entry.definition[word_type]:
                    definitions.append(' - ' + definition)
                paragraph += '\n'.join(definitions)
                result.append(paragraph)
            return '\n\n'.join(result)

    def get_examples(self, entry):
        if entry.definition is None:
            return ''
        else:
            result = []
            for word_type in entry.examples:
                paragraph = word_type + ':\n'
                examples = []
                for definition in entry.examples[word_type]:
                    examples.append(' - ' + definition)
                paragraph += '\n'.join(examples)
                result.append(paragraph)
            return '\n\n'.join(result)

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
        return '' if entry.synonyms is None else ', '.join(entry.synonyms)

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
        return '' if entry.antonyms is None else ', '.join(entry.antonyms)