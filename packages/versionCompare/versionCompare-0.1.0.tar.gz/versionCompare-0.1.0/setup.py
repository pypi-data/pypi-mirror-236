# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# This call to setup() does all the work
setup(
    name="versionCompare",
    version="0.1.0",
    description="A library to check if a number is greater, equal or less than the other.",
    long_description_content_type="text/markdown",
    author="Keyur Patel",
    author_email="kj8patel@uwaterloo.ca",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["versionCompare"],
    include_package_data=True
)
