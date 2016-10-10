#!/usr/bin/python

import utmp
from UTMPCONST import *
import time, pwd, grp, os, string, sys, socket
from stat import *
from string import upper

def boguslist():
    # get list of (pid, tty, commandname)
    # bogus because we are just guessing by the output of ps
    pscmd = "ps ac" # seems to be common
    psoutput = os.popen(pscmd).readlines()
    output = []
    del psoutput[0]
    for i in psoutput:
        l = string.split(i)
        pid, tty, command = int(l[0]), l[1], l[-1]
        output.append( (pid, tty, command) )
    return output
    
def proctable():
    #make table of ttys and corresponding pids
    global proctbl
    proctbl = {}
    for i in boguslist():
        if not proctbl.has_key(i[1]):
            proctbl[i[1]] = []
        proctbl[i[1]].append( (i[0], i[2]) )
            

def header(now, boottime, ops, ver):
    print "Consortium for global VMSfication"
    print time.strftime("%A, %d-%b-%Y %H:%M,", now), "%s V%s" %(ops, ver)
    print "Cluster  contains 1 node, formed", \
          time.strftime("%A, %d-%b-%Y %H:%M",  time.localtime(boottime))
    print

def getrealname(gec):
    # get real name from gecos fiels
    return string.split(gec,",",1)[0]

def userlist(u, now, node, user=""):
    proctable()
    u.setutent()
    tnow = time.mktime(now)
    header = 0
    output = [] # list of output lines, without header
    while 1:
        b = u.getutent_dict()
        if not b:
            break
        if b['ut_type'] == USER_PROCESS:
            username = b['ut_user']
            if user and b['ut_user']<>user:
                continue
            try:
                pwnam = pwd.getpwnam(username)
            except KeyError:
                continue
            realname = getrealname(pwnam[4])
            username = upper(username) # yeah, right :-)
            if 0:
                try:
                    # this works on linux and freebsd
                    # unfortunately, even if it works,
                    # it does not work well because it always returns shell...
                    f = open("/proc/%i/cmdline" % b['ut_pid'], "r")
                    program = f.read()
                    program = os.path.split(program)[1]
                except:
                    program = "?"

            tty = b['ut_line']
            program = max(proctbl[tty])[1]
            program = string.split(program, ".")[0] # SunOS uses dots in names
                
            shell = os.path.split(pwnam[6])[1]
            if program == shell or (program[0]=="-" and program[1:]==shell):
                program = "$"
            t = time.localtime(b['ut_tv'][0])
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
            location = b['ut_host']
            if location:
                location = "Host: "+location
            else:
                location = b['ut_line']
            
            #length sanitation
            username = username[:12]
            realname = realname[:22]
            program = upper(program[:10])
            login = login[:6]
            node = node[:6]
            location = location[:20]
            
            if not header:
                print "%-12s%-23s%-10s%-7s%-7s%-20s" % \
                      ("Username","Real Name","Program","Login","Node","Location")
                header = 1
        
            output.append( "%-12s%-23s%-10s%-7s%-7s%-20s" % 
                   (username,realname,program,login,node,location) )
    output.sort()
    for i in output:
        print i
    return output

def lastlogin(u, user):
    lastlogin = 0
    u.setutent()
    while 1:
        b = u.getutent_dict()
        if not b:
            break
        if b['ut_type'] in (USER_PROCESS, DEAD_PROCESS) and \
           b['ut_user'] == user and \
           b['ut_tv'][0]>lastlogin:
            lastlogin = b['ut_tv'][0]

    u = utmp.UtmpRecord(WTMP_FILE)
    while 1:
        b = u.getutent_dict()
        if not b:
            break
        if b['ut_type'] in (USER_PROCESS, DEAD_PROCESS) and \
           b['ut_user'] == user and \
           b['ut_tv'][0]>lastlogin:
            lastlogin = b['ut_tv'][0]
    u.endutent()
    return lastlogin

def userplan(homedir):          
    try:
        f = open(homedir+"/.plan", "r")
        print "Plan:"
        while 1:
            l = f.readline()
            if not l:
                break
            print string.rstrip(l)
    except:
        pass
    

def oneuser(u, user):
    pwent = pwd.getpwnam(user)
    print "Login name: %-28sIn real life: %s" % \
         (upper(user), getrealname(pwent[4]))
    print " Directory: %-37sUIC: [%s,%s] ([%i,%i])" % \
          (pwent[5], 
           upper(grp.getgrgid(pwent[3])[0]), upper(user),
           pwent[3], pwent[2])
    l = lastlogin(u, user)
    if not l:
        print "Never logged in."
    else:
        print "Last login:", time.strftime("%A, %d-%b-%Y %H:%M", time.localtime(l))
    print
    userplan(pwent[5])

def guessbotttime(u):
    # try to find out boot time
    boottime = os.stat("/")[ST_CTIME] #fallback
    u.setutent()
    while 1:
        b = u.getutent_dict()
        if not b:
            break
        if b['ut_type'] == BOOT_TIME:
            boottime = b['ut_tv'][0]
    return boottime


if len(sys.argv) == 2 and "@" in sys.argv[1]: # remote
    user, host = string.split(sys.argv[1], "@", 1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FINGER_PORT = 79
    s.connect( (host, FINGER_PORT) )
    s.send(user + '\r\n')
    while 1:
        buf = s.recv(1024)
        if not buf: break
        sys.stdout.write(buf)
    sys.stdout.flush()
    sys.exit(0)

un = os.uname()
ops = un[0]
node = un[1]
ver = un[2]
node = upper(node)
now = time.localtime(time.time())
a = utmp.UtmpRecord()
boottime = guessbotttime(a)

if len(sys.argv) == 1: # list of all local users
    header(now, boottime, ops, ver)
    r = userlist(a, now, node)
    if not r:
        print "No such processes."

else:
    #first find out if user exists
    user = sys.argv[1]
    try:
        pwd.getpwnam(user)
        r = userlist(a, now, node, user)
        if not r:
            print upper(user), "isn't logged in."
        print
        oneuser(a, user)
    except KeyError:
        lou = [] # list of matching users
        if len(user)>=3:
            for i in pwd.getpwall():
                rn = getrealname(i[4])
                if string.count(upper(rn), upper(user)):
                    lou.append( (i[0], rn) )
        if not lou:
            print upper(user), "does not match any user of this system."
        else:
            print 'Users who have "%s" in their real names:' % upper(user)
            for i in lou:
                print "%-13s- %s" % (upper(i[0]), i[1])
    
a.endutent()

