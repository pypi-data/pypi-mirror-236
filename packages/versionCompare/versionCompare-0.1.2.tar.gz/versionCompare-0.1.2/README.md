Laguage: Python

Function: Library

Name: versionCompare

Latest Version of the library: https://pypi.org/project/versionCompare/0.1.1/

A python library that takes 2 strings of versions as input and then checks if one is greater, equal or less than the other. Example output; 1.2 > 1.1, 1.1.0 < 1.1.2

Usage

Import versionComparison from class versionComparison

Create an instance of versionComparison and supply it with the 2 strings as expected in its constructor.

Call compare_versions on the instance, and it will give appropriate result.
-> 1 if version1 > version2
-> 0 if version1 == version2
-> -1 if version1 < version2
