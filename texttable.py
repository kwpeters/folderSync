HALIGN_LEFT   = 0
HALIGN_CENTER = 1
HALIGN_RIGHT  = 2

VERT_LINES_NONE  = 0
VERT_LINES_FIRST = 1
VERT_LINES_ALL   = 2

HORIZ_LINES_NONE  = 0
HORIZ_LINES_FIRST = 1
HORIZ_LINES_ALL   = 2

OUTER_LINES_NONE = 0
OUTER_LINES_ALL  = 1


class TextTable(object):
    def __init__(self):
        self.__NumCols = 0
        self.__NumRows = 0
        self.__HorizAlignments = []
        self.__Data = []
        self.__VertLinesMode = VERT_LINES_NONE
        self.__HorizLinesMode = HORIZ_LINES_NONE
        self.__OuterLinesMode = OUTER_LINES_NONE


    def SetHorizontalAlignment(self, horizAlignments):
        self.__UpdateNumCols(len(horizAlignments))

        for colIndex in range(len(horizAlignments)):
            self.__HorizAlignments[colIndex] = horizAlignments[colIndex]


    def AddRow(self, rowData):
        self.__UpdateNumCols(len(rowData))
        textData = [str(data) for data in rowData]
        self.__Data.append(textData)
        self.__NumRows = self.__NumRows + 1


    def SetVerticalLinesMode(self, vertMode):
        self.__VertLinesMode = vertMode


    def SetHorizontalLinesMode(self, horizMode):
        self.__HorizLinesMode = horizMode


    def SetOuterLinesMode(self, outerLinesMode):
        self.__OuterLinesMode = outerLinesMode


    def GetOutputLines(self):
        outputLines = []

        # Calculate the column widths.
        colWidths = [0 for i in range(self.__NumCols)]
        for rowIndex in range(self.__NumRows):
            for colIndex in range(self.__NumCols):
                colWidths[colIndex] = max(colWidths[colIndex], len(self.__Data[rowIndex][colIndex]))

        # Formulate what needs to prepended and appended onto each
        # line to account for outer lines.
        outerLinesPrepend = ['', '']
        outerLinesAppend = ['', '']
        if self.__OuterLinesMode == OUTER_LINES_ALL:
            outerLinesPrepend = ['| ', '|-'] # Index 0 is for rows with data, index 1 is for rows with lines
            outerLinesAppend = [' |', '-|']  # Index 0 is for rows with data, index 1 is for rows with lines

        # Figure out how long each line is going to be (without space for outer lines)
        numGutters = self.__NumCols - 1
        # Start with the width of the text in each column.
        lineLengthWithoutOuter = sum(colWidths)
        # Add space for the gutters
        if self.__VertLinesMode == VERT_LINES_NONE:
            lineLengthWithoutOuter = lineLengthWithoutOuter + numGutters * 1
        elif self.__VertLinesMode == VERT_LINES_FIRST:
            lineLengthWithoutOuter = lineLengthWithoutOuter + 1 * 3 + (numGutters - 1) * 1
        elif self.__VertLinesMode == VERT_LINES_ALL:
            lineLengthWithoutOuter = lineLengthWithoutOuter + numGutters * 3

        # Formulate what the horizontal line is going to be.
        if self.__VertLinesMode == VERT_LINES_NONE:
            horizLine = '-' * lineLengthWithoutOuter
        elif self.__VertLinesMode == VERT_LINES_FIRST:
            horizLine = '-' * colWidths[0] + '-+-' + '-'.join(['-' * colWidth for colWidth in colWidths[1:]])
        elif self.__VertLinesMode == VERT_LINES_ALL:
            horizLine = '-+-'.join(['-' * colWidth for colWidth in colWidths])
        horizLine = outerLinesPrepend[1] + horizLine + outerLinesAppend[1]


        for rowIndex in range(self.__NumRows):
            cellStrings = []
            for colIndex in range(self.__NumCols):
                horizAlignment = self.__HorizAlignments[colIndex]
                if  horizAlignment == HALIGN_LEFT:
                    cellStrings.append(self.__Data[rowIndex][colIndex].ljust(colWidths[colIndex]))
                elif horizAlignment == HALIGN_CENTER:
                    cellStrings.append(self.__Data[rowIndex][colIndex].center(colWidths[colIndex]))
                else:
                    cellStrings.append(self.__Data[rowIndex][colIndex].rjust(colWidths[colIndex]))


            # Formulate the acutal output line of text.
            if self.__VertLinesMode == VERT_LINES_NONE:
                outputLine = ' '.join(cellStrings)
            elif self.__VertLinesMode == VERT_LINES_FIRST:
                outputLine = cellStrings[0] + ' | ' + ' '.join(cellStrings[1:])
            elif self.__VertLinesMode == VERT_LINES_ALL:
                outputLine = ' | '.join(cellStrings)
            outputLine = outerLinesPrepend[0] + outputLine + outerLinesAppend[0]

            horizLineNeedsToFollow = (((self.__HorizLinesMode == HORIZ_LINES_FIRST) and (rowIndex == 0)) or
                ((self.__HorizLinesMode == HORIZ_LINES_ALL) and (rowIndex < self.__NumRows - 1)))
                    
            if (rowIndex == 0) and (self.__OuterLinesMode == OUTER_LINES_ALL):
                outputLines.append(horizLine)

            outputLines.append(outputLine)
            if horizLineNeedsToFollow:
                outputLines.append(horizLine)

            if (rowIndex == self.__NumRows - 1) and (self.__OuterLinesMode == OUTER_LINES_ALL):
                outputLines.append(horizLine)
        
        return outputLines


    def Print(self):
        print '\n'.join(self.GetOutputLines())


    def __UpdateNumCols(self, numCols):
        if (numCols > self.__NumCols):
            self.__NumCols = numCols

            while len(self.__HorizAlignments) < numCols:
                self.__HorizAlignments.append(HALIGN_LEFT)

            for curRow in self.__Data:
                while len(curRow) < numCols:
                    curRow.append('')


if __name__ == '__main__':
    table = TextTable()
    table.SetHorizontalAlignment([HALIGN_LEFT, HALIGN_LEFT, HALIGN_LEFT, HALIGN_RIGHT])

    #table.SetOuterLinesMode(OUTER_LINES_NONE)
    table.SetOuterLinesMode(OUTER_LINES_ALL)

    #table.SetVerticalLinesMode(VERT_LINES_NONE)
    #table.SetVerticalLinesMode(VERT_LINES_FIRST)
    table.SetVerticalLinesMode(VERT_LINES_ALL)

    #table.SetHorizontalLinesMode(HORIZ_LINES_NONE)
    #table.SetHorizontalLinesMode(HORIZ_LINES_FIRST)
    table.SetHorizontalLinesMode(HORIZ_LINES_ALL)

    table.AddRow(['Last',   'First',    'Middle', 'Age'])
    table.AddRow(['Peters', 'Kevin',    'William',   37])
    table.AddRow(['Mastey', 'Pamela',   'Joyce',     40])
    table.AddRow(['Peters', 'Audrey',   'Eileen',     3])
    table.AddRow(['Peters', 'Madeline', 'Faith',      2])
    table.AddRow(['Peters', 'Lily',     'Caroline',   0])
    table.Print()

