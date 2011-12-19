import sys

from setuptools import setup, find_packages

setup(
    name = "untracked",
    version = '11.12',
    description = "Updates your Gondor config to include multiple files in a directory easily.",
    url = "https://github.com/pizzapanther/Gondor-Untracked-Files",
    author = "Paul Bailey",
    author_email = "paul.m.bailey@gmail.com",
    license = "BSD",
    packages = ['untracked'],
    entry_points = {
        "console_scripts": [
            "untracked = untracked.__main__:main",
        ],
    },
)