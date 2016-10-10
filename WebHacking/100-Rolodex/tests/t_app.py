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
import json
import os


TEST_USERNAME = "team0"
TEST_PASSWORD = "abcd1234-1"

# In this challenge, setting the participant's position attribute
# to "admin" (case-insensitive) gives it privileged access...
PRIVILEGED_POSITION = "admin"

# Valid employee UID...
EMPLOYEE_UID = 1001


class TestApp(unittest.TestCase):
    def setUp(self):
        r = requests.get("http://127.0.0.1:30878/token", auth=(TEST_USERNAME, TEST_PASSWORD))

        response = r.json()
        self.token = response["token"]
        self.uid = response["uid"]


    def test_failed_auth(self):
        r = requests.get("http://127.0.0.1:30878/token", auth=(TEST_USERNAME, TEST_PASSWORD + "--bad--"))
        self.assertEqual(r.status_code, 401)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertTrue("error" in response)

        r = requests.get("http://127.0.0.1:30878/token", auth=(TEST_USERNAME + "--bad--", TEST_PASSWORD))
        self.assertEqual(r.status_code, 401)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertTrue("error" in response)


    def test_empty_auth(self):
        r = requests.get("http://127.0.0.1:30878/token", auth=(TEST_USERNAME, ""))
        self.assertEqual(r.status_code, 401)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertTrue("error" in response)

        r = requests.get("http://127.0.0.1:30878/token", auth=("", TEST_PASSWORD))
        self.assertEqual(r.status_code, 401)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertTrue("error" in response)

        r = requests.get("http://127.0.0.1:30878/token", auth=("", ""))
        self.assertEqual(r.status_code, 401)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertTrue("error" in response)


    def test_invalid_auth_header(self):
        for auth in (b"", b"--garbage--", b"--áççêntèd--"):
            r = requests.get(b"http://127.0.0.1:30878/token", headers={b"Authorization": auth})
            self.assertEqual(r.status_code, 401)

            response = r.json()
            self.assertEqual(response["status"], r.status_code)
            self.assertTrue("error" in response)


    def test_successful_auth(self):
        r = requests.get("http://127.0.0.1:30878/token", auth=(TEST_USERNAME, TEST_PASSWORD))
        self.assertEqual(r.status_code, 200)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertFalse("error" in response)

        self.assertTrue("uid" in response)
        self.assertTrue("token" in response)
        self.assertEqual(len(response["token"]), 64)


    def test_missing_token(self):
        r = requests.get("http://127.0.0.1:30878/users/1")
        self.assertEqual(r.status_code, 403)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertTrue("error" in response)


    def test_failed_token_header(self):
        for token in (b"", b"--garbage--", b"--áççêntèd--"):
            r = requests.get(b"http://127.0.0.1:30878/users/1",
                             headers={b"X-API-Token": token})
            self.assertEqual(r.status_code, 403)

            response = r.json()
            self.assertEqual(response["status"], r.status_code)
            self.assertTrue("error" in response)


    def test_successful_token_header(self):
        r = requests.get(b"http://127.0.0.1:30878/users/%d" % self.uid,
                         headers={b"X-API-Token": self.token})
        self.assertEqual(r.status_code, 200)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertFalse("error" in response)


    def test_failed_token_qs(self):
        for token in (b"", b"--garbage--", b"--áççêntèd--"):
            r = requests.get(b"http://127.0.0.1:30878/users/1?token=%s" % token)
            self.assertEqual(r.status_code, 403)

            response = r.json()
            self.assertEqual(response["status"], r.status_code)
            self.assertTrue("error" in response)


    def test_successful_token_qs(self):
        r = requests.get(b"http://127.0.0.1:30878/users/%s?token=%s" % (self.uid, self.token))
        self.assertEqual(r.status_code, 200)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertFalse("error" in response)


    def test_set_participant_attributes(self):
        random_name = os.urandom(10).encode("hex")

        r = requests.put(b"http://127.0.0.1:30878/users/%d" % self.uid,
                         headers={b"X-API-Token": self.token},
                         json={"name": random_name})
        self.assertTrue(r.status_code in (200, 304))

        r = requests.get(b"http://127.0.0.1:30878/users/%s?token=%s" % (self.uid, self.token))
        self.assertEqual(r.status_code, 200)

        response = r.json()
        self.assertEqual(response["user"]["name"], random_name)


    def test_set_unknown_participant_attributes(self):
        r = requests.put(b"http://127.0.0.1:30878/users/%d" % self.uid,
                         headers={b"X-API-Token": self.token},
                         json={"whatisthisattribute": "Testing Set"})
        self.assertEqual(r.status_code, 400)


    def test_set_employee_attributes(self):
        r = requests.put(b"http://127.0.0.1:30878/users/%d" % EMPLOYEE_UID,
                         headers={b"X-API-Token": self.token},
                         json={"name": "Testing Set"})
        self.assertEqual(r.status_code, 403)  # ...cannot change employees.


    def test_get_all_users_unprivileged(self):
        r = requests.put(b"http://127.0.0.1:30878/users/%d" % self.uid,
                         headers={b"X-API-Token": self.token},
                         json={"position": "unprivileged"})
        self.assertTrue(r.status_code in (200, 304))

        r = requests.get(b"http://127.0.0.1:30878/users",
                         headers={b"X-API-Token": self.token})
        self.assertEqual(r.status_code, 200)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertFalse("error" in response)

        self.assertTrue("users" in response)
        self.assertTrue(isinstance(response["users"], list))
        self.assertTrue(len(response["users"]) > 0)

        for user in response["users"]:
            self.assertTrue("uid" in user)

            if user["uid"] != self.uid:
                self.assertFalse("notes" in user)  # ...privileged attribute.


    def test_get_user_by_uid_unprivileged(self):
        r = requests.put(b"http://127.0.0.1:30878/users/%d" % self.uid,
                         headers={b"X-API-Token": self.token},
                         json={"position": "unprivileged"})
        self.assertTrue(r.status_code in (200, 304))

        r = requests.get(b"http://127.0.0.1:30878/users/%d" % EMPLOYEE_UID,
                         headers={b"X-API-Token": self.token})
        self.assertEqual(r.status_code, 200)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertFalse("error" in response)

        self.assertTrue("user" in response)
        self.assertEqual(response["user"]["uid"], EMPLOYEE_UID)
        self.assertTrue("notes" not in response["user"])


    def test_get_all_users_privileged(self):
        r = requests.put(b"http://127.0.0.1:30878/users/%d" % self.uid,
                         headers={b"X-API-Token": self.token},
                         json={"position": PRIVILEGED_POSITION})
        self.assertTrue(r.status_code in (200, 304))

        r = requests.get(b"http://127.0.0.1:30878/users",
                         headers={b"X-API-Token": self.token})
        self.assertEqual(r.status_code, 200)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertFalse("error" in response)

        self.assertTrue("users" in response)
        self.assertTrue(isinstance(response["users"], list))
        self.assertTrue(len(response["users"]) > 0)

        for user in response["users"]:
            self.assertTrue("uid" in user)

            if user["uid"] != self.uid:
                self.assertTrue("notes" in user)  # ...privileged attribute.


    def test_get_user_by_uid_privileged(self):
        r = requests.put(b"http://127.0.0.1:30878/users/%d" % self.uid,
                         headers={b"X-API-Token": self.token},
                         json={"position": PRIVILEGED_POSITION})
        self.assertTrue(r.status_code in (200, 304))

        r = requests.get(b"http://127.0.0.1:30878/users/%d" % EMPLOYEE_UID,
                         headers={b"X-API-Token": self.token})
        self.assertEqual(r.status_code, 200)

        response = r.json()
        self.assertEqual(response["status"], r.status_code)
        self.assertFalse("error" in response)

        self.assertTrue("user" in response)
        self.assertEqual(response["user"]["uid"], EMPLOYEE_UID)
        self.assertTrue("notes" in response["user"])


if __name__ == "__main__":
    unittest.main()


# vim: set expandtab ts=4 sw=4:
