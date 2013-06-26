import unittest
import NukeFolder
import os
import os.path
import FileActions
import shutil
import utility
import filecmp


UT_FIXTURE = os.path.join('.', 'utFixture')
FIXTURE_DIR_LEFT = os.path.join(UT_FIXTURE, 'left')
FIXTURE_DIR_RIGHT = os.path.join(UT_FIXTURE, 'right')


class FileActionsTests(unittest.TestCase):

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


    def __createLeftOnlyFile(self, relFilePath):
        leftOnlyFile = os.path.join(FIXTURE_DIR_LEFT, relFilePath)
        utility.CreateDirForFile(leftOnlyFile)

        handle = open(leftOnlyFile, 'w')
        handle.write('This is a left-only file.')
        handle.close()


    def __createRightOnlyFile(self, relFilePath):
        rightOnlyFile = os.path.join(FIXTURE_DIR_RIGHT, relFilePath)
        utility.CreateDirForFile(rightOnlyFile)

        handle = open(rightOnlyFile, 'w')
        handle.write('This is a right-only file.')
        handle.close()


    def testCopyLeft(self):
        self.__createRightOnlyFile('filename.txt')

        action = FileActions.FileActionCopyLeft(
            'filename.txt',
            FIXTURE_DIR_LEFT,
            FIXTURE_DIR_RIGHT)

        self.assertEqual(action.GetType(), FileActions.ACTION_COPY_LEFT)
        
        action.PerformAction()
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt'),
                                    os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))


    def testCopyRight(self):
        self.__createLeftOnlyFile('filename.txt')

        action = FileActions.FileActionCopyRight('filename.txt', FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)

        self.assertEqual(action.GetType(), FileActions.ACTION_COPY_RIGHT)
        
        action.PerformAction()
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt'),
                                    os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

    def testDeleteLeft(self):
        self.__createSameFile('filename.txt')
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

        action = FileActions.FileActionDeleteLeft('filename.txt', FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)
        
        self.assertEqual(action.GetType(), FileActions.ACTION_DELETE_LEFT)

        action.PerformAction()
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))


    def testDeleteRight(self):
        self.__createSameFile('filename.txt')
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

        action = FileActions.FileActionDeleteRight('filename.txt', FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)
        
        self.assertEqual(action.GetType(), FileActions.ACTION_DELETE_RIGHT)

        action.PerformAction()
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

    def testDeleteBoth(self):
        self.__createSameFile('filename.txt')
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

        action = FileActions.FileActionDeleteBoth('filename.txt', FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)
        
        self.assertEqual(action.GetType(), FileActions.ACTION_DELETE_BOTH)

        action.PerformAction()
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))


    def testSkip(self):
        self.__createSameFile('filename.txt')
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

        action = FileActions.FileActionSkip('filename.txt', FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT)
        
        self.assertEqual(action.GetType(), FileActions.ACTION_SKIP)

        action.PerformAction()
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))
