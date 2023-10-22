'''
=========================================
StryPy - String Python
Made to help developers work with strings
Published by TomTheCodingGuy
MIT License
=========================================

This file covers the testing of basics.py
'''

import strypy as sp

def test_add():
    assert sp.add("a","b") == "ab", "sp.add('a','b') should return 'ab'"

def test_subtract():
    assert sp.subtract("abc",1) == "ab", "sp.subtract('abc',1) should return 'ab'"

def test_remove():
    assert sp.remove("abc","c") == "ab", "sp.remove('abc','c') should return 'ab'"

def test_divchunks():
    assert sp.divchunks("abc",1) == ["a","b","c"], "sp.divchunks('abc',1) should return ['a','b','c']"

def test_join():
    assert sp.join(["ab","c"]) == "abc", "sp.join(['ab','c']) should return 'abc'"

def test_split():
    assert sp.split("ab cd") == ["ab","cd"], "sp.split('ab cd') should return ['ab','cd']"
    
def test_splitdex():
    assert sp.splitdex("abc",2) == ["ab","c"], "sp.splitdex('abc',2) should return ['ab','c']"

def test_switch():
    assert sp.switch("ayz","yz","bc") == "abc", "sp.switch('ayz','yz','bc') should return 'abc'"

def test_switchchars():
    assert sp.switchchars('abd','d','c') == 'abc', "sp.switchchars('abd','d','c') should return 'abc'"

def test_switchdex():
    assert sp.switchdex('abd',3,'c') == 'abc', "sp.switchdex('abd',3,'c') should return 'abc'"

def test_chars():
    assert sp.chars("abc") == ["a","b","c"], "sp.chars('abc'), should return ['a','b','c']"

def test_uniques():
    assert sp.uniques('aabbcc') == ['a','b','c'], "sp.uniques('aabbcc') should return ['a','b','c']"

def test_mesh():
    assert sp.mesh('ac','bd') == 'abcd', "sp.mesh('ac','bd') should return 'abcd'"

def test_reverse():
    assert sp.reverse('cba') == 'abc', "sp.reverse('cba') should return 'abc'"

def test_length():
    assert sp.length('abc') == 3, "sp.length('abc') should return 3"

def test_count():
    assert sp.count('a', 'abc') == 1, "sp.count('a', 'abc') should return 1"