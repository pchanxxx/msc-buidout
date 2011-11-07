import doctest
import unittest
import zope.component.event # import does the trick
from zope.testing.cleanup import cleanUp

# BBB Zope 2.11
try:
    from zope.site.hooks import setHooks
except ImportError:
    from zope.app.component.hooks import setHooks


def setUp(test=None):
    setHooks()

def tearDown(test=None):
    cleanUp()

def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite('siteview.txt',
                             package='kss.core',
                             setUp=setUp,
                             tearDown=tearDown)
        ])
