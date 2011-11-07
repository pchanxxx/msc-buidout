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
"""Local Component Architecture
"""
__docformat__ = "reStructuredText"

import zope.component
import zope.deprecation

from zope.site import getNextUtility, queryNextUtility # BBB

_marker = object()

# BBB: Deprecated on 9/26/2006
@zope.deprecation.deprecate('''This function has been deprecated and will go
away in Zope 3.6. There is no replacement for this function, since it does not
make sense in light of registry bases anymore. If you are using this function
to lookup the next utility, consider using get/queryNextUtility. Otherwise, it
is suggested to iterate through the list of bases of a registry manually.''')
def getNextSiteManager(context):
    """Get the next site manager."""
    sm = queryNextSiteManager(context, _marker)
    if sm is _marker:
        raise zope.component.interfaces.ComponentLookupError(
              "No more site managers have been found.")
    return sm


# BBB: Deprecated on 9/26/2006
@zope.deprecation.deprecate('''This function has been deprecated and will go
away in Zope 3.6. There is no replacement for this function, since it does not
make sense in light of registry bases anymore. If you are using this function
to lookup the next utility, consider using get/queryNextUtility. Otherwise, it
is suggested to iterate through the list of bases of a registry manually.''')
def queryNextSiteManager(context, default=None):
    """Get the next site manager.

    If the site manager of the given context is the global site manager, then
    `default` is returned.
    """
    sm = zope.component.getSiteManager(context)
    if sm is zope.component.getGlobalSiteManager():
        return default

    bases = sm.__bases__
    if not bases:
        return zope.component.getGlobalSiteManager()
    return bases[0]
