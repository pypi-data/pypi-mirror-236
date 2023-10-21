'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers colouring strings, using the colorama module.
'''

from colorama import Fore, Back, Style, just_fix_windows_console, init, deinit
just_fix_windows_console()

def fcolour(String,f):
    '''
    Change the foreground colour of a string.
    
    >>> sp.fcolour("Hello World", "RED")
    [ 'Hello World' with red text ] 
    '''
    
    if f == "RED":
        return Fore.RED + String + Style.RESET_ALL
    elif f == "BLACK":
        return Fore.BLACK + String + Style.RESET_ALL
    elif f == "GREEN":
        return Fore.GREEN + String + Style.RESET_ALL
    elif f == "YELLOW":
        return Fore.YELLOW + String + Style.RESET_ALL
    elif f == "MAGENTA":
        return Fore.MAGENTA + String + Style.RESET_ALL
    elif f == "CYAN":
        return Fore.CYAN + String + Style.RESET_ALL
    elif f == "WHITE":
        return Fore.WHITE + String + Style.RESET_ALL
    elif f == "BLUE":
        return Fore.BLUE + String + Style.RESET_ALL 
    else:
        return String

def bcolour(String, b):
    '''
    Change the background colour of a string.
    
    >>> sp.bcolour("Hello World", "RED")
    [ 'Hello World' with a red background ]
    '''

    if b == "RED":
        return Back.RED + String + Style.RESET_ALL
    elif b == "BLACK":
        return Back.BLACK + String + Style.RESET_ALL
    elif b == "GREEN":
        return Back.GREEN + String + Style.RESET_ALL
    elif b == "YELLOW":
        return Back.YELLOW + String + Style.RESET_ALL
    elif b == "MAGENTA":
        return Back.MAGENTA + String + Style.RESET_ALL
    elif b == "CYAN":
        return Back.CYAN + String + Style.RESET_ALL
    elif b == "WHITE":
        return Back.WHITE + String + Style.RESET_ALL
    elif b == "BLUE":
        return Back.BLUE + String + Style.RESET_ALL
    return String
    
def style(String,s):
    '''
    Change the style (dim, bright, normal) of a string.
    
    >>> sp.style("Hello World", "BRIGHT")
    [ 'Hello World' in bright text ]
    '''
    
    if s == "DIM":
        return Style.DIM + String + Style.RESET_ALL
    elif s == "NORMAL":
        return Style.NORMAL + String + Style.RESET_ALL
    elif s == "BRIGHT":
        return Style.BRIGHT + String + Style.RESET_ALL
    return String