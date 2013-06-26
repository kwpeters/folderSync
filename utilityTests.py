import unittest
import utility
import os
import os.path


class UtilityTests(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testShortenPath(self):
        path = os.path.join('one', 'two', 'three', 'four', 'five.txt')
        expected = 'one' + os.sep + '...' + os.sep + 'five.txt'
        self.assertEqual(utility.ShortenPath(path, 16), expected)

        path = os.sep + 'one' + os.sep + 'two' + os.sep + 'three' + os.sep + 'four' + os.sep + 'five.txt'
        expected = os.sep + 'one' + os.sep + '...' + os.sep + 'five.txt'
        self.assertEqual(utility.ShortenPath(path, 17), expected)
