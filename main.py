import sys
import os

# SETUP (argument reader, help printer, etc...) <==========================================
def errorParsingArguments():
    print('There were errors while parsing the arguments')
    print('Foreign argument | Incomplete argument given')
    print('See --help    | -h')

def showHelp():
    print('--path     | -p     => Path to folder')
    print('--match    | -m     => Pattern to match')
    print('--white-sp | -wp    => White space ends \'&\'')
    print('--print    | -pr    => Print instead of renaming (Testing purpose)')
    print('Pattern :  (encapsulate in \" \")     ')
    print('     % => Any string combination to be ignored')
    print('     @ => Any number NOT to be ignored (stops at character  | raw ascii)')
    print('     & => Any string NOT to be ignored (stops at whitespace | raw ascii)\n')
    print('EG:  %_$_&_% matches XASD_123_WOW_DSAX')
    print('                      ^^   ^   ^   ^^')
    print(' $ and & will be      %    $   &   % ')
    print(' deleted from                        ')
    print(' the file name  <=>  XASDDSAX        ')
    print(' along with any raw char in pattern  ')

if len(sys.argv) == 1:
    showHelp()
    sys.exit(0)

path    = ''
pattern = ''
whiteSeparator = False
printOnly = False

#scan arguments
sz = len(sys.argv)
i = 1
while(i < sz):
    arg = sys.argv[i]

    if arg == '--help'  or arg == '-h':
        showHelp()
        sys.exit(0)
    elif arg == '--print' or arg == '-pr':
        printOnly = True
    elif (arg == '--path'  or arg == '-p') and i + 1 < sz:
        i += 1
        path = sys.argv[i]
    elif (arg == '--match' or arg == '-m') and i + 1 < sz:
        i += 1
        pattern = sys.argv[i]
    elif arg == '--white-sp' or arg == '-wp':
        whiteSeparator = True
    else:
        errorParsingArguments()
        sys.exit(0)
    
    i += 1

if path == '' or pattern == '':
    print('Path and Pattern required!')
    print('See --help    | -h')
    sys.exit(0)

print('Using path: '    + path)
print('Using pattern: ' + pattern)
if whiteSeparator == True:
    print('White space WILL interfere when using \'&\'\n')
else:
    print('White space WILL NOT interfere when using \'&\'\n')

# SETUP DONE => FILE RENAMER <=============================================================

#check if the path is valid
if os.path.isdir(path) == False:
    print('Invalid PATH')
    sys.exit(0)

#check pattern
i = 1
sz = len(pattern)
wellFormatted = True
while i < sz and wellFormatted == True:
    if pattern[i - 1] == pattern[i] and (pattern[i] == '@' or pattern[i] == '&' or pattern[i] == '%'):
        wellFormatted = False
    i += 1

if wellFormatted == False:
    print('Invalid PATTERN')
    print('No adjacent special characters: %% @& &%')
    sys.exit(0)

patternsToSearch = pattern.split("%")


#renames a string based on pattern
def rename(string, patternArray):
    lastIndex = 0
    modStr = string

    #browse sub patterns from pattern
    for pattern in patternArray:
        i = 0
        sz = len(pattern)
        while i < sz and pattern[i] != '@' and pattern[i] != '&':
            i += 1
        
        startMatch = pattern[:i]
        endMatch   = pattern[i + 1:]

        #nothing to be matched
        if startMatch == '' and endMatch == '':
            continue

        startIndex = modStr.find(startMatch, lastIndex)
        endIndex   = -1
        #didn't find a matching start
        if startIndex == -1 or startIndex >= len(modStr):
            continue

        #search a number
        if pattern[i] == '@':   # search a number
            i = startIndex + len(startMatch)
            while i < len(modStr) and modStr[i] >= '0' and modStr[i] <='9':
                i += 1

            endIndex = i
            j = 0
            while endIndex < len(modStr) and j < len(endMatch) and modStr[endIndex] == endMatch[j]:
                endIndex += 1
                j += 1

            #didn't find a matching end
            if j < len(endMatch):
                continue
        #search the last string ending with the desired endMatch
        elif pattern[i] == '&':
            i = startIndex + len(startMatch)
            endIndex = i
            if len(endMatch) == 0:
                #no endMatch
                if whiteSeparator == True:
                    while endIndex < len(modStr) and modStr[endIndex] != ' ' and modStr[endIndex] != '\n':
                        endIndex += 1
                else:
                    endIndex = len(modStr) - 1

                if endIndex >= len(modStr):
                    endIndex = len(modStr) - 1
            else:
                #search last matched
                if whiteSeparator == False:
                    indexFound = modStr.find(endMatch, endIndex)
                    if indexFound != -1:
                        while indexFound != -1:
                            endIndex = indexFound + len(endMatch) - 1
                            indexFound = modStr.find(endMatch, endIndex + 1)
                    else:
                        endIndex = -1
                else:
                    whiteSpace = modStr.find(' ', endIndex)
                    indexFound = modStr.find(endMatch, endIndex)

                    if indexFound == -1 and whiteSpace == -1:
                        continue
                    
                    if (whiteSpace != -1 and indexFound == -1) or (whiteSpace != -1 and indexFound != -1 and whiteSpace <= indexFound):
                        endIndex = whiteSpace
                    else:
                        if indexFound != -1:
                            while indexFound != -1:
                                endIndex = indexFound + len(endMatch) - 1
                                indexFound = modStr.find(endMatch, endIndex + 1)
                        else:
                            endIndex = -1   

        if endIndex == -1:
            continue
        
        if endIndex >= len(modStr):
                endIndex = len(modStr) - 1

        #delete mid content
        modStr = modStr[:startIndex] + modStr[endIndex + 1:]
        #update lastIndex reached
        lastIndex = startIndex

    return modStr

# scan directory for files and rename everything according to a pattern
directory = os.fsencode(path)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filepath = os.path.join(path, filename)
    name, extension = os.path.splitext(filename)

    renamed = rename(name, patternsToSearch)
    filepathRenamed = os.path.join(path, renamed + extension)

    if printOnly == True:
        print(renamed)
    else:
        print(renamed)
        # os.rename(filepath, filepathRenamed)

