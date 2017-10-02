#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# W200/C4 challenge for Pixels Camp Quals 2017
#

from __future__ import print_function

import sys
import os
import logging

from getopt import getopt, GetoptError

from bottle import get, response, error, run
from pymongo import MongoClient
import json

import settings

log = logging.getLogger("ctf-challenge")

client = MongoClient("mongodb://127.0.0.1:27017")
db = client[settings.MONGO_DB]


@error(404)
def error404(error):
    response.headers["content-type"] = "text/plain"
    return "There doesn't seem to be anything here"


@get('/')
def root():
    response.headers["content-type"] = "text/plain"
    reply = "Hello"
    return reply


@get('/user')
@get('/user/')
def user():
    response.headers["content-type"] = "text/plain"

    response.status = 404
    reply = "Please specify a user using /user/<username>"

    return reply


@get('/user/<username>')
def user_details(username):
    response.headers["content-type"] = "text/plain"
    log.debug(username)

    isJson = True
    try:
        username_json = json.loads(username)
    except ValueError:
        isJson = False

    try:
        if isJson:
            username = username_json
    except AttributeError:
        log.debug("invalid json")

    data = db.user.find({"user": username})

    reply = ""
    if data.count() == 0:
        response.status = 404
        reply = "Query returned no results"
    else:
        for row in data:
            log.debug(row)
            reply += row["user"] + "," + row["pass"] + "\n"
    return reply


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

    listen = {"host": "127.0.0.1", "port": settings.LISTEN}
    debug = False

    for option, value in options:
        if option in ("-h", "--help"):
            print_usage()
            sys.exit(0)
        elif option in ("-l", "--listen"):
            fields = value.split(":")
            listen = {"host": fields[0].strip(),
                      "port": int(fields[1]) if len(fields) > 1 else settings.LISTEN}
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
