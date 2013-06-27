#! /usr/bin/python
import sys
import getopt
import os.path
import FolderComparer
import prompts
import utility


def GetUsage():
    return r'''
folderSync.py <left_folder> <right_folder>
'''


NEWER_SIDE_LEFT = 0;
NEWER_SIDE_RIGHT = 1;

OUTPUT_WIDTH = 120

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

    comp = FolderComparer.FolderComparer(leftDir, rightDir, FolderComparer.PREFER_NONE)

    # Same files are not interesting.
    # print 'Same files:'
    # print comp.GetSameFiles()

    print 'Left:', leftDir
    print 'Right:', rightDir

    diffPairings = comp.GetDiffFilePairings()
    leftOnlyPairings = comp.GetLeftOnlyFilePairings()
    leftOnlyDirPairings = comp.GetLeftOnlyDirPairings()
    rightOnlyPairings = comp.GetRightOnlyFilePairings()
    rightOnlyDirPairings = comp.GetRightOnlyDirPairings()

    if len(diffPairings) > 0:
        print
        print 'Modified files:'
        PrintPairings(diffPairings)

    if len(leftOnlyPairings) > 0:
        print
        print 'Left-only files:'
        PrintPairings(leftOnlyPairings)

    if len(leftOnlyDirPairings) > 0:
        print
        print 'Left-only directories:'
        PrintPairings(leftOnlyDirPairings)

    if len(rightOnlyPairings) > 0:
        print
        print 'Right-only files:'
        PrintPairings(rightOnlyPairings)

    if len(rightOnlyDirPairings) > 0:
        print
        print 'Right-only directories:'
        PrintPairings(rightOnlyDirPairings)
