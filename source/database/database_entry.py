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
    time_to_show: int
        when to show word in the app (default: 0)
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
        self.time_to_show = math.inf

    def __hash__(self):
        return hash(self.word)
    
    def __eq__(self, other):
        if type(self) is type(other):
            return (self.word == other.word) and (self.frequency == other.frequency) and (self.time_to_show == other.time_to_show)
        return False

    def __le__(self, other):
        if self.time_to_show < other.time_to_show:
            return True
        elif self.time_to_show > other.time_to_show:
            return False
        else:
            if self.frequency > other.frequency:
                return True
            elif self.frequency < other.frequency:
                return False
            return self.word < other.word
