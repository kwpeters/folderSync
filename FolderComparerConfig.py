import re


PREFER_NONE         = 0
PREFER_LEFT         = 1
PREFER_RIGHT        = 2


class FolderComparerConfig(object):

    def __init__(self, leftFolder, rightFolder, preferredSide, ignoreRegexes):

        self.__leftFolder = leftFolder
        self.__rightFolder = rightFolder
        self.__preferredSide = preferredSide

        self.__ignoreRegexes = [
            # ._xyzzy files are used in Mac OS X on some filesystems to store metadata about a file
            re.compile(r'^(.*/)*\._.*$', re.IGNORECASE),   # todo: Update "/" for use on Windows
            # .DS_Store files are used on Mac OS X to store custom attributes of a folder
            re.compile(r'^(.*/)*\.DS_Store$', re.IGNORECASE)   # todo: Update "/" for use on Windows
            ]

        self.__ignoreRegexes.extend(ignoreRegexes)


    def GetLeftFolder(self):
        return self.__leftFolder


    def GetRightFolder(self):
        return self.__rightFolder


    def GetPreferredSide(self):
        return self.__preferredSide


    def GetIgnoreRegexes(self):
        return self.__ignoreRegexes

