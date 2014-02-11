#!/usr/bin/env python -O

import sys
import getopt
import os.path
import FolderComparerConfig
import FolderComparer
import prompts


def GetUsage():
    return r'''
folderSync.py <left_folder> <right_folder>
'''


NEWER_SIDE_LEFT = 0;
NEWER_SIDE_RIGHT = 1;

OUTPUT_WIDTH = 300

def PrintPairings(pairings):
    for pairing in pairings:
        PrintPairing(pairing)


def PrintPairing(pairing):
    print pairing.Render(OUTPUT_WIDTH)
    for curWarning in pairing.GetWarnings():
        print curWarning



if __name__ == '__main__':

    (options, args) = getopt.getopt(sys.argv[1:], '', ['help'])
    for (option, value) in options:
        if option == '--help':
            print GetUsage()
            sys.exit(0)
        else:
            print 'Unknown option!'
            print GetUsage()
            sys.exit(1)

    if len(args) != 2:
        print 'Invalid number of arguments!'
        print GetUsage()
        sys.exit(1)

    leftDir = args[0]
    rightDir = args[1]

    if not os.path.isdir(leftDir):
        print '%s is not a directory!' % leftDir
        print GetUsage()
        sys.exit(1)

    if not os.path.isdir(rightDir):
        print '%s is not a directory!' % rightDir
        print GetUsage()
        sys.exit(1)


    # res = prompts.GetChoice('Which side should have newer files?  ',
    #                         [os.path.abspath(leftDir), os.path.abspath(rightDir)])
    # newerSide = NEWER_SIDE_RIGHT;
    # if res == 0:
    #     newerSide = NEWER_SIDE_LEFT;

    config = FolderComparerConfig.FolderComparerConfig(leftDir, rightDir, FolderComparerConfig.PREFER_NONE, [])
    comp = FolderComparer.FolderComparer(config)

    print '-' * OUTPUT_WIDTH
    print 'Left:', leftDir
    print 'Right:', rightDir
    print '-' * OUTPUT_WIDTH

    # A list of tuples containing a description of the category and
    # the pairings for that category.  A list was used in order to
    # keep the order of the categories.
    categorizedPairings = [
        ('Modified Files', comp.GetDiffFilePairings()),
        ('Left-only Files', comp.GetLeftOnlyFilePairings()),
        ('Left-only Directories', comp.GetLeftOnlyDirPairings()),
        ('Right-only Files', comp.GetRightOnlyFilePairings()),
        ('Right-only Directories', comp.GetRightOnlyDirPairings())
        ]

    # Display an overview of all the categories and thier pairings.
    for (desc, pairings) in categorizedPairings:
        if len(pairings) > 0:
            print
            print desc + ':'
            PrintPairings(pairings)
            acceptOperations = prompts.GetYesNo('Accept operations?')
            if acceptOperations:
                for pairing in pairings:
                    PrintPairing(pairing)
                    pairing.PerformAction()

    # todo: Interview the user to set the action for each pairing.
    # todo: Complete the interview before starting to execute actions.



