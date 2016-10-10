import utmpaccess
from UTMPCONST import *

import types

class UtmpEntry:
    def __init__(self, *arg, **dictarg):
        self.clear()
        if len(arg)==1:
            arg = arg[0]
        if (type(arg)==tuple or type(arg)==list) and arg:
            self.ut_type, self.ut_pid, self.ut_line, \
            self.ut_id, self.ut_user, self.ut_host, \
            self.ut_exit, self.ut_session, self.ut_tv, \
            self.ut_addr_v6 = arg
        elif type(arg)==dict:
            for i in arg.keys():
                self[i] = arg[i]
        elif type(arg)==types.InstanceType:
            self.ut_type, self.ut_pid, self.ut_line, \
            self.ut_id, self.ut_user, self.ut_host, \
            self.ut_exit, self.ut_session, self.ut_tv, \
            self.ut_addr_v6 = arg.ut_type, arg.ut_pid, arg.ut_line, \
            arg.ut_id, arg.ut_user, arg.ut_host, \
            arg.ut_exit, arg.ut_session, arg.ut_tv, \
            arg.ut_addr_v6
        for i in dictarg.keys():
            self[i] = dictarg[i]

    def clear(self):
            self.ut_type = EMPTY
            self.ut_pid = 0
            self.ut_line = ''
            self.ut_id = ''
            self.ut_user = ''
            self.ut_host = ''
            self.ut_exit = (0, 0)
            self.ut_session = 0
            self.ut_tv = (0, 0)
            self.ut_addr_v6 = (0, 0, 0, 0)

    def _as_tuple(self):
        return (self.ut_type, self.ut_pid, self.ut_line, \
            self.ut_id, self.ut_user, self.ut_host, \
            self.ut_exit, self.ut_session, self.ut_tv, \
            self.ut_addr_v6)

    def __getitem__(self, item):
        if item=='ut_type' or item==0:
            return self.ut_type
        elif item=='ut_pid' or item==1:
            return self.ut_pid
        elif item=='ut_line' or item==2:
            return self.ut_line
        elif item=='ut_id' or item==3:
            return self.ut_id
        elif item=='ut_user' or item==4:
            return self.ut_user
        elif item=='ut_host' or item==5:
            return self.ut_host
        elif item=='ut_exit' or item==6:
            return self.ut_exit
        elif item=='ut_session' or item==7:
            return self.ut_session
        elif item=='ut_tv' or item==8:
            return self.ut_tv
        elif item=='ut_addr_v6' or item==9:
            return self.ut_addr_v6
        else:
            raise IndexError("Bad key used to access UtmpEntry: "+repr(item))

    def __setitem__(self, item, val):
        if item=='ut_type' or item==0:
            self.ut_type=val
        elif item=='ut_pid' or item==1:
            self.ut_pid=val
        elif item=='ut_line' or item==2:
            self.ut_line=val
        elif item=='ut_id' or item==3:
            self.ut_id=val
        elif item=='ut_user' or item==4:
            self.ut_user=val
        elif item=='ut_host' or item==5:
            self.ut_host=val
        elif item=='ut_exit' or item==6:
            self.ut_exit=val
        elif item=='ut_session' or item==7:
            self.ut_session=val
        elif item=='ut_tv' or item==8:
            self.ut_tv=val
        elif item=='ut_addr_v6' or item==9:
            self.ut_addr_v6=val
        else:
            raise IndexError("Bad key used to access UtmpEntry: "+repr(item))

    def __repr__(self):
        fs = []
        for key in 'ut_type', 'ut_pid', 'ut_line', \
                   'ut_id', 'ut_user', 'ut_host', \
                   'ut_exit', 'ut_session', 'ut_tv', \
                   'ut_addr_v6':
            fs.append( key+'='+repr(self[key]) )
        fs = ', '.join(fs)
        r = fs
        r = 'utmp.UtmpEntry( %s )' % fs
        return r

class UtmpRecord:

    def __init__(self, fname=None):
        if fname:
            utmpaccess.utmpname(fname)
        self.fname = fname
        self.setutent()

    def _makeclass(self, a):
        if not a:
            return None
        return UtmpEntry(a)

    def setutent(self):
        "rewinds the file pointer to the beginning of the utmp file."
        utmpaccess.setutent()

    def endutent(self):
        "closes the utmp file."
        utmpaccess.endutent()

    def getutent(self):
        """reads a line from the current file position in the utmp file. It returns an
        UtmpEntry instance corresponding to a given line."""
        return self._makeclass(utmpaccess.getutent())

    def __iter__(self):
        return self

    def __next__(self):
        r = self.getutent()
        if not r:
            raise StopIteration
        return r

    next = __next__

    def pututline(self, *ut, **dictut):
        """writes the UtmpEntry provided as parameter into the utmp file. It uses getutid() to search
        for the proper place in the file to insert the new entry. If it cannot find an
        appropriate slot for ut, pututline() will append the new entry to the end of the file."""
        if len(ut) == 1:  # one tuple passed as argument
            u=ut[0]
        else:
            u = ut
        u = UtmpEntry(u, **dictut)
        utmpaccess.pututline(*u._as_tuple())

    def getutid(self, ut_type, ut_id=''):
        """searches forward from the current file position in the utmp
        file based upon ut_type. If ut_type is RUN_LVL,  BOOT_TIME, 
        NEW_TIME, or OLD_TIME, getutid() will find the first entry whose
        ut_type field matches ut_type argument. If ut_type is one of
        INIT_PROCESS, LOGIN_PROCESS, USER_PROCESS, or DEAD_PROCESS,
        getutid() will find the first entry whose ut_id field matches
        ut_id argument."""
        return self._makeclass(utmpaccess.getutid(ut_type, ut_id))

    def getutline(self, ut_line):
        """searches forward from the current file position in the
        utmp file. It scans entries whose ut_type is USER_PROCESS or
        LOGIN_PROCESS and returns the first one whose ut_line field matches 
        ut_lie argument."""
        return self._makeclass(utmpaccess.getutline(ut_line))

    getutent_dict = getutent
    pututline_dict = pututline
    getutid_dict = getutid
    getutline_dict = getutline

    def __del__(self):
        self.endutent()

    def __repr__(self):
        if not self.fname:
            fname = ''
        return 'utmp.UtmpRecord(%s)' % fname
