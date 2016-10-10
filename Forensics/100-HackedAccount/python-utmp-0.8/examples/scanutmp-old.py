#!/usr/bin/python
# scan utmp and remove bogus entries
# works only for systems that have ut_pid
# linux has, BSD has not

import utmp
from UTMPCONST import *
import time, os, string

a = utmp.UtmpRecord()

print "Removing bogus entries:"
print "%-10s %-10s %5s %-25s %-20s" % ("USER", "TTY", "PID", "HOST", "LOGIN")

ps = os.popen("ps aux").readlines()[1:]
#ps = os.popen("ps -edf").readlines()[1:]
pids = {}
for i in ps:
    user, pid = string.split(i)[:2]
    pids[int(pid)] = user

while 1:
    b = a.getutent()
    if not b:
        break
    if b[0] == USER_PROCESS:
        if (not pids.has_key(b[1])) or b[4]<>pids[b[1]]:
            print "%-10s %-10s %5i %-25s %-20s" % (b[4], b[2], b[1], b[5], time.ctime(b[8][0]))
            b = list(b)
            b[0] = DEAD_PROCESS
            b[4] = ''
            b[8] = (0, 0)
            a.pututline(b)
            a.getutent() # to move to next entry
a.endutent()

