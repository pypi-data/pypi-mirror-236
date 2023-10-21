File
====

As well as using strings located in your Python script, StryPy enables you to load them from files.

.. function:: sp.read(file)
    
    *Returns the text from a file*
    
    Reads the text from a file and returns it as a string.
        >>> sp.read("path/to/file.txt")
        'File contents'

.. function:: sp.getstrings(file, separator=" ")

    *Returns a list of strings from a file*
    
    This function reads a file, then splits the resulting string into parts, with the specified separator.
        >>> sp.getstrings("/path/to/file.txt")
        ["File", "contents"]

.. function:: sp.getchars(file)

    *Returns a list of characters from a file*
    
    This function reads a file, then splits the resulting string into individual characters.
        >>> sp.getchars("/path/to/file.txt")
        ["F","i","l","e"," ","c","o","n","t","e","n","t","s"]