import math
from functools import total_ordering

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
    """
    def __init__(
        self,
        word,
        frequency
        ):
        """
        Parameters
        ----------
        word: str
            english word from dictionary
        frequency: int
            how often word appeared in dictionary
        """
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
