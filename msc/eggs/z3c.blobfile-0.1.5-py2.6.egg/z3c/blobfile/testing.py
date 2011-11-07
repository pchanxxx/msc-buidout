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
"""z3c.blobfile common test related classes/functions/objects.

$Id: testing.py 113078 2010-06-04 06:32:13Z ctheune $
"""
__docformat__ = "reStructuredText"

import os.path
import shutil
import tempfile
import persistent
import transaction
from ZODB.DB import DB
from ZODB.DemoStorage import DemoStorage
from ZODB.blob import BlobStorage
import ZODB.interfaces

import zope.interface
from zope.testing import doctest
import zope.app.testing.functional
import zope.app.file.interfaces

from zope.app.component.hooks import setSite

here = os.path.dirname(os.path.realpath(__file__))

zptlogo = (
    'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
    '\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
    '\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
    '\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
    '\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
    '\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
    '\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
    '\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
    '\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
    '\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04'
    '\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4'
    '\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
    '\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
    '\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
    '\x00A\x00;'
    )

class MyFile(persistent.Persistent):
    zope.interface.implements(zope.app.file.interfaces.IFile)

    data = 'My data'
    contentType = 'text/plain'

class FunctionalBlobTestSetup(zope.app.testing.functional.FunctionalTestSetup):

    temp_dir_name = None
    direct_blob_support = False

    def setUp(self):
        """Prepares for a functional test case."""
        # Tear down the old demo storage (if any) and create a fresh one
        transaction.abort()
        self.db.close()
        storage = DemoStorage("Demo Storage", self.base_storage)
        if ZODB.interfaces.IBlobStorage.providedBy(storage):
            # at least ZODB 3.9
            self.direct_blob_support = True
        else:
            # make a dir
            temp_dir_name = self.temp_dir_name = tempfile.mkdtemp()
            # wrap storage with BlobStorage
            storage = BlobStorage(temp_dir_name, storage)
        self.db = self.app.db = DB(storage)
        self.connection = None

    def tearDown(self):
        """Cleans up after a functional test case."""
        transaction.abort()
        if self.connection:
            self.connection.close()
            self.connection = None
        self.db.close()
        if not self.direct_blob_support and self.temp_dir_name is not None:
            # del dir named '__blob_test__%s' % self.name
            shutil.rmtree(self.temp_dir_name, True)
            self.temp_dir_name = None
        setSite(None)

    def closeDB(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        self.db.close()

    def reopenDB(self):
        storage = BlobStorage(temp_dir_name, storage)
        self.db = self.app.db = DB(storage)
        self.connection = None



class ZCMLLayer(zope.app.testing.functional.ZCMLLayer):

    def setUp(self):
        self.setup = FunctionalBlobTestSetup(self.config_file)

def FunctionalBlobDocFileSuite(*paths, **kw):
    globs = kw.setdefault('globs', {})
    globs['http'] = zope.app.testing.functional.HTTPCaller()
    globs['getRootFolder'] = zope.app.testing.functional.getRootFolder
    globs['sync'] = zope.app.testing.functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        FunctionalBlobTestSetup().setUp()

        if kwsetUp is not None:
            kwsetUp(test)
    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        if kwtearDown is not None:
            kwtearDown(test)
        FunctionalBlobTestSetup().tearDown()
    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old
                             | doctest.ELLIPSIS
                             | doctest.REPORT_NDIFF
                             | doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = zope.app.testing.functional.Functional
    return suite

BlobFileLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'BlobFileLayer', allow_teardown=True)
