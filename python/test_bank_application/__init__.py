#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Arjun Prasad Namdeo"
__email__ = "arjun.namdeo.vfx@gmail.com"

"""
keeping this file to give access to the package directory

Also If you want to add some requirements for the project. This is the module
you should use. 
"""


# setting PYTHONDONTWRITEBYTECODE env variable so
# the program execution do not generate pyc files
# read more about it in here
# http://stackoverflow.com/questions/37669883/disabling-pyc-files-in-production
import sys
sys.dont_write_bytecode=True

print "hello"