#!/usr/bin/env python
""" Generate a bunch of new/random entries

Module "utmp" provides class UtmpEntry, correcponding to one
entry in UTMP/WTMP file.
UtmpEntry has the following attributes (values after "=" demonstrate default values)

ut_type = EMPTY
ut_pid = 0
ut_line = ''
ut_id = ''
ut_user = ''
ut_host = ''
ut_exit = (0, 0)
ut_session = 0
ut_tv = (0, 0)
ut_addr_v6 = (0, 0, 0, 0)

"""

#
# This code is definitely not beautiful, beware!
#

import utmp
import GeoIP
from random import randrange, choice

# Configuration values
FILENAME = "wtmp.new"
LINE_LIST = ['pts/0', 'pts/1', 'pts/2', 'pts/3', 'pts/4', 'pts/5']
TTY_LIST = ['ts/0', 'ts/1', 'ts/2', 'ts/3', 'ts/4', 'ts/5']
IP_FILE = 'addresses.txt'
USER_FILE = 'usernames.txt'
BOGUS_USER = "pjsmith"
BOGUS_IPS = ['76.192.3.2', '217.77.163.138']
BOGUS_ENTRY_INDEX = 1580
NR_ENTRIES = 2000
TIME_RANDOM_INTERVAL = 200
USER_PROCESS = 7

MAX_RED_HERRINGS = 3
SAFE_RED_HERRING_INTERVAL = 100800  # enough time to travel to another country

open(FILENAME, "w").close()  # truncate the file :/
NEW_RECORD = utmp.UtmpRecord(FILENAME)

# T0
timestamp = 1470587713

time_window = 128835
bad_ip = 0
users = []
ips = []

geoip = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
country_per_user = {}
last_seen = {}  # keyed by user
red_herrings = 0


def create_users():
    # Read usernames file and create users list
    with open(USER_FILE, 'r') as f:
        global users
        users = [u.strip().lower() for u in f]


def create_ips():
    # Read ips file and create ips list
    with open(IP_FILE, 'r') as f:
        global ips
        ips = [ip.strip() for ip in f]


def get_random_line():
    return choice(LINE_LIST)


def get_random_tty():
    return choice(TTY_LIST)


def get_random_pid():
    return randrange(1024, 65535)


def get_random_user():
    return choice(users)[:8]


def get_random_ip(user, login_timestamp):
    """Return an IP for the user, ensuring it's always in the same country."""

    if user not in country_per_user:
        ip = choice(ips)
        cc = geoip.country_code_by_addr(ip)
        country_per_user[user] = cc
    else:
        while True:
            ip = choice(ips)
            cc = geoip.country_code_by_addr(ip)

            global red_herrings

            if (red_herrings < MAX_RED_HERRINGS and
                last_seen.get(user, 0) < login_timestamp - SAFE_RED_HERRING_INTERVAL):
                if cc != country_per_user[user]:
                    red_herrings += 1

                break

            if cc == country_per_user[user]:
                break

    last_seen[user] = login_timestamp
    return ip


# ------


create_users()
create_ips()

print("Bad user is: %s" % BOGUS_USER)


for entry in xrange(NR_ENTRIES):
    timestamp += randrange(TIME_RANDOM_INTERVAL)
    rand_line = randrange(len(TTY_LIST))

    if (entry != BOGUS_ENTRY_INDEX):
        user = get_random_user()
        NEW_RECORD.pututline(ut_type=USER_PROCESS, ut_pid=get_random_pid(),
                             ut_line=LINE_LIST[rand_line], ut_id=TTY_LIST[rand_line],
                             ut_user=user, ut_host=get_random_ip(user, timestamp),
                             ut_tv=(timestamp, randrange(10, time_window)))
    elif ((entry == BOGUS_ENTRY_INDEX) and (bad_ip < len(BOGUS_IPS))):
        NEW_RECORD.pututline(ut_type=USER_PROCESS, ut_pid=get_random_pid(),
                             ut_line=LINE_LIST[rand_line], ut_id=TTY_LIST[rand_line],
                             ut_user=BOGUS_USER, ut_host=BOGUS_IPS[bad_ip],
                             ut_tv=(timestamp, randrange(10, time_window)))
        BOGUS_ENTRY_INDEX += 12
        bad_ip += 1
        #print entry
