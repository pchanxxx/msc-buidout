##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Unit tests for SkinsTool module.

$Id: test_SkinsTool.py 110577 2010-04-07 06:33:17Z jens $
"""

import unittest
import Testing

from zope.interface.verify import verifyClass
from zope.testing.cleanup import cleanUp


class SkinsContainerTests(unittest.TestCase):

    def test_interfaces(self):
        from Products.CMFCore.interfaces import ISkinsContainer
        from Products.CMFCore.SkinsContainer import SkinsContainer

        verifyClass(ISkinsContainer, SkinsContainer)


class SkinsToolTests(unittest.TestCase):

    def _makeOne(self, *args, **kw):
        from Products.CMFCore.SkinsTool import SkinsTool

        return SkinsTool(*args, **kw)

    def test_interfaces(self):
        from Products.CMFCore.interfaces import IActionProvider
        from Products.CMFCore.interfaces import ISkinsContainer
        from Products.CMFCore.interfaces import ISkinsTool
        from Products.CMFCore.SkinsTool import SkinsTool

        verifyClass(IActionProvider, SkinsTool)
        verifyClass(ISkinsContainer, SkinsTool)
        verifyClass(ISkinsTool, SkinsTool)

    def test_add_invalid_path(self):
        tool = self._makeOne()

        # We start out with no wkin selections
        self.assertEquals(len(tool.getSkinSelections()), 0)

        # Add a skin selection with an invalid path element
        paths = 'foo, bar, .svn'
        tool.addSkinSelection('fooskin', paths)

        # Make sure the skin selection exists
        paths = tool.getSkinPath('fooskin')
        self.failIf(paths is None)

        # Test for the contents
        self.failIf(paths.find('foo') == -1)
        self.failIf(paths.find('bar') == -1)
        self.failUnless(paths.find('.svn') == -1)


class SkinnableTests(unittest.TestCase):

    def _makeOne(self):
        from Products.CMFCore.SkinsTool import SkinsTool
        from Products.CMFCore.Skinnable import SkinnableObjectManager

        class TestSkinnableObjectManager(SkinnableObjectManager):
            tool = SkinsTool()
            # This is needed otherwise REQUEST is the string
            # '<Special Object Used to Force Acquisition>'
            REQUEST = None
            def getSkinsFolderName(self):
                '''tool'''
                return 'tool'

        return TestSkinnableObjectManager()

    def tearDown(self):
        from Products.CMFCore.Skinnable import SKINDATA
        SKINDATA.clear()
        cleanUp()

    def test_getCurrentSkinName(self):
        som = self._makeOne()

        pathA = ('foo, bar')
        pathB = ('bar, foo')

        som.tool.addSkinSelection('skinA', pathA)
        som.tool.addSkinSelection('skinB', pathB)

        som.tool.manage_properties(default_skin='skinA')

        # Expect the default skin name to be returned
        self.failUnless(som.getCurrentSkinName() == 'skinA')

        # after a changeSkin the new skin name should be returned
        som.changeSkin('skinB', som.REQUEST)
        self.failUnless(som.getCurrentSkinName() == 'skinB')


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(SkinsContainerTests),
        unittest.makeSuite(SkinsToolTests),
        unittest.makeSuite(SkinnableTests),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
