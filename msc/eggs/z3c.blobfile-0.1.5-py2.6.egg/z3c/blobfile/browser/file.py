##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
"""File views.

$Id: file.py 113078 2010-06-04 06:32:13Z ctheune $
"""
__docformat__ = 'restructuredtext'

import zope.event
from zope import lifecycleevent
from zope.contenttype import guess_content_type
from zope.publisher import contenttype
from zope.schema import Text
from zope.exceptions.interfaces import UserError

from zope.app.file.interfaces import IFile
from z3c.blobfile.i18n import ZopeMessageFactory as _
from zope.dublincore.interfaces import IZopeDublinCore
from zope.app.file.browser.file import FileUpdateView
import zope.datetime

import time
from datetime import datetime

import z3c.blobfile.file

class FileView(object):

    def show(self):
        """Returns file handle for efficient streaming."""
        
        if self.request is not None:
            self.request.response.setHeader('Content-Type',
                                            self.context.contentType)
            self.request.response.setHeader('Content-Length',
                                            self.context.getSize())
        try:
            modified = IZopeDublinCore(self.context).modified
        except TypeError:
            modified = None
        if modified is None or not isinstance(modified, datetime):
            return self.context.openDetached()

        header= self.request.getHeader('If-Modified-Since', None)
        lmt = zope.datetime.time(modified.isoformat())
        if header is not None:
            header = header.split(';')[0]
            try:
                mod_since = long(zope.datetime.time(header))
            except:
                mod_since = None
            if mod_since is not None:
                if lmt <= mod_since:
                    self.request.response.setStatus(304)
                    return ''

        self.request.response.setHeader('Last-Modified', zope.datetime.rfc1123_date(lmt))

        return self.context.openDetached()

class FileAdd(FileUpdateView):
    """View that adds a new File object based on a file upload."""

    def update_object(self, data, contenttype):
        f = z3c.blobfile.file.File(data, contenttype)
        zope.event.notify(lifecycleevent.ObjectCreatedEvent(f))
        self.context.add(f)
        self.request.response.redirect(self.context.nextURL())
        return ''
