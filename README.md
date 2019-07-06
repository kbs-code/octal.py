Where are the problematic file permissions on my Linux system?  How do I find them?
While you can answer this question by executing 'ls -l' along with other arguments or pipelines, Octal attempts to improve this process in a couple of ways:
- by displaying permissions in the octal format
- providing a useful summary that can be expanded, thus eliminating some tedium
- allowing for .csv reports to be generated, which work well with grep

Dependencies:

Python 3 (required)

less (highly recommended)

Note:

Only supports regular file and directory file types

from the help menu:

Octal scans a specified path and lists all the regular file and/or directory permissions found in octal format along with the corresponding file(s).  Interactive mode is the preferred method and displays a summary of the permissions found.  The user then has the option to view all of the files that have a certain permission. Requires Python 3.x.

