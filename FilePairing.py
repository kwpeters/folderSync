import collections
import FileActions
import os.path
import FolderComparerConfig
import utility


def CreateDiffFilePairing(relFilePath, config):

    leftFilePath = os.path.join(config.GetLeftFolder(), relFilePath)
    assert os.path.isfile(leftFilePath)
    rightFilePath = os.path.join(config.GetRightFolder(), relFilePath)
    assert os.path.isfile(rightFilePath)

    leftModTime = os.path.getmtime(leftFilePath)
    rightModTime = os.path.getmtime(rightFilePath)

    copyLeft = FileActions.FileActionCopyLeft(relFilePath, config)
    copyRight = FileActions.FileActionCopyRight(relFilePath, config)
    deleteLeft = FileActions.FileActionDeleteLeft(relFilePath, config)
    deleteRight = FileActions.FileActionDeleteRight(relFilePath, config)
    deleteBoth = FileActions.FileActionDeleteBoth(relFilePath, config)
    skip = FileActions.FileActionSkip(relFilePath, config)

    # If a preferred side is not set, set it based on which file is newer.
    preferredSide = config.GetPreferredSide()
    if preferredSide == FolderComparerConfig.PREFER_NONE:
        if leftModTime > rightModTime:
            preferredSide = FolderComparerConfig.PREFER_LEFT
        else:
            preferredSide = FolderComparerConfig.PREFER_RIGHT

    actions = collections.deque()
    if preferredSide == FolderComparerConfig.PREFER_LEFT:
        actions.append(copyRight)
        actions.append(copyLeft)
    else:
        actions.append(copyLeft)
        actions.append(copyRight)

    actions.append(deleteLeft)
    actions.append(deleteRight)
    actions.append(deleteBoth)
    actions.append(skip)

    pairing = FilePairing(relFilePath, config, actions)
    return pairing



def CreateLeftOnlyFilePairing(relFilePath, config):
    leftFilePath = os.path.join(config.GetLeftFolder(), relFilePath)
    assert os.path.isfile(leftFilePath)

    copyRight = FileActions.FileActionCopyRight(relFilePath, config)
    deleteLeft = FileActions.FileActionDeleteLeft(relFilePath, config)
    skip = FileActions.FileActionSkip(relFilePath, config)

    preferredSide = config.GetPreferredSide()
    if preferredSide == FolderComparerConfig.PREFER_NONE:
        preferredSide = FolderComparerConfig.PREFER_LEFT

    actions = collections.deque()
    if preferredSide == FolderComparerConfig.PREFER_LEFT:
        actions.append(copyRight)
        actions.append(deleteLeft)
    else:
        actions.append(deleteLeft)
        actions.append(copyRight)

    actions.append(skip)

    pairing = FilePairing(relFilePath, config, actions)
    return pairing


def CreateRightOnlyFilePairing(relFilePath, config):
    rightFilePath = os.path.join(config.GetRightFolder(), relFilePath)
    assert os.path.isfile(rightFilePath)

    copyLeft = FileActions.FileActionCopyLeft(relFilePath, config)
    deleteRight = FileActions.FileActionDeleteRight(relFilePath, config)
    skip = FileActions.FileActionSkip(relFilePath, config)

    preferredSide = config.GetPreferredSide()
    if preferredSide == FolderComparerConfig.PREFER_NONE:
        preferredSide = FolderComparerConfig.PREFER_RIGHT

    actions = collections.deque()
    if preferredSide == FolderComparerConfig.PREFER_LEFT:
        actions.append(deleteRight)
        actions.append(copyLeft)
    else:
        actions.append(copyLeft)
        actions.append(deleteRight)

    actions.append(skip)

    pairing = FilePairing(relFilePath, config, actions)
    return pairing


def CreateLeftOnlyDirPairing(relFilePath, config):
    theDir = os.path.join(config.GetLeftFolder(), relFilePath)
    assert os.path.isdir(theDir), theDir + ' is not a directory!'

    copyTreeRight = FileActions.FileActionCopyTreeRight(relFilePath, config)
    deleteTreeLeft = FileActions.FileActionDeleteTreeLeft(relFilePath, config)
    skip = FileActions.FileActionSkip(relFilePath, config)

    preferredSide = config.GetPreferredSide()
    if preferredSide == FolderComparerConfig.PREFER_NONE:
        preferredSide = FolderComparerConfig.PREFER_LEFT

    actions = collections.deque()
    if preferredSide == FolderComparerConfig.PREFER_LEFT:
        actions.append(copyTreeRight)
        actions.append(deleteTreeLeft)
    else:
        actions.append(deleteTreeLeft)
        actions.append(copyTreeRight)

    actions.append(skip)

    pairing = FilePairing(relFilePath, config, actions)
    return pairing


def CreateRightOnlyDirPairing(relFilePath, config):
    theDir = os.path.join(config.GetRightFolder(), relFilePath)
    assert os.path.isdir(theDir)

    copyTreeLeft = FileActions.FileActionCopyTreeLeft(relFilePath, config)
    deleteTreeRight = FileActions.FileActionDeleteTreeRight(relFilePath, config)
    skip = FileActions.FileActionSkip(relFilePath, config)

    preferredSide = config.GetPreferredSide()
    if preferredSide == FolderComparerConfig.PREFER_NONE:
        preferredSide = FolderComparerConfig.PREFER_RIGHT

    actions = collections.deque()
    if preferredSide == FolderComparerConfig.PREFER_LEFT:
        actions.append(deleteTreeRight)
        actions.append(copyTreeLeft)
    else:
        actions.append(copyTreeLeft)
        actions.append(deleteTreeRight)

    actions.append(skip)

    pairing = FilePairing(relFilePath, config, actions)
    return pairing




class FilePairing(object):

    def __init__(self, relFilePath, config, actions):
        self.__relFilePath = relFilePath
        self.__config = config
        self.__actions = actions


    def RotateActionForward(self):
        self.__actions.rotate(-1)


    def RotateActionBackward(self):
        self.__actions.rotate(1)


    def GetWarnings(self):
        return self.__actions[0].GetWarnings()


    def Render(self, width):
        currentActionType = self.__actions[0].GetType()

        leftFilePath = os.path.join(self.__config.GetLeftFolder(), self.__relFilePath)
        if not os.path.isfile(leftFilePath) and not os.path.isdir(leftFilePath):
            leftFilePath = ''

        rightFilePath = os.path.join(self.__config.GetRightFolder(), self.__relFilePath)
        if not os.path.isfile(rightFilePath) and not os.path.isdir(rightFilePath):
            rightFilePath = ''

        assert not ((leftFilePath == '') and (rightFilePath == '')), '%s is not in left or right!' % self.__relFilePath

        shortLen = (width - 5)/2

        shortLeft = utility.ShortenPath(leftFilePath, shortLen)
        shortLeft = shortLeft.ljust(shortLen)
        shortRight = utility.ShortenPath(rightFilePath, shortLen)
        shortRight = shortRight.ljust(shortLen)
        return '%s %s %s' % (shortLeft, currentActionType, shortRight)


    def PerformAction(self):
        curAction = self.__actions[0]
        return curAction.PerformAction()
