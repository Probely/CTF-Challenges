#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Bright Pixel
#


from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import


import sys
import csv
import hashlib


if len(sys.argv) != 3:
    print("USAGE: %s <cleartext.csv> <hashed.csv>" % sys.argv[0], file=sys.stderr)
    sys.exit(1)

with open(sys.argv[1], "rb") as ifile:
    with open(sys.argv[2], "wb") as ofile:
        reader = csv.reader(ifile, delimiter=b",", quotechar=b"\"")
        writer = csv.writer(ofile, delimiter=b",", quotechar=b"\"", quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            row[1] = hashlib.sha1(row[1]).hexdigest()
            writer.writerow(row)


# vim: set expandtab ts=4 sw=4:
