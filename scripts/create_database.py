"""This module extracts words from file into python dictionary object"""

def get_dictionary():
    with open('data/frequency_dictionary.txt', 'r') as dictionary:
        organised_dictionary = {}
        for line in dictionary:
            word, frequency = line.split()
            organised_dictionary[word] = int(frequency)

    return organised_dictionary