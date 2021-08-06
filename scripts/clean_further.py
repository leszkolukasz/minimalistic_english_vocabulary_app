"""This module is meant to be run after clean_database.py. It further cleans database"""

import PyDictionary

def clean_database():
    """
    Get rid of word with no entry in PyDictionary
    """

    dictionary = PyDictionary.PyDictionary()

    with open('data/cleaned_dictionary.txt', 'r') as saved, open('data/cleaned_dictionary_v2.txt', 'r+') as destination:
        for line in destination:
            word, frequency, position = line.split()
            frequency, position = map(int, [frequency, position])

        for line in saved:
            word, frequency, cnt = line.split()
            frequency, cnt = map(int, [frequency, cnt])

            if cnt <= position:
                continue

            try:
                word = dictionary.translate(word, 'pl')
            except Exception as e:
                print(e)
            
            else:
                if word is not None:
                    destination.write(f"{word} {frequency} {cnt}\n")
                    destination.flush()
                    print(word, cnt)

            
        
if __name__ == '__main__':
    clean_database()