#!/usr/bin/python
# poor man's last

import utmp
from UTMPCONST import *
import time

a = utmp.UtmpRecord(WTMP_FILE)

print "%-10s %-10s %-30s %-20s" % ("USER", "TTY", "HOST", "LOGIN")

while 1:
    b = a.getutent()
    if not b:
        break
    if b[0] == USER_PROCESS:
        print "%-10s %-10s %-30s %-20s" % (b[4], b[2], b[5], time.ctime(b[8][0]))
a.endutent()

