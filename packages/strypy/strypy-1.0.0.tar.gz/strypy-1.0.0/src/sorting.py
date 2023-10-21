'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers sorting strings.
'''

from constants import UPPER, lower

def alphasort(data,r=False):
    '''
    Sorts a string or list of strings into alphabetical order.
    
    >>> sp.alphasort("Hello World")
    ' deHllloorW'
    '''
    
    if isinstance(data,list):
        c = data
        if r==True:
            c.sort(key=str.lower,reverse=True)
        else:
            c.sort(key=str.lower)
        return c
    elif isinstance(data,str):
        if r == True:
            return "".join(sorted(data,reverse=True, key = lambda x:x.lower()))
        else:
            return "".join(sorted(data, key = lambda x:x.lower()))
    else:
        return None

def casesort(String, List=False):
    '''
    Sorts a string into uppercase or lowercase.
    
    >>> sp.casesort("HEllo woRLd")
    'HERLllowod'
    '''
    
    if List == True:
        ret = []
        up=""
        low=""
        for letter in String:
            if letter in UPPER:
                up = up+letter
        for letter in String:
            if letter in lower:
                low=low+letter
        ret.append(up)
        ret.append(low)
        return ret
    else:
        ret = ""
        for letter in String:
            if letter in UPPER:
                ret=ret+letter
        for letter in String:
            if letter in lower:
                ret=ret+letter
        
        return ret
