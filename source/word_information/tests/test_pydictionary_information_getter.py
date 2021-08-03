from .. import pydictionary_word_information_getter as pwig

def test_methods():
    word_information_getter = pwig.PyDictionaryWordInformationGetter('pl')

    x = word_information_getter.get_translation('globetrotter')
    assert word_information_getter.get_translation('globetrotter') == 'obieżyświat', (
        'Wrong translation')

    x = {'Noun': [
        'a particular environment or walk of life', 
        'any spherically shaped artifact',
        'the geographical area in which one nation is very influential',
        'a particular aspect of life or activity',
        'a solid figure bounded by a spherical surface (including the space it encloses',
        'a three-dimensional closed surface such that every point on the surface is equidistant from the center',
        'the apparent surface of the imaginary sphere on which celestial bodies appear to be projected'
        ]}
    assert word_information_getter.get_definition('sphere') == x, 'Wrong definition'

    x = [
        'herb', 'Daucus', 'herbaceous plant', 'genus Daucus', 'cultivated carrot',
        'Daucus carota sativa'
        ]
    assert word_information_getter.get_synonym('carrot') == x, 'Wrong synonym'

    assert word_information_getter.get_antonym('hello') == ['love', 'like', 'goodness', 'good', 'benignity'], (
        'Wrong antonym')