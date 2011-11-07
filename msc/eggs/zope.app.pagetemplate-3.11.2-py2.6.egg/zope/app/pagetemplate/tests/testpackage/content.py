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
"""Test Content

$Id: content.py 116904 2010-09-25 13:20:53Z icemac $
"""
from zope.browserpage import ViewPageTemplateFile

class Content(object):
    def getSomething(self):
        return 42


class PTComponent(object):
    def __init__(self, content, request=None):
        self.context = content
        self.request = request

    index = ViewPageTemplateFile("view.pt")
    default = ViewPageTemplateFile("default.pt")
    nothing = ViewPageTemplateFile("nothing.pt")
