#! /usr/bin/python -O
import os.path
import re
import texttable

def PromptToContinue():
    raw_input('Press ENTER to continue.')


def GetYesNo(prompt):
    r'''Returns True if the user chose yes.  Otherwise, returns False.'''
    responseIsValid = False
    fullPrompt = prompt + ' (y/n): ' if (prompt) else '(y/n): '

    while (not responseIsValid):
        response = raw_input(fullPrompt)
        if (response == 'y') or (response == 'n'):
            responseIsValid = True
    return True if (response == 'y') else False


def GetDir(prompt, default = None):
    prompt2 = prompt
    if default:
        prompt2 += ' [' + default + ']'
    prompt2 += ': '

    print prompt2

    inputIsValid = False
    while not inputIsValid:
        theDir = raw_input('> ')
        if (theDir == '') and default:
            theDir = default
        inputIsValid = os.path.isdir(theDir)
    return theDir


def GetMaskedInput(prompt, regex, default = None):
    prompt2 = prompt
    if default:
        prompt2 += ' [' + default + ']'
    prompt2 += ':'

    print prompt2

    inputIsValid = False
    while not inputIsValid:
        userInput = raw_input('> ')
        if (userInput == '') and default:
            userInput = default
        inputIsValid = regex.match(userInput)
    return userInput


def GetChoice(prompt, choices):
    r'''Returns the index of the chosen choice.'''
    choiceRegex = re.compile(r'^(\d+)$')

    table = texttable.TextTable()
    table.SetHorizontalAlignment([texttable.HALIGN_RIGHT, texttable.HALIGN_LEFT])
    table.SetOuterLinesMode(texttable.OUTER_LINES_ALL)
    table.SetHorizontalLinesMode(texttable.HORIZ_LINES_ALL)
    table.SetVerticalLinesMode(texttable.VERT_LINES_FIRST)

    for curIndex in range(len(choices)):
        table.AddRow(['%d' % curIndex, choices[curIndex]])
    table.Print()

    inputIsValid = False
    while not inputIsValid:
        userInput = raw_input(prompt)
        choiceMatch = choiceRegex.match(userInput)
        if (choiceMatch):
            chosenIndex = int(choiceMatch.group(1))
            if (chosenIndex in range(len(choices))):
                inputIsValid = True
                userInput = chosenIndex
    return userInput


def GetMaskedInputWithChoices(prompt, regex, choices):
    choiceRegex = re.compile(r'^/(\d+)$')

    table = texttable.TextTable()
    table.SetHorizontalAlignment([texttable.HALIGN_RIGHT, texttable.HALIGN_LEFT, texttable.HALIGN_LEFT])
    table.SetOuterLinesMode(texttable.OUTER_LINES_ALL)
    table.SetHorizontalLinesMode(texttable.HORIZ_LINES_ALL)
    table.SetVerticalLinesMode(texttable.VERT_LINES_FIRST)
    table.AddRow(['Shortcut', 'Choice', ''])
    for curIndex in range(len(choices)):
        table.AddRow(['/%d' % curIndex, choices[curIndex][0], '(%s)' % choices[curIndex][1]])
    table.Print()

    inputIsValid = False
    while not inputIsValid:
        userInput = raw_input('%s > ' % prompt)
        if (userInput == ''):
            userInput = '/0'
        
        choiceMatch = choiceRegex.match(userInput)
        if (choiceMatch):
            chosenIndex = int(choiceMatch.group(1))
            if (chosenIndex in range(len(choices))):
                inputIsValid = True
                userInput = choices[chosenIndex][0]
        else:
            inputIsValid = regex.match(userInput)

    return userInput

    
    
if __name__ == '__main__':
    # res = GetMaskedInputWithChoices(
    #     'Enter machine name',
    #     re.compile('.*'),
    #     [['usmaylnkbld002', 'AOP build machine'], ['usmayaoptest1', 'aop unit test machine']])
    # print 'User entered:', res

    res = GetChoice('Pick a number:  ', ['one', 'two', 'three', 'four', 'five'])
    print 'User selected choice at index:', res
