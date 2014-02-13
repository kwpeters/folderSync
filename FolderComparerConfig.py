import re
import os

PREFER_NONE         = 0
PREFER_LEFT         = 1
PREFER_RIGHT        = 2


if os.sep == '/':
    SEPREGEX = r'/'
else:
    SEPREGEX = r'\\'


DEFAULT_IGNORE_REGEXES = [
    # ._xyzzy files are used in Mac OS X on some filesystems to store metadata about a file
    re.compile(r'^(.*' + SEPREGEX +  r')*\._.*$', re.IGNORECASE),
    # .DS_Store files are used on Mac OS X to store custom attributes of a folder
    re.compile(r'^(.*' + SEPREGEX  + r')*\.DS_Store$', re.IGNORECASE)
    ]

class FolderComparerConfig(object):

    def __init__(self, leftFolder, rightFolder, preferredSide, ignoreRegexes):

        self.__leftFolder = leftFolder
        self.__rightFolder = rightFolder
        self.__preferredSide = preferredSide

        self.__ignoreRegexes = DEFAULT_IGNORE_REGEXES

        self.__ignoreRegexes.extend(ignoreRegexes)


    def GetLeftFolder(self):
        return self.__leftFolder


    def GetRightFolder(self):
        return self.__rightFolder


    def GetPreferredSide(self):
        return self.__preferredSide


    def GetIgnoreRegexes(self):
        return self.__ignoreRegexes

