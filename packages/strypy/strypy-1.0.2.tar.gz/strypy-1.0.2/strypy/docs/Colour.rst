Colour
======

One of the most unknown features of Python is the ability to colour and style strings. StryPy makes the process a fair bit easier, by using the colorama module.

For the two colouring functions the options for the colour parameters are:
    - 'RED'
    - 'BLACK'
    - 'GREEN'
    - 'YELLOW'
    - 'MAGENTA'
    - 'CYAN'
    - 'WHITE'
    - 'BLUE'
    
.. function:: sp.fcolour(String, f)
    
    *Colours the text (foreground) of a string*
    
    This function colors the foreground (the actual text) of a string:
        >>> sp.fcolour("Hello World", "RED")
        [ 'Hello World' with red text ]
        
.. function:: sp.bcolour(String, b)
    
    *Colours the background of a string*
    
    This function colors the background of a string:
        >>> sp.bcolour("Hello World", "RED")
        [ 'Hello World' with red background ]
        
.. function:: sp.style(String, s)
    
    *Styles a string (brightness)*
    
    This function changes the brightness of a string. Different styles are 'DIM', 'BRIGHT' and 'NORMAL':
        >>> sp.style("Hello World", "DIM")
        [ 'Hello World' with dim text ]