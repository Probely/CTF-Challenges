#!/usr/bin/python

import utmp
from UTMPCONST import *
import time, pwd, grp, os, string, sys, socket, popen2
from stat import *
from string import lower


def getrealname(gec):
    # get real name from gecos fiels
    return string.split(gec,",",1)[0]

def formatidle(t):
    if t<30:
        return ""
    if t<80:
        r = "%ss" % int(t)
        return r
    if t<60*80:
        return "%sm" % int(t/60)
    if t<60*60*28:
        return "%sh" % int(t/60/60)
    if t<60*60*24*20:
        return "%sd" % int(t/60/60/24)
    return "DEAD"

def userlist(u, now, user=""):
    u.setutent()
    tnow = time.mktime(now)
    header = 0
    output = [] # list of output lines, without header
    while 1:
        b = u.getutent()
        if not b:
            break
        if b.ut_type == USER_PROCESS:
            username = b.ut_user
            if user and b.ut_user!=user:
                continue
            try:
                pwnam = pwd.getpwnam(username)
            except KeyError:
                pwnam = '?'

            tty = b.ut_line

            t = time.localtime(b.ut_tv[0])
            then = time.mktime(t)
            if tnow<then: # login in the future?
                login = "FUTURE"
            elif t[7] == now[7] and t[0] == now[0]: # today
                login = time.strftime("%H:%M", t)
            elif tnow-then<60*60*24*7: # this week
                login = time.strftime("%a", t)
            elif tnow-then<60*60*24*365.: # this year
                login = time.strftime("%d-%b", t)
            else: # way down in the past
                login = time.strftime("%Y", t)
            location = b.ut_host
            tty = b.ut_line
            try:
                s = os.stat("/dev/"+tty)
                p = s[ST_MODE] & 0x30 # 060 octal - test executable bit
                if tnow<s[ST_ATIME]:
                    idle = 0
                else:
                    idle = tnow-s[ST_ATIME]
                idle = formatidle(idle)
                if p:
                    p = ' '
                else:
                    p = '*'
            except:
                p = '?'
                
            if p == '?':
                continue
            #length sanitation
            username = username[:12]
            #realname = realname[:22]
            login = login[:6]
            location = location[:30]

            if not header:
                #print 60*"-"
                print ("%-12s%-7s%-4s%-2s%-8s%-30s" % \
                       ("USERNAME","Login","Idle","", "TTY","Location")
                      )
                #print 60*"-"
                header = 1
        
            output.append( "%-12s%-7s%4s%2s%-8s%-30s" % 
                   (username,login,idle,p,tty,location) )
    output.sort()
    for i in output:
        print(i)
    return output

def lastlogin(u, user):
    lastlogin = 0, ""
    u.setutent()
    while 1:
        b = u.getutent_dict()
        if not b:
            break
        if b.ut_type in (USER_PROCESS, DEAD_PROCESS) and \
           b.ut_user == user and \
           b.ut_tv[0]>lastlogin[0]:
            lastlogin = b.ut_tv[0], b.ut_host

    u = utmp.UtmpRecord(WTMP_FILE)
    while 1:
        b = u.getutent_dict()
        if not b:
            break
        if b.ut_type in (USER_PROCESS, DEAD_PROCESS) and \
           b.ut_user == user and \
           b.ut_tv[0]>lastlogin[0]:
            lastlogin = b.ut_tv[0], b.ut_host
    u.endutent()
    return lastlogin

def userplan(homedir):          
    try:
        f = open(homedir+"/.plan", "r")
        print("Plan:")
        while 1:
            l = f.readline()
            if not l:
                break
            print string.rstrip(l)
    except:
        pass


def oneuser(u, user):
    pwent = pwd.getpwnam(user)
    rn = getrealname(pwent[4])
    print ("Login name: %-30s In real life: %s" % (user, rn))
    print (" Directory: %-30s Shell: %s" % (pwent[5], pwent[6]))
    print ("            %-30s Group: [%s]" % ("", grp.getgrgid(pwent[3])[0]))
    l, h = lastlogin(u, user)
    if not l:
        print("Never logged in.")
    else:
        r = "Last login %-30s  " % time.strftime("%A, %d-%b-%Y %H:%M", time.localtime(l))
        if h:
            r = r+'from: '+h
        print(r)
    print('\n')
    userplan(pwent[5])

print('\n')

if len(sys.argv) == 2 and "@" in sys.argv[1]: # remote
    user, host = string.split(sys.argv[1], "@", 1)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        FINGER_PORT = 79
        s.connect( (host, FINGER_PORT) )
        s.send(user + '\r\n')
        while 1:
            buf = s.recv(1024)
            if not buf: break
            sys.stdout.write(buf)
        sys.stdout.flush()
    except socket.error, why:
        print "ERROR:", why
    sys.exit(0)

now = time.localtime(time.time())
a = utmp.UtmpRecord()

if len(sys.argv) == 1: # list of all local users
    r = userlist(a, now)
    if not r:
        print "No such processes."

else:
    #first find out if user exists
    user = sys.argv[1]
    try:
        pwd.getpwnam(user)
        r = userlist(a, now, user)
        if not r:
            print '"%s" isn\'t logged in.' % user
        print
        oneuser(a, user)
    except KeyError:
        print '"%s" does not match any user of this system.' % user
a.endutent()

