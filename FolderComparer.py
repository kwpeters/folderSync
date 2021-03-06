#! /usr/bin/python -O
import filecmp
import os.path
import utility
import FilePairing

class FolderComparer(object):

    def __init__(self, config):

        self.__config = config

        dircmp = filecmp.dircmp(config.GetLeftFolder(), config.GetRightFolder(), [], [])
        (self.__sameFiles,
         self.__diffFiles,
         self.__leftOnlyFiles,
         self.__leftOnlyDirs,
         self.__rightOnlyFiles,
         self.__rightOnlyDirs) = self.__analyzeDir(dircmp)


    def __analyzeDir(self, dircmp):

        ignoreRegexes = self.__config.GetIgnoreRegexes()

        sameFiles = dircmp.same_files
        sameFiles = utility.FilterOut(sameFiles, ignoreRegexes)
        sameFiles = [os.path.join(dircmp.left, curFile) for curFile in sameFiles]
        sameFiles = [os.path.relpath(curFile, self.__config.GetLeftFolder()) for curFile in sameFiles]

        diffFiles = dircmp.diff_files
        diffFiles = utility.FilterOut(diffFiles, ignoreRegexes)
        diffFiles = [os.path.join(dircmp.left, curFile) for curFile in diffFiles]
        diffFiles = [os.path.relpath(curFile, self.__config.GetLeftFolder()) for curFile in diffFiles]

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

        leftOnlyFiles = [os.path.relpath(curFile, self.__config.GetLeftFolder()) for curFile in leftOnlyFiles]
        leftOnlyFiles = utility.FilterOut(leftOnlyFiles, ignoreRegexes)
        leftOnlyDirs = [os.path.relpath(curFile, self.__config.GetLeftFolder()) for curFile in leftOnlyDirs]

        for curItem in dircmp.right_only:
            itemName = os.path.join(dircmp.right, curItem)
            if utility.MatchesAny(itemName, ignoreRegexes):
                continue

            if os.path.isfile(itemName):
                rightOnlyFiles.append(itemName)
            else:
                rightOnlyDirs.append(itemName)

        rightOnlyFiles = [os.path.relpath(curFile, self.__config.GetRightFolder()) for curFile in rightOnlyFiles]
        rightOnlyFiles = utility.FilterOut(rightOnlyFiles, ignoreRegexes)
        rightOnlyDirs = [os.path.relpath(curFile, self.__config.GetRightFolder()) for curFile in rightOnlyDirs]


        for subDirCmp in dircmp.subdirs.values():
            subDirResults = self.__analyzeDir(subDirCmp)
            sameFiles.extend(subDirResults[0])
            diffFiles.extend(subDirResults[1])
            leftOnlyFiles.extend(subDirResults[2])
            leftOnlyDirs.extend(subDirResults[3])
            rightOnlyFiles.extend(subDirResults[4])
            rightOnlyDirs.extend(subDirResults[5])

        return (sameFiles, diffFiles, leftOnlyFiles, leftOnlyDirs,
                rightOnlyFiles, rightOnlyDirs)


    def GetSameFiles(self):
        return self.__sameFiles


    def GetDiffFiles(self):
        return self.__diffFiles


    def GetDiffFilePairings(self):
        diffFiles = self.GetDiffFiles()
        diffFiles = [FilePairing.CreateDiffFilePairing(curDiffFile, self.__config) for
            curDiffFile in diffFiles]
        return diffFiles


    def GetLeftOnlyDirs(self):
        return self.__leftOnlyDirs


    def GetLeftOnlyDirPairings(self):
        leftOnlyDirs = self.GetLeftOnlyDirs()
        leftOnlyDirs = [FilePairing.CreateLeftOnlyDirPairing(curDir, self.__config)
                        for curDir in leftOnlyDirs]
        return leftOnlyDirs


    def GetLeftOnlyFiles(self):
        return self.__leftOnlyFiles


    def GetLeftOnlyFilePairings(self):
        leftOnlyFiles = self.GetLeftOnlyFiles()
        leftOnlyFiles = [FilePairing.CreateLeftOnlyFilePairing(curFile, self.__config) for
                         curFile in leftOnlyFiles]
        return leftOnlyFiles


    def GetRightOnlyDirs(self):
        return self.__rightOnlyDirs


    def GetRightOnlyDirPairings(self):
        rightOnlyDirs = self.GetRightOnlyDirs()
        rightOnlyDirs = [FilePairing.CreateRightOnlyDirPairing(curDir, self.__config)
                        for curDir in rightOnlyDirs]
        return rightOnlyDirs


    def GetRightOnlyFiles(self):
        return self.__rightOnlyFiles


    def GetRightOnlyFilePairings(self):
        rightOnlyFiles = self.GetRightOnlyFiles()
        rightOnlyFiles = [FilePairing.CreateRightOnlyFilePairing(curFile, self.__config) for
                         curFile in rightOnlyFiles]
        return rightOnlyFiles
