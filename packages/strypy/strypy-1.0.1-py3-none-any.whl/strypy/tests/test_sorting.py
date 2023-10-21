'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers the testing of sorting.py
'''

import strypy as sp

def test_alphasort():
    assert sp.alphasort('cba') == 'abc', "sp.alphasort('cba') should return 'abc'"

def test_casesort():
    assert sp.casesort('aBc') == 'Bac', "sp.casesort('aBc') should return 'Bac'"