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
"""File content component

$Id: file.py 113078 2010-06-04 06:32:13Z ctheune $
"""
__docformat__ = 'restructuredtext'

from persistent import Persistent
import transaction
from zope.interface import implements
import zope.component
import zope.component.interfaces
import zope.app.publication.interfaces

from ZODB.blob import Blob

import interfaces

class File(Persistent):
    """A persistent content component storing binary file data."""

    implements(zope.app.publication.interfaces.IFileContent,
               interfaces.IBlobFile)

    def __init__(self, data='', contentType=''):
        self.contentType = contentType
        self._blob = Blob()
        f = self._blob.open('w')
        f.write('')
        f.close()
        self._setData(data)

    def open(self, mode='r'):
        if mode != 'r' and 'size' in self.__dict__:
            del self.__dict__['size']
        return self._blob.open(mode)

    def openDetached(self):
        return open(self._blob.committed(), 'rb')

    def _setData(self, data):
        if 'size' in self.__dict__:
            del self.__dict__['size']
        # Search for a storable that is able to store the data
        dottedName = ".".join((data.__class__.__module__,
                               data.__class__.__name__))
        storable = zope.component.getUtility(interfaces.IStorage,
                                             name=dottedName)
        storable.store(data, self._blob)

    def _getData(self):
        fp = self._blob.open('r')
        data = fp.read()
        fp.close()
        return data

    _data = property(_getData, _setData)
    data = property(_getData, _setData)

    @property
    def size(self):
        if 'size' in self.__dict__:
            return self.__dict__['size']
        reader = self._blob.open()
        reader.seek(0,2)
        size = int(reader.tell())
        reader.close()
        self.__dict__['size'] = size
        return size

    def getSize(self):
        return self.size

class FileReadFile(object):
    """Adapter for file-system style read access."""

    def __init__(self, context):
        self.context = context

    def read(self, bytes=-1):
        return self.context.data

    def size(self):
        return self.context.size


class FileWriteFile(object):
    """Adapter for file-system style write access."""

    def __init__(self, context):
        self.context = context

    def write(self, data):
        self.context._setData(data)

class FileReplacedEvent(zope.component.interfaces.ObjectEvent):
    """Notifies about the replacement of a zope.app.file with a z3c.blobfile."""

    def __init__(self, object, blobfile):
        super(FileReplacedEvent, self).__init__(object)
        self.blobfile = blobfile


