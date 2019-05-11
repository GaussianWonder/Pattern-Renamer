import sys

# SETUP (argument reader, help printer, etc...)
def errorParsingArguments():
    print('There were errors while parsing the arguments')
    print('Foreign argument | Incomplete argument given')
    print('See --help    | -h')

def showHelp():
    print('--path     | -p     => Path to folder')
    print('--match    | -m     => Pattern to match')
    print('--white-sp | -wp    => White space is a separator\n')
    print('Pattern :  (encapsulate in \" \")     ')
    print('     % => Any string combination to be ignored')
    print('     @ => Any number NOT to be ignored')
    print('     & => Any string NOT to be ignored\n')
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
whiteSeparator = True # Default must be False !! CHANGE THIS

sz = len(sys.argv)
i = 1
while(i < sz):
    arg = sys.argv[i]

    if arg == '--help'  or arg == '-h':
        showHelp()
        sys.exit(0)
    elif (arg == '--path'  or arg == '-p') and i + 1 < sz:
        i += 1
        path = sys.argv[i]
    elif (arg == '--match' or arg == '-m') and i + 1 < sz:
        i += 1
        pattern = sys.argv[i]
    elif arg == '--white-sp' or arg == '-wp':
        whiteSeparator = True
    else :
        errorParsingArguments()
        sys.exit(0)
    
    i += 1

if path == '' or pattern == '':
    print('Path and Pattern required!')
    print('See --help    | -h')
    sys.exit(0)

print('Using path: '    + path)
print('Using pattern: ' + pattern)

# SETUP DONE => FILE RENAMER:
