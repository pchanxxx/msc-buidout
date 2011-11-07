import unittest

import zope, transaction
import os.path
from zope.testing import doctest, doctestunit, module

import testing

def setUp(test):
    module.setUp(test, 'z3c.blobfile.readme_txt')

def tearDown(test):
    module.tearDown(test, 'z3c.blobfile.readme_txt')


def test_suite():
    suite = unittest.TestSuite()
    
    globs = {'zope': zope,
            'transaction': transaction,
            'pprint': doctestunit.pprint}

    test = testing.FunctionalBlobDocFileSuite('blobfile.txt',
                package='z3c.blobfile',
                globs=globs,
                optionflags=doctest.NORMALIZE_WHITESPACE+doctest.ELLIPSIS)
    test.layer = testing.BlobFileLayer
    
    suite.addTests((test,))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
