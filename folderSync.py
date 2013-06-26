#! /usr/bin/python -O
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

    print 'Diff files:'

    for diffFilePairing in comp.GetDiffFilePairings():
        print diffFilePairing.Render(130)

    print 'Left-only files:'
    for curFile in comp.GetLeftOnlyFiles():
        print utility.ShortenPath(curFile, 30)

    print 'Right-only files:'
    for curFile in comp.GetRightOnlyFiles():
        print utility.ShortenPath(curFile, 30)

