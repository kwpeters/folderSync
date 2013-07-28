import unittest
import NukeFolder
import os
import os.path
import FolderComparerConfig
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
        assert nukeSucceeded


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


    def testFileActionCopyLeft(self):
        self.__createRightOnlyFile('filename.txt')

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionCopyLeft('filename.txt', config)

        self.assertEqual(action.GetType(), FileActions.ACTION_COPY_LEFT)

        action.PerformAction()
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt'),
                                    os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))


    def testFileActionCopyRight(self):
        self.__createLeftOnlyFile('filename.txt')

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionCopyRight('filename.txt', config)

        self.assertEqual(action.GetType(), FileActions.ACTION_COPY_RIGHT)

        action.PerformAction()
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))
        self.assertTrue(filecmp.cmp(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt'),
                                    os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

    def testFileActionDeleteLeft(self):
        self.__createSameFile('filename.txt')
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionDeleteLeft('filename.txt', config)

        self.assertEqual(action.GetType(), FileActions.ACTION_DELETE_LEFT)

        action.PerformAction()
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))


    def testFileActionDeleteRight(self):
        self.__createSameFile('filename.txt')
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionDeleteRight('filename.txt', config)

        self.assertEqual(action.GetType(), FileActions.ACTION_DELETE_RIGHT)

        action.PerformAction()
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

    def testFileActionDeleteBoth(self):
        self.__createSameFile('filename.txt')
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionDeleteBoth('filename.txt', config)

        self.assertEqual(action.GetType(), FileActions.ACTION_DELETE_BOTH)

        action.PerformAction()
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))


    def testFileActionSkip(self):
        self.__createSameFile('filename.txt')
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionSkip('filename.txt', config)

        self.assertEqual(action.GetType(), FileActions.ACTION_SKIP)

        action.PerformAction()
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, 'filename.txt')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, 'filename.txt')))


    def testFileActionCopyTreeLeft(self):
        relFilePath1 = os.path.join('adirectory', 'filename.txt')
        relFilePath2 = os.path.join('adirectory', '.DS_Store')

        self.__createRightOnlyFile(relFilePath1)
        self.__createRightOnlyFile(relFilePath2)
        self.assertTrue(os.path.isdir(os.path.join(FIXTURE_DIR_RIGHT, 'adirectory')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, relFilePath1)))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, relFilePath2)))

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionCopyTreeLeft('adirectory', config)

        self.assertEqual(action.GetType(), FileActions.ACTION_COPY_TREE_LEFT)

        action.PerformAction()

        # File 1 should have been copied, but not file 2.
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, relFilePath1)))
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, relFilePath2)))

        # The original files should still be present.
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, relFilePath1)))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, relFilePath2)))


    def testFileActionCopyTreeRight(self):
        relFilePath1 = os.path.join('adirectory', 'filename.txt')
        relFilePath2 = os.path.join('adirectory', '.DS_Store')

        self.__createLeftOnlyFile(relFilePath1)
        self.__createLeftOnlyFile(relFilePath2)
        self.assertTrue(os.path.isdir(os.path.join(FIXTURE_DIR_LEFT, 'adirectory')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, relFilePath1)))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, relFilePath2)))

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionCopyTreeRight('adirectory', config)

        self.assertEqual(action.GetType(), FileActions.ACTION_COPY_TREE_RIGHT)

        action.PerformAction()

        # File 1 should have been copied, but not file 2.
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, relFilePath1)))
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, relFilePath2)))

        # The original files should still be present.
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, relFilePath1)))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, relFilePath2)))


    def testFileActionDeleteTreeLeft(self):
        relFilePath1 = os.path.join('adirectory', 'filename.txt')

        self.__createLeftOnlyFile(relFilePath1)
        self.assertTrue(os.path.isdir(os.path.join(FIXTURE_DIR_LEFT, 'adirectory')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, relFilePath1)))

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionDeleteTreeLeft('adirectory', config)
        self.assertEqual(action.GetType(), FileActions.ACTION_DELETE_TREE_LEFT)

        action.PerformAction()

        # The file and directory should not exist on the left side.
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, relFilePath1)))
        self.assertFalse(os.path.isdir(os.path.join(FIXTURE_DIR_LEFT, 'adirectory')))

        # The file and directory should not exist on the right side.
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, relFilePath1)))
        self.assertFalse(os.path.isdir(os.path.join(FIXTURE_DIR_RIGHT, 'adirectory')))


    def testFileActionDeleteTreeRight(self):
        relFilePath1 = os.path.join('adirectory', 'filename.txt')

        self.__createRightOnlyFile(relFilePath1)
        self.assertTrue(os.path.isdir(os.path.join(FIXTURE_DIR_RIGHT, 'adirectory')))
        self.assertTrue(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, relFilePath1)))

        config = FolderComparerConfig.FolderComparerConfig(
            FIXTURE_DIR_LEFT, FIXTURE_DIR_RIGHT, FolderComparerConfig.PREFER_NONE, [])

        action = FileActions.FileActionDeleteTreeRight('adirectory', config)
        self.assertEqual(action.GetType(), FileActions.ACTION_DELETE_TREE_RIGHT)

        action.PerformAction()

        # The file and directory should not exist on the left side.
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_LEFT, relFilePath1)))
        self.assertFalse(os.path.isdir(os.path.join(FIXTURE_DIR_LEFT, 'adirectory')))

        # The file and directory should not exist on the right side.
        self.assertFalse(os.path.isfile(os.path.join(FIXTURE_DIR_RIGHT, relFilePath1)))
        self.assertFalse(os.path.isdir(os.path.join(FIXTURE_DIR_RIGHT, 'adirectory')))
