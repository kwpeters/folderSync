import unittest
import FolderComparerConfig

class FolderComparerConfigTests(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testIsCreatable(self):
        config = FolderComparerConfig.FolderComparerConfig(
            'leftFolder', 'rightFolder', FolderComparerConfig.PREFER_NONE, [])
        self.assertIsNotNone(config)


    def testIsCreatedWithBuiltInIgnoreRegexes(self):
        config = FolderComparerConfig.FolderComparerConfig(
            'leftFolder', 'rightFolder', FolderComparerConfig.PREFER_NONE, [])

        regexes = config.GetIgnoreRegexes()
        self.assertTrue(len(regexes) > 0)


