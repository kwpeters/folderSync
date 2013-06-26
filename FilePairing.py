import collections
import FileActions
import os.path
import FolderComparer
import utility

WARNING_NONE         = 0
WARNING_TAKING_OLDER = 'An older file is being copied over a newer file!'


def CreateDiffFilePairing(relFilePath, leftRoot, rightRoot, preferredSide):

    leftFilePath = os.path.join(leftRoot, relFilePath)
    assert os.path.isfile(leftFilePath)
    rightFilePath = os.path.join(rightRoot, relFilePath)
    assert os.path.isfile(rightFilePath)

    leftModTime = os.path.getmtime(leftFilePath)
    rightModTime = os.path.getmtime(rightFilePath)

    copyLeft = FileActions.FileActionCopyLeft(relFilePath, leftRoot, rightRoot)
    copyRight = FileActions.FileActionCopyRight(relFilePath, leftRoot, rightRoot)
    deleteLeft = FileActions.FileActionDeleteLeft(relFilePath, leftRoot, rightRoot)
    deleteRight = FileActions.FileActionDeleteRight(relFilePath, leftRoot, rightRoot)
    deleteBoth = FileActions.FileActionDeleteBoth(relFilePath, leftRoot, rightRoot)
    skip = FileActions.FileActionSkip(relFilePath, leftRoot, rightRoot)

    # If a preferred side is not set, set it based on which file is newer.
    if not preferredSide:
        if leftModTime > rightModTime:
            preferredSide = FolderComparer.PREFER_LEFT
        else:
            preferredSide = FolderComparer.PREFER_RIGHT

    actions = collections.deque()
    if preferredSide == FolderComparer.PREFER_LEFT:
        actions.append(copyRight)
        actions.append(copyLeft)
    else:
        actions.append(copyLeft)
        actions.append(copyRight)

    actions.append(deleteLeft)
    actions.append(deleteRight)
    actions.append(deleteBoth)
    actions.append(skip)

    pairing = FilePairing(relFilePath, leftRoot, rightRoot, preferredSide, actions)
    return pairing



def CreateLeftOnlyFilePairing(relFilePath, leftRoot, rightRoot):
    pass


def CreateRightOnlyFilePairing(relFilePath, leftRoot, rightRoot):
    pass


class FilePairing(object):

    def __init__(self, relFilePath, leftRoot, rightRoot, preferredSide, actions):
        self.__relFilePath = relFilePath
        self.__leftRoot = leftRoot
        self.__rightRoot = rightRoot
        self.__preferredSide = preferredSide
        self.__actions = actions


    def RotateActionForward(self):
        self.__actions.rotate(-1)


    def RotateActionBackward(self):
        self.__actions.rotate(1)


    def GetWarnings(self):
        currentActionType = self.__actions[0].GetType()

        leftFilePath = os.path.join(self.__leftRoot, self.__relFilePath)
        assert os.path.isfile(leftFilePath)
        rightFilePath = os.path.join(self.__rightRoot, self.__relFilePath)
        assert os.path.isfile(rightFilePath)

        leftModTime = os.path.getmtime(leftFilePath)
        rightModTime = os.path.getmtime(rightFilePath)
        leftIsNewer = leftModTime > rightModTime
        rightIsNewer = not leftIsNewer

        warnings = []
        if ((leftIsNewer and (currentActionType == FileActions.ACTION_COPY_LEFT)) or
            (rightIsNewer and (currentActionType == FileActions.ACTION_COPY_RIGHT))):
            warnings.append(WARNING_TAKING_OLDER)

        return warnings


    def Render(self, width):
        currentActionType = self.__actions[0].GetType()

        leftFilePath = os.path.join(self.__leftRoot, self.__relFilePath)
        assert os.path.isfile(leftFilePath)
        rightFilePath = os.path.join(self.__rightRoot, self.__relFilePath)
        assert os.path.isfile(rightFilePath)

        shortLen = (width - 5)/2

        shortLeft = utility.ShortenPath(leftFilePath, shortLen)
        shortLeft = shortLeft.ljust(shortLen)
        shortRight = utility.ShortenPath(rightFilePath, shortLen)
        shortRight = shortRight.ljust(shortLen)
        return '%s %s %s' % (shortLeft, currentActionType, shortRight)


    def PerformAction(self):
        curAction = self.__actions[0]
        return curAction.PerformAction()
