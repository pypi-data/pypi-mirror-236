Sorting
=======

StryPy has many sorting capabilities with strings.

.. function:: sp.alphasort(data, r=False)
    
    *Returns a string or list sorted alphabetically*
    
    This function sorts a string or list of strings into alphabetical order. The *r* parameter stands for reverseand means it sorts in reverse alphabetica/ order:
        >>> sp.alphasort("Hello World")
        ' deHllloorW'

.. function:: sp.casesort(String, List=False)

    *Returns a string or list sorted into upper and lower case letters*
    
    This function sorts a string into upper case and lower case letters. By setting *List* to True, it returns a list of two strings, one of upper case letters, and the other of lowercase letters:
        >>> sp.casesort("HEllo woRLd")
        'HERLllowod'