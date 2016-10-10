#!/usr/bin/python
# poor man's who

import utmp
from UTMPCONST import *
import time

a = utmp.UtmpRecord()

print "%-10s %-10s %5s %-25s %-20s" % ("USER", "TTY", "PID", "HOST", "LOGIN")

for b in a: # example of using an iterator
    if b.ut_type == USER_PROCESS:
        print "%-10s %-10s %5i %-25s %-20s" % \
        (b.ut_user, b.ut_line, b.ut_pid, 
         b.ut_host, time.ctime(b.ut_tv[0]))
a.endutent()

