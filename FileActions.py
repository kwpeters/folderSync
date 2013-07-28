import os
import os.path
import shutil
import utility


ACTION_COPY_LEFT         = '<--'
ACTION_COPY_RIGHT        = '-->'
ACTION_DELETE_LEFT       = 'x -'
ACTION_DELETE_RIGHT      = '- x'
ACTION_DELETE_BOTH       = 'x x'
ACTION_SKIP              = '- -'
ACTION_COPY_TREE_LEFT    = '<=='
ACTION_COPY_TREE_RIGHT   = '==>'
ACTION_DELETE_TREE_LEFT  = 'X -'
ACTION_DELETE_TREE_RIGHT = '- X'

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

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_COPY_LEFT


    def GetWarnings(self):
        warnings = []
        leftFile = os.path.join(self.__config.GetLeftFolder(), self.__relFilePath)
        if os.path.isfile(leftFile):
            warnings.extend(GetOverwriteWarnings(self.__relFilePath, self.__config.GetRightFolder(), self.__config.GetLeftFolder()))
        return warnings


    def PerformAction(self):
        leftFile = os.path.join(self.__config.GetLeftFolder(), self.__relFilePath)
        rightFile = os.path.join(self.__config.GetRightFolder(), self.__relFilePath)

        # Create the destination directory if it doesn't exist already.
        utility.CreateDirForFile(leftFile)

        shutil.copy2(rightFile, leftFile)



class FileActionCopyRight(object):

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_COPY_RIGHT


    def GetWarnings(self):
        warnings = []
        rightFile = os.path.join(self.__config.GetRightFolder(), self.__relFilePath)
        if os.path.isfile(rightFile):
            warnings.extend(GetOverwriteWarnings(self.__relFilePath, self.__config.GetLeftFolder(), self.__config.GetRightFolder()))
        return warnings


    def PerformAction(self):
        leftFile = os.path.join(self.__config.GetLeftFolder(), self.__relFilePath)
        rightFile = os.path.join(self.__config.GetRightFolder(), self.__relFilePath)

        # Create the destination directory if it doesn't exist already.
        utility.CreateDirForFile(rightFile)

        shutil.copy2(leftFile, rightFile)



class FileActionDeleteLeft(object):

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_DELETE_LEFT


    def GetWarnings(self):
        return []


    def PerformAction(self):
        leftFile = os.path.join(self.__config.GetLeftFolder(), self.__relFilePath)
        os.remove(leftFile)



class FileActionDeleteRight(object):

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_DELETE_RIGHT


    def GetWarnings(self):
        return []


    def PerformAction(self):
        rightFile = os.path.join(self.__config.GetRightFolder(), self.__relFilePath)
        os.remove(rightFile)


class FileActionDeleteBoth(object):

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_DELETE_BOTH


    def GetWarnings(self):
        return []


    def PerformAction(self):
        leftFile = os.path.join(self.__config.GetLeftFolder(), self.__relFilePath)
        os.remove(leftFile)

        rightFile = os.path.join(self.__config.GetRightFolder(), self.__relFilePath)
        os.remove(rightFile)



class FileActionSkip(object):

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_SKIP


    def GetWarnings(self):
        return []


    def PerformAction(self):
        pass


class FileActionCopyTreeLeft(object):

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_COPY_TREE_LEFT


    def GetWarnings(self):
        return []


    def PerformAction(self):
        srcDir = os.path.join(self.__config.GetRightFolder(), self.__relFilePath)
        dstDir = os.path.join(self.__config.GetLeftFolder(), self.__relFilePath)
        shutil.copytree(srcDir, dstDir)


class FileActionCopyTreeRight(object):

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_COPY_TREE_RIGHT


    def GetWarnings(self):
        return []


    def PerformAction(self):
        srcDir = os.path.join(self.__config.GetLeftFolder(), self.__relFilePath)
        dstDir = os.path.join(self.__config.GetRightFolder(), self.__relFilePath)
        shutil.copytree(srcDir, dstDir)


class FileActionDeleteTreeLeft(object):

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_DELETE_TREE_LEFT


    def GetWarnings(self):
        return []


    def PerformAction(self):
        theDir = os.path.join(self.__config.GetLeftFolder(), self.__relFilePath)
        shutil.rmtree(theDir)


class FileActionDeleteTreeRight(object):

    def __init__(self, relFilePath, config):
        self.__relFilePath = relFilePath
        self.__config = config


    def GetType(self):
        return ACTION_DELETE_TREE_RIGHT


    def GetWarnings(self):
        return []


    def PerformAction(self):
        theDir = os.path.join(self.__config.GetRightFolder(), self.__relFilePath)
        shutil.rmtree(theDir)
