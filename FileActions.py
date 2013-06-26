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


class FileActionCopyLeft(object):

    def __init__(self, relFilePath, leftRoot, rightRoot):
        self.__relFilePath = relFilePath
        self.__leftRoot = leftRoot
        self.__rightRoot = rightRoot


    def GetType(self):
        return ACTION_COPY_LEFT


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


    def PerformAction(self):
        pass
