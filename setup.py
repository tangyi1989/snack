import os
import setuptools
import sys


def read_file(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setuptools.setup(
    name="snack",
    version="2012.12",
    author="Alex, Tang",
    description="A demo dashboard use tornado.",
    packages=setuptools.find_packages(exclude=['bin', 'tests'])
)