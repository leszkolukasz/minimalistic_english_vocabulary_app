"""This module extracts words from file into python dictionary object"""

def get_dictionary():
    """
    Extract words from file into python dictionary object

    Returns
    -------
    Dict[str, int]
        dictionary containing all english words and their frequency of appearance
    """
    
    with open('data/frequency_dictionary.txt', 'r') as dictionary:
        organised_dictionary = {}
        for line in dictionary:
            word, frequency = line.split()
            organised_dictionary[word] = int(frequency)

    return organised_dictionary