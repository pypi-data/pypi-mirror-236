'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers clipboard actions, using the module pyperclip.  
'''

import pyperclip as p

### Copy and Paste ###

def copy(string):
    '''
    Takes advantage of the copy() function from 'pyperclip' to copy strings to the clipboard.
    
    >>> sp.copy("Hello World")
    '''
    
    p.copy(string)

def paste(Print=False):
    '''
    Returns the contents of the clipboard, with an option to print().
    
    >>> sp.copy("Hello World") # Initiliasing the clipboard with specified text (see above)
    >>> sp.paste()
    'Hello World'
    '''
    
    if Print==True:
        print(p.paste())
        return None
    else:
        return p.paste()