'''    
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

StryPy is a Python package to help developers work with strings quickly and effectively.
It provides a huge range of functions and objects that can be used to manipulate strings in almost any way you want.
The package also simplifies advanced string functions making them more accessable for the average programmer.

Basic usage with a few different functions:

    >>> import strypy as sp
    >>> sp.add("hello","world",spaces=True)
    'hello world'
    
    >>> sp.mesh("hello","world")
    'hweolrllod'
    
    >>> sp.split("hello, my, world",separator=", ")
    ['hello', 'my', 'world']
    
    >>> # file.txt contents = "hello, my, world"
    >>> sp.getstrings("/path/to/file.txt",separator = ", ")
    ['hello', 'my', 'world']
    
    >>> sp.switch("hello there","there","world")
    'hello world'
'''

from .basics import add, subtract, divchunks, remove
from .basics import join, split, splitdex, switch, switchchars, switchdex
from .basics import chars, uniques, reverse, mesh, length, count
from .file import read, getstrings, getchars
from .generator import randstr, numcode, asciidec
from .sorting import alphasort, casesort
from .clipboard import copy, paste
from .colour import fcolour, bcolour, style