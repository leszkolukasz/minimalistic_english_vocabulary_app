"""This module defines class which divides list of entries into smaller batches"""

class BatchDistributor:
    """
    Divide list of entires into smaller batches and create interface to get them one by one

    Attributes
    ----------
    entries: List[Entry]
    list of entries to be later divided into batches
    """

    def __init__(self, entries):
        self.entries = list(reversed(entries))

    def get_batch(self):
        number_of_entries = min(len(self.entries), 500)
        batch = []
        
        while number_of_entries:
            number_of_entries -= 1
            batch.append(self.entries[-1])
            self.entries.pop()

        return batch

    def is_batch(self):
        return True if self.entries else False