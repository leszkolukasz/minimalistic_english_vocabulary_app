"""This module is meant to be run after clean_further.py. It merges duplicates"""

def clean_database():
    """
    Get rid of duplicates
    """

    clean_dictionary = {}

    with open('data/cleaned_dictionary_v2.txt', 'r') as saved, open('data/final_dictionary.txt', 'w') as destination:
        
        for line in saved:
            word, frequency, cnt = line.split()
            frequency, cnt = map(int, [frequency, cnt])

            if word in clean_dictionary:
                clean_dictionary[word] += frequency

            else:
                clean_dictionary[word] = frequency

        for (word, frequency) in clean_dictionary.items():
            destination.write(f'{word} {frequency}')

            
        
if __name__ == '__main__':
    clean_database()