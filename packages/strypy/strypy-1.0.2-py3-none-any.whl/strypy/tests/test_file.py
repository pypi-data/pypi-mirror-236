'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers the testing of file.py
'''

import strypy as sp

def test_read():
    assert sp.read('test.txt') == 'abc abc', "sp.read('test.txt') should return 'abc abc'"

def test_getstrings():
    assert sp.getstrings('test.txt') == ['abc','abc'], "sp.getstrings('test.txt') should return ['abc','abc']"

def test_getchars():
    assert sp.getchars('test.txt') == ['a','b','c',' ','a','b','c'], "sp.getchars('test.txt') should return ['a','b','c',' ','a','b','c']"