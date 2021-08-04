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
        self.time_to_show = 0
