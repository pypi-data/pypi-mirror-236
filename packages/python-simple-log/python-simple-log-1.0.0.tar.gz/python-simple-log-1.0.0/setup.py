#!/usr/bin/env python3

"""
# simple-log
# Very simple loging library.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-simple-log/
#
#
# python3 -m venv venv
# source venv/activate.fish
# pip install wheel twine
# python3 setup.py sdist bdist_wheel
# pip install --upgrade dist/simple_log-1.0.0-py3-none-any.whl
# twine upload dist/*
#
"""

from simplelog.const import Const
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    readme = fh.read()
    setup(
        name = Const.APP_NAME,
        version = Const.APP_VERSION,
        packages = find_packages(),

        install_requires = [
            'argparse>=1.4.0',
        ],
        entry_points = {
            'console_scripts': [],
        },

        author = 'Marcin Orlowski',
        author_email = 'mail@marcinOrlowski.com',
        description = 'Simple log helper library.',
        long_description = readme,
        long_description_content_type = 'text/markdown',
        url = Const.APP_URL,
        keywords = 'simple log helper library',
        project_urls = {
            'Bug Tracker':   'https://github.com/MarcinOrlowski/python-simple-log/issues/',
            'Documentation': 'https://github.com/MarcinOrlowski/python-simple-log/',
            'Source Code':   'https://github.com/MarcinOrlowski/python-simple-log/',
        },
        # https://choosealicense.com/
        license = 'MIT License',
        classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
    )
