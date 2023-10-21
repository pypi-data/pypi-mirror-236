Clipboard
=========

This StryPy utility takes advantage of pyperclip, a package containing basic copy and paste functions.

.. function:: sp.copy(string)
    
    *Copys a string to the clipboard*
    
    This function copys a specified string to your clipboard.
        >>> sp.copy("Hello World")

.. function:: sp.paste(Print=False)
    
    *Returns the contents of the clipboard*
    
    This function returns the contents of the clipboard, with an option to print it instead.
        >>> sp.copy("Hello World") # Initiliasing the clipboard with specified text (see above)
        >>> sp.paste()
        'Hello World'