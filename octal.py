import os, argparse, csv, pydoc

regular_files = {}
directories = {}

def report(dictname, permission):
    if dictname == 'directories': 
        text = '\nDirectories with ' + permission + ' permissions:\n'
        for path in directories[permission]:
            text = str(text) + str(path) + '\n'
    else: 
        text = '\nRegular files with ' + permission + ' permissions:\n'
        for path in regular_files[permission]:
            text = str(text) + str(path) + '\n'
    pydoc.pager(text)

def scanfiles(path):
    for item in os.listdir(path):
        item = os.path.normpath(os.path.join(path, item))
        key = oct(os.stat(item).st_mode)[-3:]
        try:
            if os.path.isdir(item):
                if not key in directories:
                    directories[key] = [item]
                else:
                    directories[key].append(item)
                scanfiles(item)
            elif os.path.isfile(item):
                if os.path.exists(item):
                    if not key in regular_files:
                        regular_files[key] = [item]
                    else:
                        regular_files[key].append(item)
        except:
           print('Could not read ', item)

def interactive():
    print('Interactive mode.  Type "exit" to stop.')
    while True: 
        path = input('Please enter a path:\n')
        if path == "" : continue
        if path in ('exit', 'Exit', 'EXIT'): 
            print('Stopping.')
            break
        if os.path.exists(path):
            scanfiles(path)
            for k, v in directories.items(): 
                print('[Code: d'+k+']','Directory Permission:\t', k,
                        "Number found:", len(v))
            for k, v in regular_files.items():
                print('[Code: r'+k+']', 'Regular File Permission:\t', k,
                        "Number found:", len(v))
            break
        else: print('Invalid path.')
    if path not in ('exit', 'Exit', 'EXIT'):
        while True:
            code = input('\nPlease enter a lookup code: ')
            if code == '' : continue
            if code in ('exit', 'EXIT', 'Exit'):
                print('Stopping.')
                break
            if code[0] in ('r', 'R') and code[1:] in regular_files:
                permission = code[1:]
                report('regular_files', permission)
            elif code[0] in ('d', 'D') and code[1:] in directories:
                permission = code[1:]
                report('directories', permission)
            else:
                print('Invalid code.')

def csvgen(filename, dictname):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['permission', 'path'])
        for k, v in dictname.items():
            for path in v:
                writer.writerow([k, path])

parser = argparse.ArgumentParser(description=(
    'Octal scans a specified path and lists all the regular file ' 
    'and/or directory permissions found in octal format along ' 
    'with the corresponding file(s).  Interactive mode is the preferred '
    'method and displays a summary of the permissions found.  The ' 
    'user then has the option to view all of the files that have a certain ' 
    'permission. Requires Python 3.x.'))
group = parser.add_mutually_exclusive_group()
group.add_argument(
        '-i', dest='interactive', action='store_true',
        help='Enter interactive mode (cannot be used with -p).')
group.add_argument(
        '-p', dest='path',
        help=('Generates the report as directories.csv and regular_files.csv.'
            ' PATH is the path to audit. Only recommended for afk use.'))
if parser.parse_args().path:
    scanfiles(parser.parse_args().path)
    csvgen('directories.csv', directories)
    csvgen('regular_files.csv', regular_files)
elif parser.parse_args().interactive:
    interactive()
else:
    parser.print_help()
