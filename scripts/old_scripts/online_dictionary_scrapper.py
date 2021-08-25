"""This module gets base form of a word using Dictionary.com website"""

import urllib.request
from bs4 import BeautifulSoup

def get_base_form(word):
    """
    Get base form of a word using Dictionary.com website

    Parameters
    ----------
    words : str
        word to get a base form from

    Results
    -------
    str
        base form of a word
    """

    with urllib.request.urlopen(r'https://www.dictionary.com/browse/' + word) as page:
        page_in_bytes = page.read()
        page_in_html = page_in_bytes.decode('utf8')

    soup = BeautifulSoup(page_in_html, 'html.parser')
    return soup.find('h1', class_='css-o8eka5 e1wg9v5m0').contents[0]