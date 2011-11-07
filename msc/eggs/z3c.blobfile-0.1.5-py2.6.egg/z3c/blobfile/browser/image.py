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
"""Image view.

$Id: image.py 113078 2010-06-04 06:32:13Z ctheune $
"""
__docformat__ = 'restructuredtext'

from z3c.blobfile.browser.file import FileView
from zope.app.file.browser.image import ImageData

class ImageData(FileView, ImageData):
    '''Image view with zope.app.file's show method overriden by z3c.blobfile's one'''
