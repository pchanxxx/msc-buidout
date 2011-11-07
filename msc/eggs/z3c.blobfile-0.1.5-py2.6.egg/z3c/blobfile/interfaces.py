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
"""File interfaces

$Id: interfaces.py 113078 2010-06-04 06:32:13Z ctheune $
"""
__docformat__ = 'restructuredtext'

import zope.interface
import zope.component.interfaces
import zope.app.file.interfaces

class IOpenable(zope.interface.Interface):
    """Openable file
    """

    def open(mode='r'):
        """Open file and return the file descriptor
        """

    def openDetached():
        '''Return a read-only file descriptor, detached from ZODB connection'''

class IBlobFile(zope.app.file.interfaces.IFile, IOpenable):
    """A file that uses Blobs as data storage."""


class IBlobImage(zope.app.file.interfaces.IImage, IOpenable):
    """An image that uses Blobs as data storage."""

    
class IStorage(zope.interface.Interface):
    """Store file data
    """

    def store(data, blob):
        """Store the data into the blob

	    Raises NonStorable if data is not storable.
        """

class NotStorable(Exception):
    """Data is not storable
    """

class IFileReplacedEvent(zope.component.interfaces.IObjectEvent):
    """A zope.app.file has been replaced by it's blobfile counterpart."""
