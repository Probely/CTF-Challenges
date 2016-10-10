#!/usr/bin/python
# dump utmp 

import utmp
from UTMPCONST import *

a = utmp.UtmpRecord()


for b in a:
    print(b)

