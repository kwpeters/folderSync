r'''This module contains miscellaneous utility methods and classes.
'''
import os
import os.path
import re


def CreateDir(theDir):
    if not os.path.isdir(theDir):
        os.makedirs(theDir)
        

def CreateDirForFile(filePath):
    r'''Helper function that makes sure the directory for the specified file exits.
    '''
    theDir = os.path.dirname(filePath)
    CreateDir(theDir)



def MatchesAny(str, regexes):
    '''Helper function that tests to see if the string str matches any of
    the regular expressions in regexes.'''
    for regex in regexes:
        match = regex.search(str)
        if match:
            return True
    return False


def FilterOut(itemsToFilter, regexesToRemove):
    result = []
    for curItem in itemsToFilter:
        if not MatchesAny(curItem, regexesToRemove):
            result.append(curItem)
    return result


def ConvertToRegexes(origList):
    '''If the given list is a list of strings, the returned list will be a
    list of compiled regular expression objects.  If the provided list
    does not contain strings, the original list is returned.'''
    if type(origList[0]) == str:
        newList = [re.compile(regexstr) for regexstr in origList]
    else:
        newList = origList
    return newList


def ShortenPath(path, numChars):
    '''
    '''
    #
    # If no shortening is necessary, just return the supplied path.
    #
    if len(path) <= numChars:
        return path

    #
    # Divide the supplied path into segments.  Then, put the directory
    # separator back in so we don't have to re-add it later.
    #
    segs = path.split(os.sep)
    segs = [seg + os.sep for seg in segs[:-1]] + [segs[-1]]

    #
    # We will always use the first and last segments.  Save them and remove
    # them from the list.
    #
    firstSeg = segs[0]
    lastSeg = segs[-1]
    segs = segs[1: -1]

    fixedBegin = ('%s...' % firstSeg) + os.sep
    fixedEnd   = lastSeg
    
    charsLeft = numChars - len(fixedBegin) - len(fixedEnd)
    if charsLeft <= 0:
        #
        # The fixed begining and ending have already exhausted the allowable
        # string length, so get out now.
        #
        return fixedBegin + fixedEnd

    additionalSegs = ''
    while True:
        curSeg = segs.pop()
        if len(curSeg) + len(additionalSegs) > charsLeft:
            break
        else:
            additionalSegs = curSeg + additionalSegs

    return fixedBegin + additionalSegs + fixedEnd
        
