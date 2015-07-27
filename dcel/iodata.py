#! /usr/bin/env python
#Copyright 2008, Angel Yanguas-Gil

#TODO: interface should be a class

"""Extracts/saves numerical data from/to files and lines"""

_commentchars = ['#']
_emptycell = 'NaN'

def commentchar():
    """returns a list with the chars that signal comment lines"""

    return _commentchars

def addcommentchar(c):
    """appends a char to the list of chars that signal comment lines"""
   
    if not c in _commentchars:
        _commentchars.append(c[0])

def setcommentchar(lc):
    """passes a list of comment markers"""
    
    _commentchars = lc

def tokenize(line):
    """determines the tokens inside a line (space or tab
    separated) and returns their numerical values or, if that
    fails, the token as a string"""
    
    lw = []
    if len(line) == 0 or line[0] in _commentchars:
        return lw
    else:
        for word in line.split():
            try:
                val = float(word)
            except:
                val = word
            
            lw.append(val)
        return lw


def filetosheet(filename):
    """Given a file, returns a sheet. A sheet is basically a list
    of data rows"""

    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    plist = []
    for line in lines:
        p = tokenize(line)
        if len(p) == 0:
            continue
        plist.append(p)
    return plist

def extractcolumn(sheet, coln):
    """gets column from sheet"""
    
    col = []
    for row in sheet:
        try:
            v = row[coln-1]
        except:
            v = _emptycell
        col.append(v)
    return col

def operate(col1, col2, func):
    """Just another name for map(f,l1,l2)"""  
    
    return map(func, col1, col2)

def transform(col, func):
    """Just another name for map(f,l)"""
    
    return map(func, col)


