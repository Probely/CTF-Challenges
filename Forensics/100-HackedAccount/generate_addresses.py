#!/usr/bin/env python

import sys
import os.path
import ipaddr

if len(sys.argv) != 2:
    print("USAGE: %s <subnets.txt>" % os.path.basename(sys.argv[0]))
    sys.exit(1)

for line in open(sys.argv[1], 'r'):
    netw = ipaddr.IPv4Network(line.rstrip())
    for ip in netw.iterhosts():
        print ip
