import re
import sys
import getopt

version = "0.1"

def analyzeMatch(countRow, countCompareRow, linesNumber, linesBefore, allLines, lineRow):
    linesAnalyzed = analyzeLinesBeforeLine(
        linesNumber[countRow-1], linesBefore, allLines)
    linesCompareAnalyzed = analyzeLinesBeforeLine(
        linesNumber[countCompareRow-1], linesBefore, allLines)
    sumVar = 0
    totalVar = int(linesBefore)
    posAnalyze = 0;
    for lineAnalyze in linesAnalyzed:
        posCompareAnalyze = 0;
        for lineCompareAnalyzed in linesCompareAnalyzed:
            if (lineCompareAnalyzed == lineAnalyze):
                if (posAnalyze > posCompareAnalyze):
                    if (posAnalyze == 0):
                        weightPos = 1
                    else:
                        weightPos = (posCompareAnalyze / posAnalyze)
                else:
                    if (posCompareAnalyze == 0):
                        weightPos = 1
                    else:
                        weightPos = (posAnalyze / posCompareAnalyze)
                sumVar += 1 * (weightPos)
                break
            posCompareAnalyze += 1
        posAnalyze += 1
    print " "
    print ("----------------------------------------------------"
            +"Match (%s)! "
            +"--------------------------------------------------\n"
            +"Lines: %s = %s. %s lines before each line analized.\n"
            +" \n"
            +"Line (without numbers): %s\n"
            +"-----------------------------------------------------------"
            +"-----------------------------------------------------------") % (
                "{0:.2f}%".format(sumVar*100/totalVar),
                linesNumber[countRow-1],
                linesNumber[countCompareRow-1],
                linesBefore,
                lineRow
            )
    print " "

def analyzeLinesBeforeLine(lineNumber, linesBefore, allLines):
    arrayToCompare = []
    #print "%s lines before line %s: " % (linesBefore, lineNumber)
    for x in reversed(range(2, 2 + int(linesBefore))):
        #print "line %s: %s" % (lineNumber-x+1, allLines[lineNumber-x])
        arrayToCompare.append(re.sub(r"[0-9]", "", allLines[lineNumber-x]))
    return arrayToCompare

def usage():
    print "Usage: searcher.py [options]"
    print "-p, --pattern=PATTERN    pattern to search"
    print "-f, --file=FILE          file where it will search"
    print "-l, --lines=LINES        number of lines used to the 'pattern algorithm' (default = 5)"
    print "-v, --version            print program version"

def main(argv):
    try:                                
        opts, args = getopt.getopt(argv, "?hvp:f:l:", ["version", "help", "pattern=", "file=", "lines="])
    except getopt.GetoptError:          
        print "GetoptError"        
        usage()                         
        sys.exit(2) 

    pattern = ""
    fileOpened = ""
    linesBefore = 5;
    for opt, arg in opts: 
        if opt in ("-h", "--help", "-?"): 
            usage()
            sys.exit()
        elif opt in ("-v", "--version"):
            print "TodayPASNow " + version
            sys.exit()
        elif opt in ("-f", "--file"):
            fileOpened = open(arg)
        elif opt in ("-p", "--pattern"):
            pattern = re.compile(arg)
        elif opt in ("-l", "--lines"):
            linesBefore = arg

    if (not pattern or not fileOpened):
        usage()
        sys.exit(2)

    isMatch = 0

    lines = [];
    linesNumber = [];
    allLines = fileOpened.readlines()
      
    for i, line in enumerate(allLines):
        for match in re.finditer(pattern, line):
            lines.append(re.sub(r"[0-9]", "#", line).strip())
            linesNumber.append(i+1)
            #print 'Found on line %s: %s' % (i+1, line)

    countRow = 0
    for lineRow in lines:
        countRow += 1
        countCompareRow = 0
        for lineCompareRow in lines:
            countCompareRow += 1
            if (lineCompareRow == lineRow and countRow != countCompareRow):
                isMatch = 1
                analyzeMatch(countRow, countCompareRow, linesNumber, 
                    linesBefore, allLines, lineRow);

    if (not isMatch):
        print "No matches..."

if __name__ == "__main__":
   main(sys.argv[1:])
