"""This module cleans database and exports it using pickle"""

import create_database
import online_dictionary_scrapper

def clean_database():
    """
    Get rid of letters and nonbase forms of words
    """

    dictionary = create_database.get_dictionary()

    with open('data/cleaned_dictionary.txt', 'r+') as saved:
        for line in saved:
            word, frequency, position = line.split()
            frequency, position = map(int, [frequency, position])

        for cnt, (word, frequency) in enumerate(dictionary.items(), 1):
            if cnt <= position:
                continue

            if len(word) == 1:
                continue
            try:
                word = online_dictionary_scrapper.get_base_form(word)
            except Exception as e:
                print(e)
            else:
                saved.write(f"{word} {frequency} {cnt}\n")
                saved.flush()
                print(word, cnt)

            
        
if __name__ == '__main__':
    clean_database()