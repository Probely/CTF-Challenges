#include <sys/param.h>

/* a bad hack, we should dynamically allocate the array */
#ifndef MAXPATHLEN 
# define MAXPATHLEN 1024
#endif


#ifdef USE_UTMPX
# include <utmpx.h>
# define choice_utmp utmpx
#else
# include <utmp.h>
# define choice_utmp utmp
#endif

#ifndef _HAVE_UT_USER
# define ut_user ut_name
#endif

struct choice_utmp utmp_entry;

#define STRUCTSIZE ((long)sizeof(utmp_entry))

#ifndef UT_NAMESIZE
# define UT_NAMESIZE	    sizeof(utmp_entry.ut_user)
#endif

#ifndef UT_LINESIZE
# define UT_LINESIZE	    sizeof(utmp_entry.ut_line)
#endif

#ifdef _HAVE_UT_ID
# define UT_IDSIZE       sizeof(utmp_entry.ut_id)
#else
# define UT_IDSIZE       UT_LINESIZE
#endif

#ifndef UT_HOSTSIZE
# ifdef _HAVE_UT_HOST
#  define UT_HOSTSIZE	    sizeof(utmp_entry.ut_host)
# else
#  define UT_HOSTSIZE       0
# endif
#endif

#ifndef UTMP_FILE
# ifdef _PATH_UTMP /* newer BSD's */
#  define UTMP_FILE _PATH_UTMP
# else
#  define UTMP_FILE "/etc/utmp"
# endif
#endif

#ifndef WTMP_FILE
# ifdef _PATH_WTMP /* newer BSD's */
#  define WTMP_FILE _PATH_WTMP
# else
#  define WTMP_FILE "/etc/wtmp"
# endif
#endif



#ifndef _HAVE_UT_TYPE
# define EMPTY 0
# define RUN_LVL 1
# define BOOT_TIME 2
# define NEW_TIME 3
# define OLD_TIME 4
# define INIT_PROCESS 5
# define LOGIN_PROCESS 6
# define USER_PROCESS 7
# define DEAD_PROCESS 8
# define ACCOUNTING 9
# define UT_UNKNOWN EMPTY

#else

#ifndef EMPTY
# define EMPTY 0
#endif

#ifndef RUN_LVL
# define RUN_LVL EMPTY
#endif

#ifndef BOOT_TIME
# define BOOT_TIME EMPTY
#endif

#ifndef NEW_TIME
# define NEW_TIME EMPTY
#endif

#ifndef OLD_TIME
# define OLD_TIME EMPTY
#endif

#ifndef INIT_PROCESS
# define INIT_PROCESS EMPTY
#endif

#ifndef LOGIN_PROCESS
# define LOGIN_PROCESS EMPTY
#endif

#ifndef USER_PROCESS
# define USER_PROCESS EMPTY
#endif

#ifndef DEAD_PROCESS
# define DEAD_PROCESS EMPTY
#endif

#ifndef ACCOUNTING
# define ACCOUNTING EMPTY
#endif

#ifndef UT_UNKNOWN
# define UT_UNKNOWN EMPTY
#endif

#endif /* _HAVE_UT_TYPE */
