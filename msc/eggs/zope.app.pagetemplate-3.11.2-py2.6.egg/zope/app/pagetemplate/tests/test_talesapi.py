##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tales API Tests

$Id: test_talesapi.py 116904 2010-09-25 13:20:53Z icemac $
"""
from datetime import datetime
from doctest import DocTestSuite
from zope.interface import implements
from zope.size.interfaces import ISized
from zope.traversing.interfaces import IPhysicallyLocatable
from zope.dublincore.interfaces import IZopeDublinCore

from zope.app.pagetemplate.talesapi import ZopeTalesAPI

class TestObject(object):

    implements(IZopeDublinCore, # not really, but who's checking. ;)
               IPhysicallyLocatable, # not really
               ISized)

    description = u"This object stores some number of apples"
    title = u"apple cart"
    created = datetime(2000, 10, 1, 23, 11, 00)
    modified = datetime(2003, 1, 2, 3, 4, 5)

    def sizeForSorting(self):
        return u'apples', 5

    def sizeForDisplay(self):
        return u'5 apples'

    def getName(self):
        return u'apples'

testObject = TestObject()

def title():
    """
    >>> api = ZopeTalesAPI(testObject)
    >>> api.title
    u'apple cart'
    """

def description():
    """
    >>> api = ZopeTalesAPI(testObject)
    >>> api.description
    u'This object stores some number of apples'
    """

def name():
    """
    >>> api = ZopeTalesAPI(testObject)
    >>> api.name()
    u'apples'
    """

def title_or_name():
    """
    >>> api = ZopeTalesAPI(testObject)
    >>> api.title_or_name()
    u'apple cart'

    >>> testObject = TestObject()
    >>> testObject.title = u""
    >>> api = ZopeTalesAPI(testObject)
    >>> api.title_or_name()
    u'apples'
    """

def size():
    """
    >>> api = ZopeTalesAPI(testObject)
    >>> api.size()
    u'5 apples'
    """

def modified():
    """
    >>> api = ZopeTalesAPI(testObject)
    >>> api.modified
    datetime.datetime(2003, 1, 2, 3, 4, 5)
    """

def created():
    """
    >>> api = ZopeTalesAPI(testObject)
    >>> api.created
    datetime.datetime(2000, 10, 1, 23, 11)
    """


def test_suite():
    return DocTestSuite()
