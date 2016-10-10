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


__all__ = ["DisplayText"]


class DisplayText(object):
    def __init__(self, text):
        self._text = text

    def __str__(self):
        return self._text


# vim: set expandtab ts=4 sw=4:
