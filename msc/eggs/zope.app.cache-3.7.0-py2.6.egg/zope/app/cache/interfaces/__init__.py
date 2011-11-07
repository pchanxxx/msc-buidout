##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""Interfaces for cache manager.

$Id: __init__.py 102133 2009-07-23 10:09:00Z hannosch $
"""
__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope.schema import Choice

class ICacheable(Interface):
    """Object that can be associated with a cache manager."""

    cacheId = Choice(
        title=u"Cache Name",
        description=u"The name of the cache used for this object.",
        required=True,
        vocabulary="Cache Names")

    def getCacheId():
        """Gets the associated cache manager ID."""

    def setCacheId(id):
        """Sets the associated cache manager ID."""


# BBB import. Leave in place
from zope.ramcache.interfaces import ICache
