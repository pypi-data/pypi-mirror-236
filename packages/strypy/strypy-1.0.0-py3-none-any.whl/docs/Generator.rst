Generator
=========

Strypy features an advanced range of string generators and convertors, including random strings and Unicode conversions.

.. function:: sp.randstr(minlength=1, maxlength=50, lower=True, upper=True, digit=True, special=True, character_string=None)
    
    *Returns a random string*
    
    This advanced random string generator features 7 specific parameters to customise your string:
        - minlength - defines the minimum length of the string (integer, default = 1)
        - maxlength - defines the maximum length of the string (integer, default = 50)
        - lower - Include lowercase characters (boolean, default = True)
        - upper - Include uppercase characters (boolean, default = True)
        - digit - Include digits (boolean, default = True)
        - special - Include special characters (boolean, default = True)
        - character_string - Only use characters specified by the user (string, default = None)
    
    Usage:
        >>> sp.randstr()
        '+T-MY||e_8Dt(Gc?,H%D3*uIejx<i3}4' # Similar to this

.. function:: sp.numcode(String)
    
    *Convert a string to numbers according to the alphabet*
    
    This function converts a string into a series of numbers according to each letter's place in the alphabet:
        >>> sp.numcode("hello world")
        [8, 5, 12, 12, 15, 0, 23, 15, 18, 12, 4]
        
.. function:: sp.unidec(String)
    
    *Returns the Unicode decimal values of the string*
    
    This function is the first of the Unicode conversion functons that StryPy offers. It converts your string to a list of Unicode decimal values:
        >>> sp.unidec("Hello World")
        [72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100]

.. function:: sp.unihex(String)
    
    *Returns the Unicode hexadecimal values of the string*
    
    This function converts your string to a list of Unicode hexadecimal values:
        >>> sp.unihex("Hello World")
        ['0x48', '0x65', '0x6c', '0x6c', '0x6f', '0x20', '0x57', '0x6f', '0x72', '0x6c', '0x64']
        
.. function:: sp.unioct(String)
    
    *Returns the Unicode octal values of the string*
    
    This function converts your string to a list of Unicode octal values:
        >>> sp.unioct("Hello World")
        ['0o110', '0o145', '0o154', '0o154', '0o157', '0o40', '0o127', '0o157', '0o162', '0o154', '0o144']