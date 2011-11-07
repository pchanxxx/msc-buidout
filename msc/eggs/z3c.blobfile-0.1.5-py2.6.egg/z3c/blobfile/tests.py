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
"""Test Image content component

$Id: tests.py 113078 2010-06-04 06:32:13Z ctheune $
"""
import unittest
import zope.component
import struct

from zope.interface.verify import verifyClass
from zope.app.file.interfaces import IImage
from z3c.blobfile.image import Image, FileFactory, ImageSized, getImageInfo
from z3c.blobfile.file import File, FileWriteFile, FileReadFile
from z3c.blobfile.interfaces import IBlobFile, IBlobImage

import testing
import storages
import interfaces

def registerUtilities():
     zope.component.provideUtility(storages.StringStorable(),
                                   interfaces.IStorage,
                                   name="__builtin__.str")
     zope.component.provideUtility(storages.UnicodeStorable(),
                                   interfaces.IStorage,
                                   name="__builtin__.unicode")
     zope.component.provideUtility(storages.FileChunkStorable(),
                                   interfaces.IStorage,
                                   name="zope.app.file.file.FileChunk")
     zope.component.provideUtility(storages.FileDescriptorStorable(),
                                   interfaces.IStorage,
                                   name="__builtin__.file")

class TestImage(unittest.TestCase):

    def setUp(self):
        registerUtilities()

    def _makeImage(self, *args, **kw):
        return Image(*args, **kw)

    def testEmpty(self):
        file = self._makeImage()
        self.assertEqual(file.contentType, '')
        self.assertEqual(file.data, '')

    def testConstructor(self):
        file = self._makeImage('Data')
        self.assertEqual(file.contentType, '')
        self.assertEqual(file.data, 'Data')

    def testMutators(self):
        image = self._makeImage()

        image.contentType = 'image/jpeg'
        self.assertEqual(image.contentType, 'image/jpeg')

        image._setData(testing.zptlogo)
        self.assertEqual(image.data, testing.zptlogo)
        self.assertEqual(image.contentType, 'image/gif')
        self.assertEqual(image.getImageSize(), (16, 16))

    def testInterface(self):
        self.failUnless(IImage.implementedBy(Image))
        self.failUnless(verifyClass(IImage, Image))
        self.failUnless(IBlobFile.implementedBy(Image))
        self.failUnless(IBlobImage.implementedBy(Image))
        self.failUnless(verifyClass(IBlobFile, Image))
    
    def testDataMutatorWithLargeHeader(self):
        from z3c.blobfile.image import IMAGE_INFO_BYTES
        bogus_header_length = struct.pack('>H', IMAGE_INFO_BYTES * 2)
        data = ('\xff\xd8\xff\xe0' + bogus_header_length +
                '\x00' * IMAGE_INFO_BYTES * 2 +
                '\xff\xc0\x00\x11\x08\x02\xa8\x04\x00')
        image = self._makeImage()
        image._setData(data)
        self.assertEqual(image.getImageSize(), (1024, 680))

class TestFileAdapters(unittest.TestCase):

    def setUp(self):
        registerUtilities()

    def _makeFile(self, *args, **kw):
        return Image(*args, **kw)

    def test_ReadFile(self):
        file = self._makeFile()
        content = "This is some file\ncontent."
        file.data = content
        file.contentType = 'text/plain'
        self.assertEqual(FileReadFile(file).read(), content)
        self.assertEqual(FileReadFile(file).size(), len(content))

    def test_WriteFile(self):
        file = self._makeFile()
        content = "This is some file\ncontent."
        FileWriteFile(file).write(content)
        self.assertEqual(file.data, content)

class DummyImage(object):

    def setUp(self):
        registerUtilities()

    def __init__(self, width, height, bytes):
        self.width = width
        self.height = height
        self.bytes = bytes

    def getSize(self):
        return self.bytes

    def getImageSize(self):
        return self.width, self.height


class TestFileFactory(unittest.TestCase):

    def setUp(self):
        registerUtilities()

    def test_image(self):
        factory = FileFactory(None)
        f = factory("spam.txt", "image/foo", "hello world")
        self.assert_(isinstance(f, Image), f)
        f = factory("spam.txt", "", testing.zptlogo)
        self.assert_(isinstance(f, Image), f)

    def test_text(self):
        factory = FileFactory(None)
        f = factory("spam.txt", "", "hello world")
        self.assert_(isinstance(f, File), f)
        self.assert_(not isinstance(f, Image), f)
        f = factory("spam.txt", "", "\0\1\2\3\4")
        self.assert_(isinstance(f, File), f)
        self.assert_(not isinstance(f, Image), f)
        f = factory("spam.txt", "text/splat", testing.zptlogo)
        self.assert_(isinstance(f, File), f)
        self.assert_(not isinstance(f, Image), f)
        f = factory("spam.txt", "application/splat", testing.zptlogo)
        self.assert_(isinstance(f, File), f)
        self.assert_(not isinstance(f, Image), f)

class TestSized(unittest.TestCase):

    def setUp(self):
        registerUtilities()

    def testInterface(self):
        from zope.size.interfaces import ISized
        self.failUnless(ISized.implementedBy(ImageSized))
        self.failUnless(verifyClass(ISized, ImageSized))

    def test_zeroSized(self):
        s = ImageSized(DummyImage(0, 0, 0))
        self.assertEqual(s.sizeForSorting(), ('byte', 0))
        self.assertEqual(s.sizeForDisplay(), u'0 KB ${width}x${height}')
        self.assertEqual(s.sizeForDisplay().mapping['width'], '0')
        self.assertEqual(s.sizeForDisplay().mapping['height'], '0')

    def test_arbitrarySize(self):
        s = ImageSized(DummyImage(34, 56, 78))
        self.assertEqual(s.sizeForSorting(), ('byte', 78))
        self.assertEqual(s.sizeForDisplay(), u'1 KB ${width}x${height}')
        self.assertEqual(s.sizeForDisplay().mapping['width'], '34')
        self.assertEqual(s.sizeForDisplay().mapping['height'], '56')

    def test_unknownSize(self):
        s = ImageSized(DummyImage(-1, -1, 23))
        self.assertEqual(s.sizeForSorting(), ('byte', 23))
        self.assertEqual(s.sizeForDisplay(), u'1 KB ${width}x${height}')
        self.assertEqual(s.sizeForDisplay().mapping['width'], '?')
        self.assertEqual(s.sizeForDisplay().mapping['height'], '?')

    def test_getImageInfo(self):
        t, w, h = getImageInfo('\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01'
                               '\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C')
        self.assertEqual(t, "image/jpeg")

    def test_getImageInfo_bmp(self):
        t, w, h = getImageInfo('BMl\x05\x00\x00\x00\x00\x00\x006\x04\x00\x00('
                               '\x00\x00\x00\x10\x00\x00\x00\x10\x00\x00\x00'
                               '\x01\x00\x08\x00\x01\x00\x00\x006\x01\x00\x00'
                               '\x12\x0b\x00\x00\x12\x0b\x00\x00\x00\x01\x00'
                               '... and so on ...')
        self.assertEqual(t, "image/x-ms-bmp")
        self.assertEqual(w, 16)
        self.assertEqual(h, 16)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestImage),
        unittest.makeSuite(TestFileAdapters),
        unittest.makeSuite(TestFileFactory),
        unittest.makeSuite(TestSized)
        ))

if __name__=='__main__':
    unittest.TextTestRunner().run(test_suite())
