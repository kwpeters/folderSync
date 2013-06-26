import unittest
import NukeFolder
import os
import os.path
import FolderComparer
import shutil
import utility

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


    def __createSameFile(self, relFilePath):
        sameFileLeft = os.path.join(FIXTURE_DIR_LEFT, relFilePath)
        utility.CreateDirForFile(sameFileLeft)
        
        sameFileRight = os.path.join(FIXTURE_DIR_RIGHT, relFilePath)
        utility.CreateDirForFile(sameFileRight)

        output = open(sameFileLeft, 'w')
        output.write('This is a same file.')
        output.close()

        shutil.copy2(sameFileLeft, sameFileRight)


    def __createDiffFile(self, relFilePath):
        diffFileLeft = os.path.join(FIXTURE_DIR_LEFT, relFilePath)
        utility.CreateDirForFile(diffFileLeft)

        diffFileRight = os.path.join(FIXTURE_DIR_RIGHT, relFilePath)
        utility.CreateDirForFile(diffFileRight)

        leftHandle = open(diffFileLeft, 'w')
        leftHandle.write('This is a different file (left side)');
        leftHandle.close()

        rightHandle = open(diffFileRight, 'w')
        rightHandle.write('This is a different file (right side)')
        rightHandle.close()


    def __createLeftOnlyDir(self, relDirPath):
        dirPath = os.path.join(FIXTURE_DIR_LEFT, relDirPath)
        utility.CreateDir(dirPath)


    def __createLeftOnlyFile(self, relFilePath):
        leftOnlyFile = os.path.join(FIXTURE_DIR_LEFT, relFilePath)
        utility.CreateDirForFile(leftOnlyFile)

        handle = open(leftOnlyFile, 'w')
        handle.write('This is a left-only file.')
        handle.close()


    def __createRightOnlyDir(self, relDirPath):
        dirPath = os.path.join(FIXTURE_DIR_RIGHT, relDirPath)
        utility.CreateDir(dirPath)


    def __createRightOnlyFile(self, relFilePath):
        rightOnlyFile = os.path.join(FIXTURE_DIR_RIGHT, relFilePath)
        utility.CreateDirForFile(rightOnlyFile)

        handle = open(rightOnlyFile, 'w')
        handle.write('This is a right-only file.')
        handle.close()


    def testIsCreatable(self):
        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE)
        self.assertTrue(comp)


    def testSameFiles(self):
        self.__createSameFile('samefile.txt')
        
        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE)
        self.assertEqual(comp.GetSameFiles(), ['samefile.txt'])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnlyDirs(), [])
        self.assertEqual(comp.GetLeftOnlyFiles(), [])
        self.assertEqual(comp.GetRightOnlyDirs(), [])
        self.assertEqual(comp.GetRightOnlyFiles(), [])


    def testSameFilesInSubdirs(self):
        self.__createSameFile(os.path.join('subdir', 'samefile.txt'))

        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE);
        self.assertEqual(comp.GetSameFiles(), [os.path.join('subdir', 'samefile.txt')])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnlyDirs(), [])
        self.assertEqual(comp.GetLeftOnlyFiles(), [])
        self.assertEqual(comp.GetRightOnlyDirs(), [])
        self.assertEqual(comp.GetRightOnlyFiles(), [])


    def testDiffFiles(self):
        self.__createDiffFile('thefile.txt')

        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), ['thefile.txt'])
        self.assertEqual(comp.GetLeftOnlyDirs(), [])
        self.assertEqual(comp.GetLeftOnlyFiles(), [])
        self.assertEqual(comp.GetRightOnlyDirs(), [])
        self.assertEqual(comp.GetRightOnlyFiles(), [])

        

    def testLeftOnly(self):
        self.__createLeftOnlyDir('leftOnlyDir')
        self.__createLeftOnlyFile('leftOnlyFile.txt')

        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnlyDirs(), ['leftOnlyDir'])
        self.assertEqual(comp.GetLeftOnlyFiles(), ['leftOnlyFile.txt'])
        self.assertEqual(comp.GetRightOnlyDirs(), [])
        self.assertEqual(comp.GetRightOnlyFiles(), [])
        
    
    def testRightOnly(self):
        self.__createRightOnlyDir('rightOnlyDir')
        self.__createRightOnlyFile('rightOnlyFile.txt')

        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnlyDirs(), [])
        self.assertEqual(comp.GetLeftOnlyFiles(), [])
        self.assertEqual(comp.GetRightOnlyDirs(), ['rightOnlyDir'])
        self.assertEqual(comp.GetRightOnlyFiles(), ['rightOnlyFile.txt'])


    def testMacMetadataFilesAreIgnoredSame(self):
        r'''Same files beginning with "._" should not appear in the same files list.
        '''
        self.__createSameFile('._samefile.txt')
        self.__createSameFile(os.path.join('folder', '._anothersamefile.txt'))
        
        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnlyDirs(), [])
        self.assertEqual(comp.GetLeftOnlyFiles(), [])
        self.assertEqual(comp.GetRightOnlyDirs(), [])
        self.assertEqual(comp.GetRightOnlyFiles(), [])


    def testMacMetadataFilesAreIgnoredDiff(self):
        r'''Different files starting with "._" should not appear in the different files list.
        '''
        self.__createDiffFile('._difffile.txt')
        self.__createDiffFile(os.path.join('folder', '._anotherdifffile.txt'))
        
        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnlyDirs(), [])
        self.assertEqual(comp.GetLeftOnlyFiles(), [])
        self.assertEqual(comp.GetRightOnlyDirs(), [])
        self.assertEqual(comp.GetRightOnlyFiles(), [])


    def testMacMetadataFilesAreIgnoredLeftOnly(self):
        r'''Left-only files starting with "._" should not appear in the left-only files list.
        '''
        self.__createLeftOnlyFile('._leftfile.txt')
        self.__createLeftOnlyFile(os.path.join('folder', '._anotherleftfile.txt'))
        
        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnlyDirs(), ['folder'])
        self.assertEqual(comp.GetLeftOnlyFiles(), [])
        self.assertEqual(comp.GetRightOnlyDirs(), [])
        self.assertEqual(comp.GetRightOnlyFiles(), [])


    def testMacMetadataFilesAreIgnoredRightOnly(self):
        r'''Right-only files starting with "._" should not appear in the right-only files list.
        '''
        self.__createRightOnlyFile('._rightfile.txt')
        self.__createRightOnlyFile(os.path.join('folder', '._anotherrightfile.txt'))
        
        comp = FolderComparer.FolderComparer(FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparer.PREFER_NONE)
        self.assertEqual(comp.GetSameFiles(), [])
        self.assertEqual(comp.GetDiffFiles(), [])
        self.assertEqual(comp.GetLeftOnlyDirs(), [])
        self.assertEqual(comp.GetLeftOnlyFiles(), [])
        self.assertEqual(comp.GetRightOnlyDirs(), ['folder'])
        self.assertEqual(comp.GetRightOnlyFiles(), [])


    
