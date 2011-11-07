##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""Registration functional tests
"""
from zope import interface
from zope.app.component.testing import AppComponentLayer
from zope.app.testing import functional
import doctest
import os.path
import unittest
import zope.app.testing.functional

AppComponentBrowserLayer = functional.ZCMLLayer(
    os.path.join(os.path.dirname(__file__), 'ftesting.zcml'),
    __name__, 'AppComponentBrowserLayer', allow_teardown=True)

class ISampleBase(interface.Interface):
    pass

class ISample(ISampleBase):
    pass

class Sample:
    interface.implements(ISample)


def test_suite():
    site = zope.app.testing.functional.FunctionalDocFileSuite(
        "site.txt",
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    site.layer = AppComponentBrowserLayer
    return unittest.TestSuite((site,))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

