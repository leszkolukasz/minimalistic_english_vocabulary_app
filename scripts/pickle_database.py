"""
Export pickled dictionary
"""

import pickle
from source.database.database_entry import Entry

def export():
    dictionary = set()
    with open('final_dictionary.txt', 'r') as source, open('dictionary', 'wb') as destination:

        for line in source:
            word, frequency = line.split()
            frequency = int(frequency)

            dictionary.update([Entry(word, frequency)])

        pickle.dump(dictionary, destination)

if __name__ == '__main__':
    export()