'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers the testing of colour.py
'''

import strypy as sp
from colorama import Fore, Back, Style, just_fix_windows_console, init

just_fix_windows_console()

def test_fcolour():
    assert sp.fcolour('abc', 'RED') == '\033[31mabc\033[0m', "sp.fcolour('abc', 'RED') should return '\033[31mabc'(red text)"

def test_bcolour():
    assert sp.bcolour('abc', 'RED') == '\033[41mabc\033[0m', "sp.bcolour('abc', 'RED') should return '\033[41mabc'(red background)"

def test_style():
    assert sp.style('abc','DIM') == '\033[2mabc\033[0m', "sp.style('abc','DIM') should return '\033[2mabc'(dim text)"