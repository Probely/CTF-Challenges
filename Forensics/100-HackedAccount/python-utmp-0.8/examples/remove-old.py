#!/usr/bin/python
# remove tty given as argument from utmp file

import utmp, sys
from UTMPCONST import *

a = utmp.UtmpRecord()

line = sys.argv[1]

b = a.getutline_dict(line)
if not b:
    print line, "is not occupied, cannot remove."
    sys.exit()
b['ut_type'] = DEAD_PROCESS
b['ut_line'] = ''
b['ut_user'] = ''
a.pututline_dict(b)
a.endutent()

