#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# P100 challenge for Pixels Camp CTF 2016
#
# Copyright (c) 2016, Bright Pixel
#


from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import sys
import os
import logging
import cPickle as pickle
import re

from getopt import getopt, GetoptError
from functools import wraps
from base64 import b64encode, b64decode

from bottle import route, request, response, run, HTTPError
from protocol import DisplayText


log = logging.getLogger("ctf-challenge")


# The text for display (the challenge flag)...
ADMIN_PASSWORD = "thisIs!the&nSwer"

# To justify returning the same string that was
# sent, the display supposedly formats the text...
DISPLAY_LENGTH = 32

# Text starts like this and returns
# to it when a team gets the flag...
DEFAULT_TEXT = "--testing--"

# The text currently being displayed...
current_text = DEFAULT_TEXT


class ExploitFilterError(Exception):
    pass


def ensure_challenge_invariant(func):
    """Ensure the challenge is kept sane on each request."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        os.environ["ADMIN_PASSWORD"] = ADMIN_PASSWORD

        global current_text
        if current_text == ADMIN_PASSWORD:
            current_text = DEFAULT_TEXT

        return func(*args, **kwargs)

    return wrapper


@route("/text", method="GET")
@ensure_challenge_invariant
def get_text():
    text = DisplayText(current_text)
    payload = b64encode(pickle.dumps(text))

    response.status = 200
    return payload


@route("/text", method="POST")
@ensure_challenge_invariant
def set_text():
    try:
        payload = b64decode(request.body.read())
        if not re.search(r"(?:[\n]DisplayText|^cos[\n]getenv)[\n]", payload):
            log.warning("Decoded payload (filtered): %s", repr(payload[:64]))
            raise ExploitFilterError("Hint: Your payload was blocked by a sanity filter. "
                                     "Either send a valid 'DisplayText' object or go after "
                                     "the flag. This is just a 100, don't overthink it.")

        text = pickle.loads(payload)

    except ExploitFilterError as e:
        log.warning("Payload was blocked by the sanity filter.")
        raise HTTPError(400, str(e))

    except Exception as e:
        log.error("Payload decoding raised a %s exception!", type(e).__name__)
        raise HTTPError(400, "invalid request")

    # Another safety-check: abort if the object looks suspicious...
    if not (isinstance(text, DisplayText) or isinstance(text, unicode)):
        log.critical("BREACH! Payload: %s", repr(payload[:64]))
        os._exit(1)

    log.info("Payload text: %s", text)
    proposed_text = str(text)[:DISPLAY_LENGTH]

    global current_text
    current_text = proposed_text

    response.status = 200
    return current_text


def print_usage():
    """Output the proper usage syntax for this program."""

    print("USAGE: %s [--listen <ip:port>] [--debug]" % os.path.basename(sys.argv[0]))


def parse_args():
    """Parse and enforce command-line arguments."""

    try:
        options, args = getopt(sys.argv[1:], "l:dh", ["listen=", "debug", "help"])
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

    format = logging.Formatter("%(asctime)s: %(levelname)s [%(process)s]: %(message)s")
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(format)
    logging.getLogger().addHandler(handler)

    log.setLevel(logging.DEBUG if debug else logging.INFO)

    run(host=listen["host"], port=listen["port"], debug=debug)


# vim: set expandtab ts=4 sw=4:
