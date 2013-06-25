#! /usr/bin/python -O
import filecmp
import os.path
import utility
import re

ignoreRegexes = [
    re.compile(r'.*/\._.*$', re.IGNORECASE)
    ]


class FolderComparer(object):
    
    def __init__(self, leftFolder, rightFolder):

        self.__leftRoot = leftFolder
        self.__rightRoot = rightFolder

        dircmp = filecmp.dircmp(leftFolder, rightFolder, [], [])
        (self.__sameFiles,
         self.__diffFiles,
         self.__leftOnlyFiles,
         self.__rightOnlyFiles,
         self.__leftOnlyDirs,
         self.__rightOnlyDirs) = self.__analyzeDir(dircmp, leftFolder, rightFolder)
        

    def __analyzeDir(self, dircmp, leftRoot, rightRoot):

        sameFiles = [os.path.join(dircmp.left, curFile) for curFile in dircmp.same_files]
        sameFiles = [os.path.relpath(curFile, leftRoot) for curFile in sameFiles]

        diffFiles = [os.path.join(dircmp.left, curFile) for curFile in dircmp.diff_files]
        diffFiles = [os.path.relpath(curFile, leftRoot) for curFile in diffFiles]
        
        leftOnlyFiles = []
        leftOnlyDirs = []
        rightOnlyFiles = []
        rightOnlyDirs = []
        
        for curItem in dircmp.left_only:
            if os.path.isfile(os.path.join(dircmp.left, curItem)):
                leftOnlyFiles.append(os.path.join(dircmp.left, curItem))
            else:
                leftOnlyDirs.append(os.path.join(dircmp.left, curItem))

        for curItem in dircmp.right_only:
            if os.path.isfile(os.path.join(dircmp.right, curItem)):
                rightOnlyFiles.append(os.path.join(dircmp.right, curItem))
            else:
                rightOnlyDirs.append(os.path.join(dircmp.right, curItem))

        leftOnlyFiles = [os.path.relpath(curFile, leftRoot) for curFile in leftOnlyFiles]
        leftOnlyFiles = utility.FilterOut(leftOnlyFiles, ignoreRegexes)
        leftOnlyDirs = [os.path.relpath(curFile, leftRoot) for curFile in leftOnlyDirs]

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


    def GetLeftOnly(self):
        return (self.__leftOnlyDirs, self.__leftOnlyFiles)


    def GetRightOnly(self):
        return (self.__rightOnlyDirs, self.__rightOnlyFiles)
