'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers generating and converting strings.

Usage:

    >>> import StryPy as sp
    >>> sp.randstr()
    "Uq?nB~\2ng!6%[z+:4s_`F>%h" # Or similar
    
    >>> sp.numcode("Hello World")
    [8, 5, 12, 12, 15, 0, 23, 15, 18, 12, 4]
    
    >>> sp.asciidec("Hello World")
    [72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100]
'''

import random as rd
import string
import secrets

def randstr(minlength= 1,maxlength = 50,lower= True,upper= True,digit = True,special = True,character_string= None):
    '''
    Generates a random string, with advanced parameters.
    
    >>> sp.randstr()
    '+T-MY||e_8Dt(Gc?,H%D3*uIejx<i3}4' # Similar to this
    
    Parameters:
        minlength - defines the minimum length of the string (integer, default = 1)
        maxlength - defines the maximum length of the string (integer, default = 50)
        lower - Include lowercase characters (boolean, default = True)
        upper - Include uppercase characters (boolean, default = True)
        digit - Include digits (boolean, default = True)
        special - Include special characters (boolean, default = True)
        character_string - Only use characters specified by the user (string, default = None)
    '''
    
    length = rd.randint(minlength,maxlength)
    if not (length and isinstance(length, int) and length > 0):
        raise ValueError("length must be an integer greater than zero")
    chars = ""
    if lower:
        chars = chars + string.ascii_lowercase
    if upper:
        chars = chars + string.ascii_uppercase
    if digit:
        chars = chars + string.digits
    if special:
        chars = chars + string.punctuation
    if character_string and isinstance(character_string, str):
        # if character_string is provided ignore upper/lower/digit/special parameters
        chars = character_string
    if not chars:
        raise ValueError("Empty character list to choose from")
    return "".join(secrets.choice(chars) for i in range(length))

def numcode(String):
    '''
    Convert a string to numbers alphabetically - E.G. a = 1, z = 26, A = 27, Z = 52
    
    >>> sp.numcode("hello world")
    [8, 5, 12, 12, 15, 0, 23, 15, 18, 12, 4]
    '''
    
    achars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    aletters=list(achars)
    nums=[str(i) for i in range(1,53)]
    orddict=dict(zip(aletters,nums))
    data=String
    output=[]
    for i in range(len(data)):
        if data[i] in aletters:
            output.append(int(orddict[data[i]]))
        elif data[i]==' ':
            output.append(0)
        else:
            output.append(int(data[i]))
    return output

def unidec(String, reverse=False):
    '''
    Gets the Unicode Decimal value of each character in a string.
    
    >>> sp.unidec("Hello World")
    [72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100]
    '''
    
    data=String
    output=[]
    for i in range(len(data)):
        output.append(ord(data[i]))
    return output

def unihex(String):
    '''
    Gets the Unicode Hexadecimal value of each character in a string.
    
    >>> sp.unihex("Hello World")
    ['0x48', '0x65', '0x6c', '0x6c', '0x6f', '0x20', '0x57', '0x6f', '0x72', '0x6c', '0x64']
    '''
    
    data=String
    output=[]
    for i in range(len(data)):
        output.append(hex(ord(data[i])))
    return output

def unioct(String):
    '''
    Gets the Unicode Octal value of each character in a string.
    
    >>> sp.unioct("Hello World")
    ['0o110', '0o145', '0o154', '0o154', '0o157', '0o40', '0o127', '0o157', '0o162', '0o154', '0o144']
    '''
    
    data=String
    output=[]
    for i in range(len(data)):
        output.append(oct(ord(data[i])))
    return output