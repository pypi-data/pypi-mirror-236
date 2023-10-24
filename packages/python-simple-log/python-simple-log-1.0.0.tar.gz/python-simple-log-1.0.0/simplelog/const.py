"""
# simple-log
# Very simple loging library.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-simple-log/
#
"""

from typing import List


class Const(object):
    APP_NAME: str = 'python-simple-log'
    APP_VERSION: str = '1.0.0'
    APP_URL: str = 'https://github.com/MarcinOrlowski/python-simple-log/'

    APP_DESCRIPTION: List[str] = [
        f'{APP_NAME} v{APP_VERSION} * Copyright 2023 by Marcin Orlowski.',
        'Very simple loging library.',
        f'{APP_URL}',
    ]

    class RC(object):  # noqa: WPS431
        """
        Application return codes.
        """

        OK: int = 0
        TRANSLATION_SYNTAX_ERROR = 200
