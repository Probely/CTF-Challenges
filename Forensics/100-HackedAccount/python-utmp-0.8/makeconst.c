#include <time.h>
#include <stdio.h>

#include "constants.h"

#define PRL(s) printf(#s" = %i\n", s);

#define PRLS(s) printf(#s" = \"%s\"\n", s);


int main(void)
{
    PRL(EMPTY);
    PRL(RUN_LVL);
    PRL(BOOT_TIME);
    PRL(NEW_TIME);
    PRL(OLD_TIME);
    PRL(INIT_PROCESS);
    PRL(LOGIN_PROCESS);
    PRL(USER_PROCESS);
    PRL(DEAD_PROCESS);
    PRL(ACCOUNTING);
    PRL(UT_UNKNOWN);
    printf("\n");
    PRL(UT_LINESIZE);
    PRL(UT_NAMESIZE);
    PRL(UT_HOSTSIZE);
    PRL(UT_IDSIZE);
    printf("\n");
    PRLS(UTMP_FILE);
    PRLS(WTMP_FILE);
    return 0;
}
