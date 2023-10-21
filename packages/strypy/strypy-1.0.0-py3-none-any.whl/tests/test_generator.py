'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers the testing of generator.py
'''

import strypy as sp

def test_randstr():
    pass # TODO: Can't check if a string is random?

def test_numcode():
    assert sp.numcode('abc') == [1,2,3], "sp.numcode('abc') should return [1,2,3]"

def test_unidec():
    assert sp.unidec('abc') == [97,98,99], "sp.unidec('abc') should return [97,98,99]"

def test_unihex():
    assert sp.unihex('abc') == ['0x61', '0x62', '0x63'], "sp.unihex('abc') should return ['0x61', '0x62', '0x63']"
    
def test_unioct():
    assert sp.unioct('abc') == ['0o141', '0o142', '0o143'], "sp.unioct('abc') should return ['0o141', '0o142', '0o143']"