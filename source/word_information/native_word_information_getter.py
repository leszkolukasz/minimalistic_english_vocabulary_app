"""This module defines class which extract information about a single word"""

from .word_information_getter import WordInformationGetter

class NativeWordInformationGetter(WordInformationGetter):
    """Manage communication with Entry class"""
    
    def get_translation(self, entry):
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
        return '' if entry.synonyms is None else ', '.join(entry.synonyms)

    def get_antonym(self, entry):
        return '' if entry.antonyms is None else ', '.join(entry.antonyms)

    def get_level(self, entry):
        return entry.level