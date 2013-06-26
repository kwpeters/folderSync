#! /usr/bin/python -O
import filecmp
import os.path
import utility
import re
import collections


ignoreRegexes = [
    re.compile(r'^(.*/)*\._.*$', re.IGNORECASE)   # todo: Update "/" for use on Windows
    ]


PREFER_NONE         = 0
PREFER_LEFT         = 1
PREFER_RIGHT        = 2

WARNING_NONE         = 0
WARNING_TAKING_OLDER = 'An older file is being copied over a newer file!'


class DiffPairing(object):

    def __init__(self, relFilePath, leftRoot, rightRoot, preferredSide):
        self.__relFilePath = relFilePath
        self.__leftRoot = leftRoot
        self.__rightRoot = rightRoot
        self.__preferredSide = preferredSide
        self.__leftFilePath = os.path.join(leftRoot, relFilePath)
        self.__rightFilePath = os.path.join(rightRoot, relFilePath)


        leftIsNewer = True;
        if os.path.getmtime(self.__leftFilePath < os.path.getmtime(self.__rightFilePath)):
            leftIsNewer = False
        rightIsNewer = not leftIsNewer   # to make following logic easier

        if (preferredSide == PREFER_LEFT) or ((preferredSide == PREFER_NONE) and leftIsNewer):
            self.__allowedActions = collections.deque([ACTION_COPY_RIGHT, ACTION_COPY_LEFT, ACTION_DELETE_LEFT, ACTION_DELETE_RIGHT, ACTION_SKIP])
        elif (preferredSide == PREFER_RIGHT) or ((preferredSide == PREFER_NONE) and rightIsNewer):
            self.__allowedActions = collections.deque([ACTION_COPY_LEFT, ACTION_COPY_RIGHT, ACTION_DELETE_LEFT, ACTION_DELETE_RIGHT, ACTION_SKIP])



    def GetCurrentAction(self):
        return self.__allowedActions[0]


    def CycleAction(self):
        self.__allowedActions.rotate(-1)


    def GetWarnings(self):
        warnings = []
        curAction = self.GetCurrentAction()

        if (((curAction == ACTION_COPY_RIGHT) and rightIsNewer) or
            ((curAction == ACTION_COPY_LEFT) and leftIsNewer)):
            warnings.append(WARNING_TAKING_OLDER)

        return warnings
    

    def ExecuteAction(self):
        pass


    def Render(self):
        pass

    

        



class FolderComparer(object):
    
    def __init__(self, leftFolder, rightFolder, preferredSide):

        self.__leftRoot = leftFolder
        self.__rightRoot = rightFolder
        self.__preferredSide = preferredSide

        dircmp = filecmp.dircmp(leftFolder, rightFolder, [], [])
        (self.__sameFiles,
         self.__diffFiles,
         self.__leftOnlyFiles,
         self.__rightOnlyFiles,
         self.__leftOnlyDirs,
         self.__rightOnlyDirs) = self.__analyzeDir(dircmp, leftFolder, rightFolder)
        

    def __analyzeDir(self, dircmp, leftRoot, rightRoot):

        sameFiles = dircmp.same_files
        sameFiles = utility.FilterOut(sameFiles, ignoreRegexes)
        sameFiles = [os.path.join(dircmp.left, curFile) for curFile in sameFiles]
        sameFiles = [os.path.relpath(curFile, leftRoot) for curFile in sameFiles]

        diffFiles = dircmp.diff_files
        diffFiles = utility.FilterOut(diffFiles, ignoreRegexes)
        diffFiles = [os.path.join(dircmp.left, curFile) for curFile in diffFiles]
        diffFiles = [os.path.relpath(curFile, leftRoot) for curFile in diffFiles]
        
        leftOnlyFiles = []
        leftOnlyDirs = []
        rightOnlyFiles = []
        rightOnlyDirs = []
        
        for curItem in dircmp.left_only:
            itemName = os.path.join(dircmp.left, curItem)
            if utility.MatchesAny(itemName, ignoreRegexes):
                continue

            if os.path.isfile(itemName):
                leftOnlyFiles.append(itemName)
            else:
                leftOnlyDirs.append(itemName)

        leftOnlyFiles = [os.path.relpath(curFile, leftRoot) for curFile in leftOnlyFiles]
        leftOnlyFiles = utility.FilterOut(leftOnlyFiles, ignoreRegexes)
        leftOnlyDirs = [os.path.relpath(curFile, leftRoot) for curFile in leftOnlyDirs]

        for curItem in dircmp.right_only:
            itemName = os.path.join(dircmp.right, curItem)
            if utility.MatchesAny(itemName, ignoreRegexes):
                continue

            if os.path.isfile(itemName):
                rightOnlyFiles.append(itemName)
            else:
                rightOnlyDirs.append(itemName)

        rightOnlyFiles = [os.path.relpath(curFile, rightRoot) for curFile in rightOnlyFiles]
        rightOnlyFiles = utility.FilterOut(rightOnlyFiles, ignoreRegexes)
        rightOnlyDirs = [os.path.relpath(curFile, rightRoot) for curFile in rightOnlyDirs]

        for subDirCmp in dircmp.subdirs.values():

            subDirResults = self.__analyzeDir(subDirCmp, leftRoot, rightRoot)
            sameFiles.extend(subDirResults[0])
            diffFiles.extend(subDirResults[1])
            leftOnlyFiles.extend(subDirResults[2])
            leftOnlyDirs.extend(subDirResults[3])
            rightOnlyFiles.extend(subDirResults[4])
            rightOnlyDirs.extend(subDirResults[5])

        return (sameFiles, diffFiles, leftOnlyFiles, rightOnlyFiles, leftOnlyDirs, rightOnlyDirs)


    def GetSameFiles(self):
        return self.__sameFiles


    def GetDiffFiles(self):
        return self.__diffFiles


    def GetDiffFilePairings(self):
        diffFiles = self.GetDiffFiles()
        pairings = [DiffPairing(curDiffFile, self.__leftRoot, self.__rightRoot, self.__preferredSide)
                    for curDiffFile in diffFiles]
        return pairings        


    def GetLeftOnlyDirs(self):
        return self.__leftOnlyDirs


    def GetLeftOnlyFiles(self):
        return self.__leftOnlyFiles


    def GetRightOnlyDirs(self):
        return self.__rightOnlyDirs


    def GetRightOnlyFiles(self):
        return self.__rightOnlyFiles
