##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Binding Tests

$Id: test_binding.py 116904 2010-09-25 13:20:53Z icemac $
"""
import unittest

from zope.component import provideAdapter
from zope.component.testing import PlacelessSetup
from zope.container.interfaces import ISimpleReadContainer
from zope.container.traversal import ContainerTraversable
from zope.traversing.interfaces import ITraversable

from zope.app.pagetemplate.tests.testpackage.content import Content
from zope.app.pagetemplate.tests.testpackage.content import PTComponent

def setUpTraversal():
    from zope.traversing.testing import setUp
    setUp()
    provideAdapter(ContainerTraversable, (ISimpleReadContainer,), ITraversable)


class BindingTestCase(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(BindingTestCase, self).setUp()
        setUpTraversal()

    def test_binding(self):
        from zope.publisher.browser import TestRequest
        comp = PTComponent(Content(), TestRequest())
        self.assertEqual(comp.index(), "42\n")
        self.assertEqual(comp.nothing(), "\n")
        self.assertEqual(comp.default(), "42\n")

def test_suite():
    return unittest.makeSuite(BindingTestCase)

if __name__=='__main__':
    unittest.main()
