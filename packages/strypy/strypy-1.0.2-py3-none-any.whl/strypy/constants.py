'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file includes all constants to do with strings.
'''

import string

UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lower = 'abcdefghijklmnopqrstuvwxyz'
letters = UPPER + lower

digits = "0123456789"
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'

special = string.punctuation
whitespace = string.whitespace

printable = digits + letters + special + whitespace