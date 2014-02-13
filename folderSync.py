#!/usr/bin/env python -O

import sys
import getopt
import os.path
import FolderComparerConfig
import FolderComparer
import prompts
import json
import re


def GetUsage():
    return r'''
folderSync.py --config <config_file>
folderSync.py --help
'''


NEWER_SIDE_LEFT = 0;
NEWER_SIDE_RIGHT = 1;

OUTPUT_WIDTH = 200

def PrintPairings(pairings):
    for pairing in pairings:
        PrintPairing(pairing)


def PrintPairing(pairing):
    print pairing.Render(OUTPUT_WIDTH)
    for curWarning in pairing.GetWarnings():
        print curWarning



if __name__ == '__main__':

    (options, args) = getopt.getopt(sys.argv[1:], '', ['config=', 'help'])
    for (option, value) in options:
        if option == '--help':
            print GetUsage()
            sys.exit(0)
        elif option == '--config':
            if not os.path.isfile(value):
                print '%s is not a file!' % value
                print GetUsage()
                sys.exit(1)
            jsonData = open(value)
            userConfig = json.load(jsonData)
            jsonData.close()
        else:
            print 'Unknown option!'
            print GetUsage()
            sys.exit(1)

    if len(args) > 0:
        print 'Invalid number of arguments!'
        print GetUsage()
        sys.exit(1)

    if not os.path.isdir(userConfig['leftDir']):
        print '%s is not a directory!' % userConfig['leftDir']
        print GetUsage()
        sys.exit(1)

    if not os.path.isdir(userConfig['rightDir']):
        print '%s is not a directory!' % userConfig['rightDir']
        print GetUsage()
        sys.exit(1)


    # res = prompts.GetChoice('Which side should have newer files?  ',
    #                         [os.path.abspath(leftDir), os.path.abspath(rightDir)])
    # newerSide = NEWER_SIDE_RIGHT;
    # if res == 0:
    #     newerSide = NEWER_SIDE_LEFT;

    # Compile the ignore regexes provided in the config file.
    userConfig['ignoreRegexes'] = [re.compile(curRegex, re.IGNORECASE) for curRegex in userConfig['ignoreRegexes']]

    # Translate the preferred side from the user config's string to the constant
    # value.
    userConfigPreferredSide = userConfig.get('preferSide', 'none')
    if userConfigPreferredSide == 'left':
        userConfigPreferredSide = FolderComparerConfig.PREFER_LEFT
    elif userConfigPreferredSide == 'right':
        userConfigPreferredSide = FolderComparerConfig.PREFER_RIGHT
    else:
        userConfigPreferredSide = FolderComparerConfig.PREFER_NONE

    config = FolderComparerConfig.FolderComparerConfig(
        userConfig['leftDir'],
        userConfig['rightDir'],
        userConfigPreferredSide,
        userConfig['ignoreRegexes'])

    comp = FolderComparer.FolderComparer(config)

    print '-' * OUTPUT_WIDTH
    print 'Left:', config.GetLeftFolder()
    print 'Right:', config.GetRightFolder()
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

    # Count the number of items that need to be synchronized.
    numItemsToSync = 0
    for (desc, pairings) in categorizedPairings:
        numItemsToSync += len(pairings)
    print
    print '%d items are out of sync.' % numItemsToSync

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



