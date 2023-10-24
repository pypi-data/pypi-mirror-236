"""
# simple-log
# Very simple loging library.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-simple-log/
#
"""


class Config(object):
    VERSION = 1

    def __init__(self):
        self.debug = False
        self.color = True
        self.quiet: bool = False
        self.verbose: bool = False
