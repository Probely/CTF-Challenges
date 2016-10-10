#!/usr/bin/python
# scan utmp and remove bogus entries
# works only for systems that have ut_pid
# linux has, BSD has not

import utmp
from UTMPCONST import *
import time, os, string

a = utmp.UtmpRecord()

print ("Removing bogus entries:")
print ("%-10s %-10s %5s %-25s %-20s" % ("USER", "TTY", "PID", "HOST", "LOGIN"))

ps = os.popen("ps aux").readlines()[1:]
#ps = os.popen("ps -edf").readlines()[1:]
pids = {}
for i in ps:
    user, pid = i.split()[:2]
    pids[int(pid)] = user


for b in a:
    if b.ut_type == USER_PROCESS:
        if (b.ut_pid not in pids) or b.ut_user!=pids[b.ut_pid]:
            print ("%-10s %-10s %5i %-25s %-20s" % (b.ut_user, b.ut_line, b.ut_pid, b.ut_host, time.ctime(b.ut_tv[0])))
            b.ut_type = DEAD_PROCESS
            b.ut_host = ''
            b.ut_tv = (0, 0)
            a.pututline(b)
            a.getutent() # to move to next entry

