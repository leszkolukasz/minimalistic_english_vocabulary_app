"""This script cleans database and pickles it"""

from collections import defaultdict
import os
import sys
sys.path.append('/home/whistleroosh/Desktop/minimalistic_english_vocabulary_app')

from deep_translator import GoogleTranslator
from nltk.corpus import wordnet
import inflect
import pickle

from source.database.database_entry import Entry
import create_database

nouns = {x.name().split('.', 1)[0] for x in wordnet.all_synsets('n')}
inflect_engine = inflect.engine()

def get_translation(word):
    return GoogleTranslator(source='en', target='pl').translate(text=word)

def get_definition(word):
    definitions = defaultdict(set)
    for syn in wordnet.synsets(word):
        if not syn.definition():
            continue
        if syn.pos() == 'v':
            definitions['Verb'].update([syn.definition()])
        elif syn.pos() == 'n':
            definitions['Noun'].update([syn.definition()])
        elif syn.pos() == 'a':
            definitions['Adjective'].update([syn.definition()])
        elif syn.pos() == 'r':
            definitions['Adverb'].update([syn.definition()])
    for part in definitions:
        definitions[part] = list(definitions[part])
    return definitions

def get_synonym(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.name() != word:
                synonyms.append(l.name())
    for pos, syn in enumerate(synonyms):
        for idx, letter in enumerate(syn):
            if letter == '_':
                synonyms[pos] = synonyms[pos][:idx] + ' ' + synonyms[pos][idx+1:]
    return list(set(synonyms))

def get_antonym(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    for pos, ant in enumerate(antonyms):
        for idx, letter in enumerate(ant):
            if letter == '_':
                antonyms[pos] = antonyms[pos][:idx] + ' ' + antonyms[pos][idx+1:]
    return list(set(antonyms))

def get_examples(word):
    examples = defaultdict(set)
    for syn in wordnet.synsets(word):
        if syn.pos() == 'v':
            for ex in syn.examples():
                if word in ex:
                    examples['Verb'].update([ex])
        elif syn.pos() == 'n':
            for ex in syn.examples():
                if word in ex:
                    examples['Noun'].update([ex])
        elif syn.pos() == 'a':
            for ex in syn.examples():
                if word in ex:
                    examples['Adjective'].update([ex])
        elif syn.pos() == 'r':
            for ex in syn.examples():
                if word in ex:
                    examples['Adverb'].update([ex])
    for part in examples:
        examples[part] = list(examples[part])
    return examples

def make_third_person_form(word):
    res = ""
    if word.endswith("y"):
        res = word[:-1]+"ies"
    elif word.endswith("o") or word.endswith("ch") or word.endswith("s") or word.endswith("sh") or word.endswith("x") or word.endswith("z"):
        res = word + "es"
    else:   
        res = word + "s" 
    return res

def clean_dictionary():
    #remove words with unknown frequency
    frequency_dictionary = create_database.get_dictionary()
    word_dictionary = set()
    with open('data/word_dictionary.txt', 'r') as dictionary:
        for word in dictionary:
            word = word[:-1]
            if word in frequency_dictionary:
                word_dictionary.update([word])
    
    #remove words in 3rd person from
    word_dictionary_without_3rd_person = set()
    blocked = set()
    for word in word_dictionary:
        if make_third_person_form(word) in word_dictionary:
            blocked.update([make_third_person_form(word)])
    for word in word_dictionary:
        if word not in blocked:
            word_dictionary_without_3rd_person.update([word])

    #remove words in plural form
    word_dictionary_cleaned = set()
    blocked = set()
    for word in word_dictionary_without_3rd_person:
        if word in nouns and inflect_engine.plural(word) != word and inflect_engine.plural(word) in word_dictionary_without_3rd_person:
            blocked.update([inflect_engine.plural(word)])
    for word in word_dictionary_without_3rd_person:
        if word not in blocked:
            word_dictionary_cleaned.update([word])

    word_dictionary_cleaned = sorted(list(word_dictionary_cleaned))
    entry_dictionary = set()

    for word in word_dictionary_cleaned:
        entry = Entry(word, frequency_dictionary[word])
        entry.translation = get_translation(word)
        entry.definition = get_definition(word)
        entry.synonyms = get_synonym(word)
        entry.antonyms = get_antonym(word)
        entry.examples = get_examples(word)
        entry_dictionary.update([entry])

    with open('data/dictionary.txt', 'wb') as destination:
        pickle.dump(entry_dictionary, destination)


if __name__ == '__main__':
    clean_dictionary()