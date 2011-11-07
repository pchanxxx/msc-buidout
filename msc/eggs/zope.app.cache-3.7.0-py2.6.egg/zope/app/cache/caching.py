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
"""Helpers for caching.

$Id: caching.py 100472 2009-05-27 16:09:26Z hannosch $
"""
__docformat__ = 'restructuredtext'

from zope.interface import classProvides
from zope.component import ComponentLookupError, getUtility
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.app.cache.interfaces import ICacheable, ICache
from zope.traversing.api import getPath

def getCacheForObject(obj):
    """Returns the cache associated with `obj` or ``None``."""
    adapter = ICacheable(obj, None)
    if adapter is None:
        return None
    cache_id = adapter.getCacheId()
    if not cache_id:
        return None
    return getUtility(ICache, cache_id)

def getLocationForCache(obj):
    """Returns the location to be used for caching the object or ``None``."""
    try:
        return getPath(obj)
    except (ComponentLookupError, TypeError):
        return None

class CacheNamesVocabulary(UtilityVocabulary):
    classProvides(IVocabularyFactory)
    interface = ICache
    nameOnly = True
