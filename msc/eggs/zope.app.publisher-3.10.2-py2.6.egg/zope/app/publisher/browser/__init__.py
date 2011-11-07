##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Provide zope app-server customizatioin of publisher browser facilities

$Id: __init__.py 103291 2009-08-27 15:12:51Z nadako $
"""
# BBB imports
from zope.publisher.browser import BrowserLanguages
from zope.publisher.browser import CacheableBrowserLanguages
from zope.publisher.browser import ModifiableBrowserLanguages
from zope.publisher.browser import NotCompatibleAdapterError
from zope.publisher.defaultview import IDefaultViewNameAPI
from zope.publisher.defaultview import getDefaultViewName
from zope.publisher.defaultview import queryDefaultViewName
