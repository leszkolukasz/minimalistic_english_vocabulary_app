from functools import total_ordering
import math


@total_ordering
class Entry:
    """
    Entry in the database

    Attributes
    ----------
    word: str
        english word from dictionary
    frequency: int
        how often word appeared in dictionary
    level: int
        level of advancement which decides when to show the word in the app (default: 0)
    last_updated: datetime.date
        last time entry's attributes where changed
    tranlsation: str
        tranlation of word to Polish (default: None)
    Definition: Dict[str, List[str]]
        definiton of word, in English, grouped by parts of speech (default: None)
    Examples: Dict[str, List[str]]
        examples of word usage, in English, grouped by parts of speech (default: None)
    Synonyms: List[str]
        synonyms of word (default: None)
    Antonyms: List[str]
        antonyms of word (default: None)
    """
    def __init__(self, word, frequency):
        self.word = word
        self.frequency = frequency
        self.level = 0
        self.last_updated = None
        self.translation = None
        self.definition = None
        self.examples = None
        self.synonyms = None
        self.antonyms = None

    def __hash__(self):
        return hash(self.word)
    
    def __eq__(self, other):
        if type(self) is type(other):
            return self.word == other.word
        return False

    def __le__(self, other):
        if self.level < other.level:
            return True
        elif self.level > other.level:
            return False
        else:
            if self.frequency > other.frequency:
                return True
            elif self.frequency < other.frequency:
                return False
            return self.word < other.word