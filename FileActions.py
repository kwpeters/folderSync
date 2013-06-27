import os
import os.path
import shutil
import utility


ACTION_COPY_LEFT    = '<--'
ACTION_COPY_RIGHT   = '-->'
ACTION_DELETE_LEFT  = 'X -'
ACTION_DELETE_RIGHT = '- X'
ACTION_DELETE_BOTH  = 'X X'
ACTION_SKIP         = '- -'

WARNING_TAKING_OLDER = 'An older file is being copied over a newer file!'


def GetOverwriteWarnings(relPath, srcRoot, destRoot):
    srcFilePath = os.path.join(srcRoot, relPath)
    assert os.path.isfile(srcFilePath)
    destFilePath = os.path.join(destRoot, relPath)
    assert os.path.isfile(destFilePath)

    srcModTime = os.path.getmtime(srcFilePath)
    destModTime = os.path.getmtime(destFilePath)
    destIsNewer = destModTime > srcModTime

    warnings = []
    if destIsNewer:
        warnings.append(WARNING_TAKING_OLDER)

    return warnings




class FileActionCopyLeft(object):

    def __init__(self, relFilePath, leftRoot, rightRoot):
        self.__relFilePath = relFilePath
        self.__leftRoot = leftRoot
        self.__rightRoot = rightRoot


    def GetType(self):
        return ACTION_COPY_LEFT


    def GetWarnings(self):
        warnings = []
        leftFile = os.path.join(self.__leftRoot, self.__relFilePath)
        if os.path.isfile(leftFile):
            warnings.extend(GetOverwriteWarnings(self.__relFilePath, self.__rightRoot, self.__leftRoot))
        return warnings


    def PerformAction(self):
        leftFile = os.path.join(self.__leftRoot, self.__relFilePath)
        rightFile = os.path.join(self.__rightRoot, self.__relFilePath)

        # Create the destination directory if it doesn't exist already.
        utility.CreateDirForFile(leftFile)

        shutil.copy2(rightFile, leftFile)



class FileActionCopyRight(object):

    def __init__(self, relFilePath, leftRoot, rightRoot):
        self.__relFilePath = relFilePath
        self.__leftRoot = leftRoot
        self.__rightRoot = rightRoot


    def GetType(self):
        return ACTION_COPY_RIGHT


    def GetWarnings(self):
        warnings = []
        rightFile = os.path.join(self.__rightRoot, self.__relFilePath)
        if os.path.isfile(rightFile):
            warnings.extend(GetOverwriteWarnings(self.__relFilePath, self.__leftRoot, self.__rightRoot))
        return warnings


    def PerformAction(self):
        leftFile = os.path.join(self.__leftRoot, self.__relFilePath)
        rightFile = os.path.join(self.__rightRoot, self.__relFilePath)

        # Create the destination directory if it doesn't exist already.
        utility.CreateDirForFile(rightFile)

        shutil.copy2(leftFile, rightFile)



class FileActionDeleteLeft(object):

    def __init__(self, relFilePath, leftRoot, rightRoot):
        self.__relFilePath = relFilePath
        self.__leftRoot = leftRoot
        self.__rightRoot = rightRoot


    def GetType(self):
        return ACTION_DELETE_LEFT


    def GetWarnings(self):
        return []


    def PerformAction(self):
        leftFile = os.path.join(self.__leftRoot, self.__relFilePath)
        os.remove(leftFile)



class FileActionDeleteRight(object):

    def __init__(self, relFilePath, leftRoot, rightRoot):
        self.__relFilePath = relFilePath
        self.__leftRoot = leftRoot
        self.__rightRoot = rightRoot


    def GetType(self):
        return ACTION_DELETE_RIGHT


    def GetWarnings(self):
        return []


    def PerformAction(self):
        rightFile = os.path.join(self.__rightRoot, self.__relFilePath)
        os.remove(rightFile)


class FileActionDeleteBoth(object):

    def __init__(self, relFilePath, leftRoot, rightRoot):
        self.__relFilePath = relFilePath
        self.__leftRoot = leftRoot
        self.__rightRoot = rightRoot


    def GetType(self):
        return ACTION_DELETE_BOTH


    def GetWarnings(self):
        return []


    def PerformAction(self):
        leftFile = os.path.join(self.__leftRoot, self.__relFilePath)
        os.remove(leftFile)

        rightFile = os.path.join(self.__rightRoot, self.__relFilePath)
        os.remove(rightFile)



class FileActionSkip(object):

    def __init__(self, relFilePath, leftRoot, rightRoot):
        self.__relFilePath = relFilePath
        self.__leftRoot = leftRoot
        self.__rightRoot = rightRoot


    def GetType(self):
        return ACTION_SKIP


    def GetWarnings(self):
        return []


    def PerformAction(self):
        pass
