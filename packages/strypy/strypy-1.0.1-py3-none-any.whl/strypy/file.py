'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers operations with strings and files.
'''
    
def read(file):
    '''
    Simply reads the text of a file and returns it in a string.
    
    >>> sp.read("/path/to/file.txt")
    "File contents"
    '''
    
    with open(file,"r") as f:
        content = f.read()
    f.close()
    return content

def getstrings(file,separator=" "):
    '''
    Get a list of strings from a text file, with the default separator being a space.
    
    >>> sp.getstrings("/path/to/file.txt")
    ["File", "contents"]
    '''
    
    with open(file,"r") as f:
        strings = []
        for line in f:
            for word in line.split(separator):
                strings.append(word)
    f.close  
    return strings

def getchars(file):
    '''
    Get a list of chracters from a text file.
    
    >>> sp.getchars("/path/to/file.txt")
    ["F","i","l","e"," ","c","o","n","t","e","n","t","s"]
    '''
    
    Chars = []
    with open(file,"r") as f:
        while True:
            char = f.read(1)
            if not char:
                break
            Chars.append(char)
            
    f.close()
    return Chars