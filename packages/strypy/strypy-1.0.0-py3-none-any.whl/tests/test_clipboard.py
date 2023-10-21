'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers the testing of clipboard.py
'''

import strypy as sp

def test_copypaste():
    sp.copy('abc')
    assert sp.paste() == 'abc', "After running sp.copy('abc'), sp.paste() should return 'abc'"