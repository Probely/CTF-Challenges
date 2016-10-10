#!/usr/bin/env python

import time
import sys

import pyutmp
import GeoIP

geoip = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
last_country = {}
last_seen = {}  # keyed by user

if len(sys.argv) <= 1:
    print("usage: %s <filename>" % sys.argv[0])
    sys.exit(0)

print("Suspicious logins:")
print("------------------")

for entry in pyutmp.UtmpFile(sys.argv[1]):
    if not entry.ut_user_process:
        continue

    ut_country = geoip.country_code_by_addr(entry.ut_host) or '-'

    if ut_country != last_country.get(entry.ut_user, ut_country):
        # different country: inspect manually
        print("%-10s %-16s %-3s %-25s [last: %s, %s]" % (
              entry.ut_user, entry.ut_host, ut_country,
              time.ctime(entry.ut_time), time.ctime(last_seen[entry.ut_user]),
              last_country[entry.ut_user]))

    last_country[entry.ut_user] = ut_country
    last_seen[entry.ut_user] = entry.ut_time
