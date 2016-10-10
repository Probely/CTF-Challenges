#include "Python.h"

#include "constants.h"


/* define out "ideal" struct utmp, based on glibc utmp */
struct myutmp {
    short ut_type;		/* type of login */
    pid_t ut_pid;		/* pid of login process */
    char ut_line[UT_LINESIZE + 1];	/* device name of tty - "/dev/" */
    char ut_id[UT_IDSIZE + 1];	/* init id or abbrev. ttyname */
    char ut_user[UT_NAMESIZE + 1];	/* user name */
    char ut_host[UT_HOSTSIZE + 1];	/* hostname for remote login */
    short int e_termination;	/* process termination status.  */
    short int e_exit;		/* process exit status.  */
    long ut_session;		/* session ID, used for windowing */
    long tv_sec;		/* time entry was made.  */
    long tv_usec;
    int32_t ut_addr_v6[4];	/* IP address of remote host.  */
};


/* some helper functions */

/* return ut_type of system utmp struct, making it up if it is without one */

int checktype(s)
struct choice_utmp *s;
{
#ifdef _HAVE_UT_TYPE
    return s->ut_type;
#else
    int r;

    r = USER_PROCESS;		/* pretend everything to be of type USER_PROCESS */
    if ((s->ut_user[0] == '\0') && (s->ut_host[0] == '\0')) {
	if (s->ut_line[0] == '\0')	/* empty record */
	    r = EMPTY;
	else
	    r = DEAD_PROCESS;
    } else {
	if (!strncmp(s->ut_line, "~", UT_LINESIZE))	/* reboot or shutdown */
	    r = BOOT_TIME;
    }
    /* { and | are NOT included, because at least at my linux
       box they are entered with ut_type USER_PROCESS, which does
       not seem to be quite correct */
    return r;
#endif
}

/* return pointer to ut_id, or ut_line if it is without ut_id */
char *checkid(s)
struct choice_utmp *s;
{
#ifdef _HAVE_UT_ID
    return s->ut_id;
#else
    return s->ut_line;
#endif
}



/* copy system utmp to our ideal one, using default values
   if system utmp does not have all the fields we have
*/
void system2my(m, s)
struct myutmp *m;
struct choice_utmp *s;
{

    m->ut_type = checktype(s);

#ifdef _HAVE_UT_PID
    m->ut_pid = s->ut_pid;
#else
    m->ut_pid = 0;
#endif

    strncpy(m->ut_line, s->ut_line, UT_LINESIZE);
    strncpy(m->ut_id, checkid(s), UT_IDSIZE);
    strncpy(m->ut_user, s->ut_user, UT_NAMESIZE);

#ifdef _HAVE_UT_HOST
    strncpy(m->ut_host, s->ut_host, UT_HOSTSIZE);
#else
    m->ut_host[0] = '\0';
#endif

#ifdef _HAVE_UT_EXIT
    m->e_termination = s->ut_exit.e_termination;
    m->e_exit = s->ut_exit.e_exit;
#else
    m->e_termination = 0;
    m->e_exit = 0;
#endif

#ifdef _HAVE_UT_TV
    m->tv_sec = s->ut_tv.tv_sec;
    m->tv_usec = s->ut_tv.tv_usec;
#else
    m->tv_sec = s->ut_time;
    m->tv_usec = 0;
#endif

#ifdef _HAVE_UT_ADDR_V6
    memcpy(m->ut_addr_v6, s->ut_addr_v6, 4 * sizeof(int32_t));
#else
    memset(m->ut_addr_v6, 0, 4 * sizeof(int32_t));
#endif

#ifdef _HAVE_UT_SESSION
    m->ut_session = s->ut_session;
#else
    m->ut_session = 0;
#endif
    m->ut_line[UT_LINESIZE] = '\0';
    m->ut_user[UT_NAMESIZE] = '\0';
    m->ut_host[UT_HOSTSIZE] = '\0';
    m->ut_id[UT_IDSIZE] = '\0';
}


/* copy our ideal utmp to system one, copy only
   those fields system utmp has
*/
void my2system(s, m)
struct myutmp *m;
struct choice_utmp *s;
{

#ifdef _HAVE_UT_HOST
    strncpy(s->ut_host, m->ut_host, UT_HOSTSIZE);
#endif

    strncpy(s->ut_user, m->ut_user, UT_NAMESIZE);


#ifdef _HAVE_UT_TYPE
    s->ut_type = m->ut_type;
#else
    if ((m->ut_type != USER_PROCESS) && (m->ut_type == BOOT_TIME)) {
	memset(s->ut_user, 0, UT_NAMESIZE);
# ifdef _HAVE_UT_HOST
	memset(s->ut_host, 0, UT_HOSTSIZE);
# endif
    }
#endif

#ifdef _HAVE_UT_PID
    s->ut_pid = m->ut_pid;
#endif


#ifdef _HAVE_UT_ID
    strncpy(checkid(s), m->ut_id, UT_IDSIZE);
#endif

    strncpy(s->ut_line, m->ut_line, UT_LINESIZE);

#ifdef _HAVE_UT_EXIT
    s->ut_exit.e_termination = m->e_termination;
    s->ut_exit.e_exit = m->e_exit;
#endif

#ifdef _HAVE_UT_TV
    s->ut_tv.tv_sec = m->tv_sec;
    s->ut_tv.tv_usec = m->tv_usec;
#else
    s->ut_time = m->tv_sec;
#endif

#ifdef _HAVE_UT_ADDR_V6
    memcpy(s->ut_addr_v6, m->ut_addr_v6, 4 * sizeof(int32_t));
#endif

#ifdef _HAVE_UT_SESSION
    s->ut_session = m->ut_session;
#endif
}


#define OUTVALUE(entry) \
                "(hlssss(hh)l(ll)(llll))", \
                entry->ut_type, \
                (long)(entry->ut_pid), \
                entry->ut_line, \
                entry->ut_id, \
                entry->ut_user, \
                entry->ut_host, \
                entry->e_termination, \
                entry->e_exit, \
                entry->ut_session, \
                entry->tv_sec, \
                entry->tv_usec, \
                (long)(entry->ut_addr_v6[0]), \
                (long)(entry->ut_addr_v6[1]), \
                (long)(entry->ut_addr_v6[2]), \
                (long)(entry->ut_addr_v6[3])


#ifndef _HAVE_SETUTENT
static char _utmpfilename[MAXPATHLEN] = UTMP_FILE;
static long _offset = 0;
static struct choice_utmp _utmprec;
#endif

#ifndef _HAVE_UTMPNAME
void my_utmpname(name)
char *name;
{
    strncpy(_utmpfilename, name, sizeof(_utmpfilename));
}
#else
# ifdef USE_UTMPX
#  define my_utmpname utmpxname
# else
#  define my_utmpname utmpname
# endif
#endif


static PyObject *utmp_utmpname(self, args)
PyObject *self;
PyObject *args;
{
    char *fname;

    if (!PyArg_ParseTuple(args, "s", &fname))
	return NULL;
    my_utmpname(fname);
    Py_INCREF(Py_None);
    return Py_None;
}


#ifndef _HAVE_SETUTENT
void my_setutent(void)
{
    _offset = 0;
}
#else
# ifdef USE_UTMPX
#  define my_setutent setutxent
# else
#  define my_setutent setutent
# endif
#endif


static PyObject *utmp_setutent(self, args)
PyObject *self;
PyObject *args;
{
    if (!PyArg_ParseTuple(args, ""))
	return NULL;
    my_setutent();
    Py_INCREF(Py_None);
    return Py_None;
}


#ifndef _HAVE_GETUTENT
struct choice_utmp *my_getutent()
{
    FILE *f;
    size_t l;
    int r;

    f = fopen(_utmpfilename, "rb");
    if (f == NULL) {
	PyErr_SetFromErrno(PyExc_IOError);
	return NULL;
    }
    r = fseek(f, (long) _offset * STRUCTSIZE, SEEK_SET);
    if (r == -1) {
	return NULL;
    }
    _offset++;			/* now it points _after_ the record just read */
    l = fread(&_utmprec, STRUCTSIZE, 1, f);
    fclose(f);
    if (l == 1)
	return &_utmprec;
    else
	return NULL;
}
#else
# ifdef USE_UTMPX
#  define my_getutent getutxent
# else
#  define my_getutent getutent
# endif
#endif


static PyObject *utmp_getutent(self, args)
PyObject *self;
PyObject *args;
{
    struct choice_utmp *entry;
    struct myutmp myentry;

    if (!PyArg_ParseTuple(args, ""))
	return NULL;
    entry = my_getutent();

    if (!entry) {
	Py_INCREF(Py_None);
	return Py_None;
    };
    system2my(&myentry, entry);

    return Py_BuildValue(OUTVALUE((&myentry)));
}


#ifndef _HAVE_GETUTID
struct choice_utmp *my_getutid(u)
struct choice_utmp *u;
{
    int t;
    struct choice_utmp *a;

    t = checktype(u);

    if ((t == RUN_LVL) || (t == BOOT_TIME) || (t == NEW_TIME)
	|| (t == OLD_TIME))
	while ((a = my_getutent())) {
	    if (t == checktype(a))
		return a;
    } else if ((t == INIT_PROCESS) || (t == LOGIN_PROCESS)
	       || (t == USER_PROCESS) || (t == DEAD_PROCESS))
	while ((a = my_getutent())) {
	    if (!strncmp(checkid(a), checkid(u), UT_IDSIZE))
		return a;
	}
    return NULL;
}
#else
# ifdef USE_UTMPX
#  define my_getutid getutxid
# else
#  define my_getutid getutid
# endif
#endif


static PyObject *utmp_getutid(self, args)
    /* args are ut_type[, ut_id] */
PyObject *self;
PyObject *args;
{
    struct myutmp myentry;
    struct choice_utmp entry;
    struct choice_utmp *nentry;
    struct myutmp mynentry;
    short ut_type;
    char *ut_id = "";


    if (!PyArg_ParseTuple(args, "h|s", &ut_type, &ut_id))
	return NULL;

    myentry.ut_type = ut_type;
    strncpy(myentry.ut_id, ut_id, UT_IDSIZE);
    my2system(&entry, &myentry);
    nentry = my_getutid(&entry);

    if (!nentry) {
	Py_INCREF(Py_None);
	return Py_None;
    };

    system2my(&mynentry, nentry);
    return Py_BuildValue(OUTVALUE((&mynentry)));
}


#ifndef _HAVE_GETUTLINE
struct choice_utmp *my_getutline(u)
struct choice_utmp *u;
{
    struct choice_utmp *a;
    int t;

    while ((a = my_getutent())) {
	t = checktype(a);
	if (((t == USER_PROCESS) || (t == LOGIN_PROCESS)) &&
	    (!strncmp(a->ut_line, u->ut_line, UT_LINESIZE)))
	    return a;
    }
    return NULL;
}
#else
# ifdef USE_UTMPX
#  define my_getutline getutxline
# else
#  define my_getutline getutline
# endif
#endif


static PyObject *utmp_getutline(self, args)
    /* args is ut_line */
PyObject *self;
PyObject *args;
{
    struct choice_utmp entry;
    struct choice_utmp *nentry;
    struct myutmp mynentry;
    char *ut_line;


    if (!PyArg_ParseTuple(args, "s", &ut_line))
	return NULL;

    strncpy(entry.ut_line, ut_line, UT_LINESIZE);
    nentry = my_getutline(&entry);

    if (!nentry) {
	Py_INCREF(Py_None);
	return Py_None;
    };

    system2my(&mynentry, nentry);
    return Py_BuildValue(OUTVALUE((&mynentry)));
}

#ifndef _HAVE_PUTUTLINE
void my_pututline(u)
struct choice_utmp *u;
{
    struct choice_utmp *a;
    FILE *f;
    int r;

    _offset--;			/* if we are at the correct line, offset points after it */
    a = my_getutid(u);
    if (!a) {
	f = fopen(_utmpfilename, "ab");
	if (f == NULL) {
/*	  PyErr_SetFromErrno (PyExc_IOError);*/
	    return;
	}
	fwrite(u, STRUCTSIZE, 1, f);
	fclose(f);
    } else {
	f = fopen(_utmpfilename, "r+b");
	if (f == NULL) {
/*	  PyErr_SetFromErrno (PyExc_IOError);*/
	    return;
	}
	_offset--;
	if (_offset < 0) {
	    PyErr_SetFromErrno(PyExc_IOError);
	    return;
	}
	r = fseek(f, (long) _offset * STRUCTSIZE, SEEK_SET);
	if (r == -1) {		/* something went wrong */
	    PyErr_SetFromErrno(PyExc_IOError);
	    return;
	}
	fwrite(u, STRUCTSIZE, 1, f);
	fclose(f);
    }
}
#else
# ifdef USE_UTMPX
#  define my_pututline pututxline
# else
#  define my_pututline pututline
# endif
#endif


static PyObject *utmp_pututline(self, args)
PyObject *self;
PyObject *args;
{
    struct choice_utmp entry;
    struct myutmp myentry;
    char *ut_line, *ut_id, *ut_user, *ut_host;
    long ut_addr_v6[4];		/* what if we are on platform where sizeof(int)=16 (minix?) ? */
    /* let's play it safe */

    long ut_pid;		/* we have to cheat here because sizeof(pid_t) is unknown */
    /* just hope it is not more than sizeof(long) */
    unsigned short int i;

    if (!PyArg_ParseTuple(args, "hlssss(hh)l(ll)(llll)",
			  &myentry.ut_type, &ut_pid,
			  &ut_line, &ut_id, &ut_user, &ut_host,
			  &myentry.e_termination, &myentry.e_exit,
			  &myentry.ut_session, &myentry.tv_sec,
			  &myentry.tv_usec, &ut_addr_v6[0],
			  &ut_addr_v6[1], &ut_addr_v6[2], &ut_addr_v6[3]))
	return NULL;

    myentry.ut_pid = (pid_t) ut_pid;

    for (i = 0; i < 4; i++)
	myentry.ut_addr_v6[i] = (int32_t) ut_addr_v6[i];

    strncpy(myentry.ut_line, ut_line, UT_LINESIZE);
    strncpy(myentry.ut_id, ut_id, UT_IDSIZE);
    strncpy(myentry.ut_user, ut_user, UT_NAMESIZE);
    strncpy(myentry.ut_host, ut_host, UT_HOSTSIZE);

    my2system(&entry, &myentry);
    my_pututline(&entry);

    Py_INCREF(Py_None);
    return Py_None;
}


#ifndef _HAVE_ENDUTENT
void my_endutent()
{
}
#else
# ifdef USE_UTMPX
#  define my_endutent endutxent
# else
#  define my_endutent endutent
# endif
#endif


static PyObject *utmp_endutent(self, args)
PyObject *self;
PyObject *args;
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;
    my_endutent();
    Py_INCREF(Py_None);
    return Py_None;
}


static PyMethodDef UtmpMethods[] = {
    {"utmpname",  utmp_utmpname,  METH_VARARGS},
    {"setutent",  utmp_setutent,  METH_VARARGS},
    {"getutent",  utmp_getutent,  METH_VARARGS},
    {"endutent",  utmp_endutent,  METH_VARARGS},
    {"getutid",   utmp_getutid,   METH_VARARGS},
    {"getutline", utmp_getutline, METH_VARARGS},
    {"pututline", utmp_pututline, METH_VARARGS},
    {NULL, NULL}		/* Sentinel */
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef utmpaccessmodule = {
   PyModuleDef_HEAD_INIT,
   "utmpaccess",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   UtmpMethods
};

PyMODINIT_FUNC
PyInit_utmpaccess(void)
{
    return PyModule_Create(&utmpaccessmodule);
}

#else

void initutmpaccess()
{
    (void) Py_InitModule("utmpaccess", UtmpMethods);
}
#endif 


