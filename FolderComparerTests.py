import unittest
import NukeFolder
import os
import os.path
import FolderComparer
import shutil

UT_FIXTURE = os.path.join('.', 'utFixture')
FIXTURE_DIR_LEFT = os.path.join(UT_FIXTURE, 'left')
FIXTURE_DIR_RIGHT = os.path.join(UT_FIXTURE, 'right')


class FolderComparerTests(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(UT_FIXTURE):
            os.mkdir(UT_FIXTURE)

        if not os.path.isdir(FIXTURE_DIR_LEFT):
            os.mkdir(FIXTURE_DIR_LEFT)

        if not os.path.isdir(FIXTURE_DIR_RIGHT):
            os.mkdir(FIXTURE_DIR_RIGHT)


    def tearDown(self):
        nukeSucceeded = NukeFolder.NukeFolder(UT_FIXTURE)
        assert nukefolder

    def __createDirForFile(self, filePath):
        theDir = os.path.dirname(filePath)
        if not os.path.isdir(theDir):
            os.makedirs(theDir)


    def __createDir(self, theDir):
        if not os.path.isdir(theDir):
            os.makedirs(theDir)
        

    def __createSameFile(self, relFilePath):
        sameFileLeft = os.path.join(FIXTURE_DIR_LEFT, relFilePath)
        self.__createDirForFile(sameFileLeft)
        
        sameFileRight = os.path.join(FIXTURE_DIR_RIGHT, relFilePath)
        self.__createDirForFile(sameFileRight)

        output = open(sameFileLeft, 'w')
        output.write('This is a same file.')
        output.close()

        shutil.copy2(sameFileLeft, sameFileRight)


    def __createDiffFile(self, relFilePath):
        diffFileLeft = os.path.join(FIXTURE_DIR_LEFT, relFilePath)
        self.__createDirForFile(diffFileLeft)

        diffFileRight = os.path.join(FIXTURE_DIR_RIGHT, relFilePath)
        self.__createDirForFile(diffFileRight)

        leftHandle = open(diffFileLeft, 'w')
        leftHandle.write('This is a different file (left side)');
        leftHandle.close()

        rightHandle = open(diffFileRight, 'w')
        rightHandle.write('This is a different file (right side)')
        rightHandle.close()


    def __createLeftOnlyDir(self, relDirPath):
        dirPath = os.path.join(FIXTURE_DIR_LEFT, relDirPath)
        self.__createDir(dirPath)


    def __createLeftOnlyFile(self, relFilePath):
        leftOnlyFile = os.path.join(FIXTURE_DIR_LEFT, relFilePath)
        self.__createDirForFile(leftOnlyFile)

        handle = open(leftOnlyFile, 'w')
        handle.write('This is a left-only file.')
        handle.close()


    def __createRightOnlyDir(self, relDirPath):
        dirPath = os.path.join(FIXTURE_DIR_RIGHT, relDirPath)
        self.__createDir(dirPath)


    def __createRightOnlyFile(self, relFilePath):
        rightOnlyFile = os.path.join(FIXTURE_DIR_RIGHT, relFilePath)
        self.__createDirForFile(rightOnlyFile)

        handle = open(rightOnlyFile, 'w')
        handle.write('This is a right-only file.')
        handle.close()


    def testIsCreatable(self):
        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)
        self.assertTrue(comp)


    def testSameFiles(self):
        self.__createSameFile('samefile.txt')
        
        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)
        self.assertEqual(comp.GetSameFiles(), ['samefile.txt'])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnly(), ([], []))
        self.assertEqual(comp.GetRightOnly(), ([], []))


    def testSameFilesInSubdirs(self):
        self.__createSameFile(os.path.join('subdir', 'samefile.txt'))

        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT);
        self.assertEqual(comp.GetSameFiles(), [os.path.join('subdir', 'samefile.txt')])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnly(), ([], []))
        self.assertEqual(comp.GetRightOnly(), ([], []))


    def testDiffFiles(self):
        self.__createDiffFile('thefile.txt')

        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), ['thefile.txt'])
        self.assertEqual(comp.GetLeftOnly(), ([], []))
        self.assertEqual(comp.GetRightOnly(), ([], []))

        

    def testLeftOnly(self):
        self.__createLeftOnlyDir('leftOnlyDir')
        self.__createLeftOnlyFile('leftOnlyFile.txt')

        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnly(), (['leftOnlyDir'], ['leftOnlyFile.txt']))
        self.assertEqual(comp.GetRightOnly(), ([], []))
        
    
    def testRightOnly(self):
        self.__createRightOnlyDir('rightOnlyDir')
        self.__createRightOnlyFile('rightOnlyFile.txt')

        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnly(), ([], []))
        self.assertEqual(comp.GetRightOnly(), (['rightOnlyDir'], ['rightOnlyFile.txt']))

        
