r'''This module contains miscellaneous utility methods and classes.
'''
import os
import os.path
import re
from collections import deque
import shutil


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
        if MatchesAny(curItem, regexesToRemove):
            pass
        else:
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
    # If no shortening is necessary, just return the supplied path.
    if len(path) <= numChars:
        return path

    YADA = '...' + os.sep

    # Divide the supplied path into segments.  Then, put the directory
    # separator back in so we don't have to re-add it later.
    segs = path.split(os.sep)
    segs = [seg + os.sep for seg in segs[:-1]] + [segs[-1]]
    segs = deque(segs)

    # We will always use the first and last segments.  Save them and remove
    # them from the deque
    beg = segs.popleft()
    # If the first segment was just a directory separator (i.e. it was
    # an absolute path), then add one more segment to the beginning.
    if beg == os.sep:
        beg += segs.popleft()

    end = segs.pop()

    canInsertMore = True
    while canInsertMore:
        addedToBeg = False
        addedToEnd = False

        proposed = beg + segs[0] + YADA + end
        if len(proposed) < numChars:
            beg += segs.popleft()
            addedToBeg = True

        proposed = beg + YADA + segs[-1] + end
        if len(proposed) < numChars:
            end = segs.pop() + end
            addedToEnd = True

        if not addedToBeg and not addedToEnd:
            canInsertMore = False

    return beg + YADA + end


def CopyDir(srcDir, dstDir, ignoreRegexes):
    r'''Helper function that copies files from srcDir to dstDir while
    ignoring files that match any pattern found in ignoreRegexes.
    '''
    srcDstPairings = []

    for (dirPath, subdirs, files) in  os.walk(srcDir):

        curDirPath = dirPath
        if not MatchesAny(curDirPath, ignoreRegexes):
            assert curDirPath.startswith(srcDir)
            relativePart = curDirPath[len(srcDir):]

            # If the relative part starts with a "/" then get rid
            # of it.  It will cause the following os.path.join()
            # to discard everything in front of it.
            if relativePart.startswith(os.sep):
                relativePart = relativePart[1:]

            dstFolder = os.path.join(dstDir, relativePart)
            srcDstPairings.append((curDirPath, dstFolder))

        for curFile in files:
            curFilePath = os.path.join(dirPath, curFile)

            if not MatchesAny(curFilePath, ignoreRegexes):
                assert curFilePath.startswith(srcDir)
                relativePart = curFilePath[len(srcDir):]

                # If the relative part starts with a "/" then get rid
                # of it.  It will cause the following os.path.join()
                # to discard everything in front of it.
                if relativePart.startswith(os.sep):
                    relativePart = relativePart[1:]

                dstFile = os.path.join(dstDir, relativePart)
                srcDstPairings.append((curFilePath, dstFile))

    for (src, dst) in srcDstPairings:

        if os.path.isdir(src):
            # The current item is a directory.  Just create the
            # destination directory.
            CreateDir(dst)

        else:
            # Do the copying.
            CreateDirForFile(dst)
            shutil.copy2(src, dst)
