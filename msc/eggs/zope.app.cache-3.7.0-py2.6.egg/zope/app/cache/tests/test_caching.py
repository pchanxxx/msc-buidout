##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Unit tests for caching helpers.

$Id: test_caching.py 85503 2008-04-20 10:35:08Z lgs $
"""
import unittest
from zope.interface import implements
from zope.annotation.interfaces import IAnnotatable, IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation.attribute import AttributeAnnotations

from zope.app.cache.interfaces import ICacheable, ICache
from zope.app.cache.caching import getCacheForObject, getLocationForCache
from zope.app.cache.annotationcacheable import AnnotationCacheable
from zope.app.testing import ztapi, placelesssetup

from zope.traversing.interfaces import IPhysicallyLocatable


class ObjectStub(object):
    implements(IAttributeAnnotatable,
               IPhysicallyLocatable)

    def getPath(self):
        return '/cached-object'

class CacheStub(object):
    implements(ICache)


class Test(placelesssetup.PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(Test, self).setUp()
        ztapi.provideAdapter(IAttributeAnnotatable, IAnnotations,
                             AttributeAnnotations)
        ztapi.provideAdapter(IAnnotatable, ICacheable,
                             AnnotationCacheable)
        self._cache = CacheStub()
        ztapi.provideUtility(ICache, self._cache, "my_cache")

    def testGetCacheForObj(self):
        obj = ObjectStub()
        self.assertEquals(getCacheForObject(obj), None)
        ICacheable(obj).setCacheId("my_cache")
        self.assertEquals(getCacheForObject(obj), self._cache)

    def testGetLocationForCache(self):
        obj = ObjectStub()
        self.assertEqual(getLocationForCache(obj), '/cached-object')


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
