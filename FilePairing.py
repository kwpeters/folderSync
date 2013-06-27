import collections
import FileActions
import os.path
import FolderComparer
import utility


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
    if preferredSide == FolderComparer.PREFER_NONE:
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



def CreateLeftOnlyFilePairing(relFilePath, leftRoot, rightRoot, preferredSide):
    leftFilePath = os.path.join(leftRoot, relFilePath)
    assert os.path.isfile(leftFilePath)

    copyRight = FileActions.FileActionCopyRight(relFilePath, leftRoot, rightRoot)
    deleteLeft = FileActions.FileActionDeleteLeft(relFilePath, leftRoot, rightRoot)
    skip = FileActions.FileActionSkip(relFilePath, leftRoot, rightRoot)

    if preferredSide == FolderComparer.PREFER_NONE:
        preferredSide = FolderComparer.PREFER_LEFT

    actions = collections.deque()
    if preferredSide == FolderComparer.PREFER_LEFT:
        actions.append(copyRight)
        actions.append(deleteLeft)
    else:
        actions.append(deleteLeft)
        actions.append(copyRight)

    actions.append(skip)

    pairing = FilePairing(relFilePath, leftRoot, rightRoot, preferredSide, actions)
    return pairing


def CreateRightOnlyFilePairing(relFilePath, leftRoot, rightRoot, preferredSide):
    rightFilePath = os.path.join(rightRoot, relFilePath)
    assert os.path.isfile(rightFilePath)

    copyLeft = FileActions.FileActionCopyLeft(relFilePath, leftRoot, rightRoot)
    deleteRight = FileActions.FileActionDeleteRight(relFilePath, leftRoot, rightRoot)
    skip = FileActions.FileActionSkip(relFilePath, leftRoot, rightRoot)

    if preferredSide == FolderComparer.PREFER_NONE:
        preferredSide = FolderComparer.PREFER_RIGHT

    actions = collections.deque()
    if preferredSide == FolderComparer.PREFER_LEFT:
        actions.append(deleteRight)
        actions.append(copyLeft)
    else:
        actions.append(copyLeft)
        actions.append(deleteRight)

    actions.append(skip)

    pairing = FilePairing(relFilePath, leftRoot, rightRoot, preferredSide, actions)
    return pairing




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
        return self.__actions[0].GetWarnings()


    def Render(self, width):
        currentActionType = self.__actions[0].GetType()

        leftFilePath = os.path.join(self.__leftRoot, self.__relFilePath)
        if not os.path.isfile(leftFilePath):
            leftFilePath = ''

        rightFilePath = os.path.join(self.__rightRoot, self.__relFilePath)
        if not os.path.isfile(rightFilePath):
            rightFilePath = ''

        shortLen = (width - 5)/2

        shortLeft = utility.ShortenPath(leftFilePath, shortLen)
        shortLeft = shortLeft.ljust(shortLen)
        shortRight = utility.ShortenPath(rightFilePath, shortLen)
        shortRight = shortRight.ljust(shortLen)
        return '%s %s %s' % (shortLeft, currentActionType, shortRight)


    def PerformAction(self):
        curAction = self.__actions[0]
        return curAction.PerformAction()
