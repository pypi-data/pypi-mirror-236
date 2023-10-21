'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers the basic operations on strings, such as concatenation and splitting strings.
'''

from sorting import alphasort

def add(*args,spaces=False):
    '''
    Adds strings together, with spaces if you want
    
    >>> sp.add("hello", "world", spaces=True)
    'hello world'
    '''
    
    if spaces==True:
        return " ".join(args)
    else:
        return "".join(args)

def subtract(String,num):
    '''
    Takes away a certain amount of characters from the end of a string
    
    >>> sp.subtract("Hello World", 6)
    'Hello'
    '''
    
    return String[:-num]

def divchunks(String,chunksize):
    '''
    Divides a string into chunks of a specified size. If it cannot divide equally there will just be one chunk smaller than the rest.
    
    >>> sp.divchunks("Hello World", 2)
    ['He', 'll', 'o ', 'Wo', 'rl', 'd']
    '''
    
    chunks = [String[i:i+chunksize] for i in range(0, len(String), chunksize)]
    return chunks
        
def remove(String,removed, spaces=False):
    '''
    Removes a string from a string, with the option of leaving spaces. 
    
    >>> sp.remove("Hello World", " World")
    'Hello'
    '''
    
    if spaces==True:
        spacestring=""
        for i in range(len(removed)):
            spacestring = spacestring + " "
        del i
        return String.replace(removed,spacestring)
    else:
        return String.replace(removed,"")

def join(List,spaces=False):
    '''
    Makes a string from a list, and can add spaces inbetween.
    
    >>> sp.join(["Hello", "World"], spaces = True)
    'Hello World'
    '''
    
    a = str()
    first = True 
    for item in List:
        if first == True:
            a = a + str(item)
            first = False
        elif spaces==True:
            a = a + " " +str(item) 
        elif spaces == False: 
            a = a + str(item) 
    
    return a

def split(String,separator = None, Maxsplit=None):
    '''
    Function to split a string into parts, you can specify the separator (default is a space) and/or maximum number of splits.
    
    >>> sp.split("Hello World")
    ['Hello', 'World']
    '''
    
    if Maxsplit != None:
        b = String.split(separator,maxsplit=Maxsplit)
    else:
        b = String.split(separator)
    return b

# def splitstr(String, separator=None, Maxsplit=None):
#     if Maxsplit != None:
#         b = String.split(separator,maxsplit=Maxsplit)
#     else:
#         b = String.split(separator)
#     return b
    
def splitdex(String, splitpoint):
    '''
    Splits a string at a specific index.
    
    >>> sp.splitdex("Hello World", 4)
    ["Hell", "o World"]
    '''
    
    stringlist = []
    stringlist.append(String[:splitpoint])
    stringlist.append(String[splitpoint:])
    return stringlist

def switch(String, oldstring,newstring):
    '''
    Switches part of a string with a new string.
    
    >>> sp.switch("Hello There", "There", "World")
    'Hello World'
    '''
    
    return String.replace(oldstring,newstring)

def switchchars(String,old,new):
    '''
    Switch all of a type of letter for a different letter
    
    >>> sp.switchchars("Hello World","l","d")
    'Heddo Wordd'
    '''
    
    c = String.replace(old,new)
    return c

def switchdex(String,index,char):
    '''
    Switch the letter at a specific index for another letter.
    
    >>> sp.switchdex("Gello World",1,"H")
    'Hello World'
    '''
    
    d = String[:index-1] + char + String[index:] # index-1 so that the user can count from 1 rather than 0
    return d

def chars(String):
    '''
    Get each character in a list from a string.
    
    >>> sp.chars("Hello World")
    ['H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd']
    '''
    
    return list(String)

def uniques(String):
    '''
    Get each unique character of a string.
    
    >>> sp.uniques("Hello World")
    [' ', 'd', 'e', 'H', 'l', 'o', 'r', 'W']
    '''
    
    return alphasort(list(set(String)))

def mesh(String1, String2):
    '''
    Mesh/interweave two strings.
    
    >>> sp.mesh("Hello", "World")
    'HWeolrllod'
    '''
    
    return ''.join(''.join(item) for item in zip(String1, String2))

def reverse(String):
    '''
    Reverse a string.
    
    >>> sp.reverse("Hello World")
    'dlroW olleH'
    '''
    
    return String[::-1]

def length(String):
    '''
    Get the length of a string.
    
    >>> sp.length("Hello World)
    11
    '''
    
    return len(String)

def count(letter, String):
    '''
    Get the amount of times any letter appears in a string.
    >>> sp.count("l","Hello World")
    3
    '''
    
    # s = String.lower()
    return String.count(letter)