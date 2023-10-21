Basics
======

StryPy includes many basic functions to aid users. Many of these do have extra parameters to elaborate on simple functions.

.. function:: sp.add(*args, spaces=False)

    *Returns a concatenated string*
    
    This function takes any number of strings and returns them concatenated.By setting the *spaces* parameter to true the function will return the string with spaces between each string:
        >>> sp.add("Hello","World", spaces=True)
        'Hello World'

.. function:: sp.subtract(String, num)

    *Returns a string with a certain number of characters removed off the end*
    
    This function removes a certain number of letters of the end of a string:
        >>> sp.subtract("Hello World", 3)
        'Hello Wo'

.. function:: sp.remove(String, removed, spaces=False)
    
    *Returns the string with a part removed*

    This function removes a string from a string, and can replace it with spaces by setting the *spaces* parameter to true:
        >>> sp.remove("Hello World", " World")
        'Hello'

.. function:: sp.join(List, spaces=False)
    
    *Returns a string made up of the ones in a list*
    
    This function takes a list of strings and joins it into one string.By setting the *spaces* parameter to true, it will add a space between each string:
        >>> sp.join(["Hello", "World"], spaces=True)
        'Hello World'

.. function:: sp.split(String, separator=None, Maxsplit=None)

    *Returns list of strings derived from a string*
    
    This function takes a string and splits it into a list of parts. The default separator is a space and you can specify the maximum amount of times to split the string:
        >>> sp.split("Hello World")
        ["Hello", "World]"

.. function:: sp.splitdex(String, splitpoint)

    *Returns a list of two parts of a string*
    
    This function takes a string and splits it into two parts at the index desired. It returns a list of the two parts:
        >>> sp.splitdex("Hello World", 4)
        ["Hell", "o World"]

.. function:: sp.switch(String, oldstring, newstring)

    *Returns a string with a replaced part*
    
    This function takes a string and replaces the *oldstring* part with the *newstring*:
        >>> sp.switch("Hello There", "There", "World")
        'Hello World'

.. function:: sp.switchchars(String, old, new)

    *Returns a string with a character replaced by another*
    
    This function takes a string and replaces every instance of the *old* character with the *new* character. It is case sensitive so 'A' is not the same as 'a':
        >>> sp.switchchars("Hello World","l","d")
        'Heddo Wordd'

.. function:: sp.switchdex(String, index, char)

    *Returns a string with the character at an index replaced by another*
    
    This function takes a string and replaces the character at a specific index with a different character. To be userfriendly, you can count from 1, rather than 0 for the index:
        >>> sp.switchdex("Gello World",1,"H")
        'Hello World'

.. function:: sp.chars(String)

    *Returns a list of characters*
    
    This function simply returns a list of each character of a string:
        >>> sp.chars("Hello World")
        ['H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd']

.. function:: sp.uniques(String)

    *Returns a list of the unique characters in a string*
    
    This function returns a list of all the unique characters in a string. It is case sensitive so 'A' is not the same as 'a':
        >>> sp.uniques("Hello World")
        [' ', 'd', 'e', 'H', 'l', 'o', 'r', 'W']
    
.. function:: sp.mesh(String1, String2)

    *Returns a string of two strings meshed together*
    
    This function meshes/interweaves two strings:
        >>> sp.mesh("Hello", "World")
        'HWeolrllod'
    
.. function:: sp.reverse(String)

    *Returns a reversed string*
    
    This function simply reverses a string:
        >>> sp.reverse("Hello World")
        'dlroW olleH'
    
.. function:: sp.length(String)

    *Returns the length of a string*
    
    This function simply returns the length of a string:
        >>> sp.length("Hello World)
        11

.. function:: sp.count(letter, String)

    *Returns the number of times a character appears in a string*
    
    This function simply returns amount of times a letter appears in a string. It is case sensitive so 'A' is not the same as 'a':
        >>> sp.count("l","Hello World")
        3
    
.. function:: sp.divchunks(String, chunksize)
    
    *Returns a list of strings*
    
    This function takes a string and divides it into chunks of a specified size. Any remainder will still be included:
        >>> sp.divchunks("Hello World", 3)
        ["Hel","lo ","Wor","ld"]