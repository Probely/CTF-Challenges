#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# P200 challenge for Pixels Camp CTF 2016
#
# Copyright (c) 2016, Bright Pixel
#

from __future__ import print_function

import sys
import os
import logging

from getopt import getopt, GetoptError
from functools import wraps

from bottle import route, request, response, \
                   run, parse_auth, HTTPError


import authentication
import settings

log = logging.getLogger("ctf-challenge")

valid_users = frozenset((
    'admin',
    'user',
))


def ensure_valid_token(func):
    """
    Decorator for routes that require a valid access token.

    The token is passed as the first parameter to the decorated
    function along with an additional "privileged" flag passed as
    a keyword argument, indicating the level of access required.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Token in headers overrides token in query string for safety...
        token = request.headers.get("X-API-Token") or request.GET.get("token")

        user = authentication.verify_token(token)
        if user is None:
            response.status = 401
            return {"status": 401, "error": "bad access token"}
        if user not in valid_users:
            response.status = 403
            # msg = {"status": 403, "error": "%r user is not valid" % user}
            msg = {"status": 403, "error": "user is not valid"}
            return msg

        privileged = user == "admin"
        kwargs["privileged"] = privileged

        if privileged:
            log.info("Privileged call for user \"%s\".", user)

        return func(*args, **kwargs)

    return wrapper


@route("/token", method="GET")
def get_token():
    token = authentication.generate_token('user')
    response.status = 200
    return {
        "status": 200,
        "token": token,
    }


@route("/flag", method="GET")
@ensure_valid_token
def get_flag(privileged=False):

    if not privileged:
        response.status = 403
        return {"status": 403, "error": "user does not have admin privileges."}

    response.status = 200
    return {"status": 200, "flag": settings.FLAG,
            "data": "Your kung fu is strong!"}


@route("/", method="GET")
def get_root():
    msg = """The following endpoints are available:

/token - generate a user token
/flag  - get the flag for this challenge


You must provide a valid token to read the flag. Either through:
    * The "token" query string parameter
    * The "X-API-Token" header

"""
    response.status = 200
    response.headers["content-type"] = "text/plain"
    return msg


def print_usage():
    """Output the proper usage syntax for this program."""

    print("USAGE: %s sv> [--listen <ip:port>] [--debug]" %
        os.path.basename(sys.argv[0]))


def parse_args():
    """Parse and enforce command-line arguments."""

    try:
        options, _ = getopt(sys.argv[1:], "l:dh",
                            ["listen=", "debug", "help"])
    except GetoptError as e:
        print("error: %s." % e, file=sys.stderr)
        print_usage()
        sys.exit(1)

    listen = {"host": "127.0.0.1", "port": "8080"}
    debug = False

    for option, value in options:
        if option in ("-h", "--help"):
            print_usage()
            sys.exit(0)
        elif option in ("-l", "--listen"):
            fields = value.split(":")
            listen = {"host": fields[0].strip(),
                      "port": int(fields[1]) if len(fields) > 1 else "8080"}
        elif option in ("-d", "--debug"):
            debug = True

    return (listen, debug)


if __name__ == "__main__":
    listen, debug = parse_args()

    fmt = logging.Formatter("%(asctime)s: %(levelname)s [%(process)s]: %(message)s")
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(fmt)
    logging.getLogger().addHandler(handler)

    log.setLevel(logging.DEBUG if debug else logging.INFO)
    run(host=listen["host"], port=listen["port"], debug=debug)


# vim: set expandtab ts=4 sw=4:
