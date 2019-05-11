import sys

def showHelp():
    print('--path    | -p     => Path to folder')
    print('--match   | -m     => Pattern to match\n')
    print('Pattern :')
    print('     % => Any string combination to be ignored')
    print('     $ => Any number NOT to be ignored')
    print('     & => Any string NOT to be ignored')
    print('EG:  %_$_&_% matches XASD_123_WOW_DSAX')
    print('                      ^^   ^   ^   ^^')
    print(' $ and & will be      %    $   &   % ')
    print('       deleted                       ')

if len(sys.argv) == 1:
    showHelp()
    sys.exit(0)

path    = ''
pattern = ''

for arg in sys.argv[1:]:
    if arg == '--help'  or arg == '-h':
        showHelp()
        sys.exit(0)
    elif arg == '--path'  or arg == '-p':
        path = arg
    elif arg == '--match' or arg == '-m':
        pattern = arg
    else :
        showHelp()
        sys.exit(0)

if path == '' or pattern == '':
    print('All arguments required!')
    print('--help    | -h')

