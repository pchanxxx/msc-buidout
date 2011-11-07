"""Test that the BBB imports in the namedtemplate module work.
"""
__docformat__ = "reStructuredText"

import unittest

from zope.component.testing import PlacelessSetup
class Test(PlacelessSetup, unittest.TestCase):

    def testImportNamedtemplateModule(self):
        from zope.app.pagetemplate import namedtemplate

def test_suite():
    loader=unittest.TestLoader()
    return loader.loadTestsFromTestCase(Test)
