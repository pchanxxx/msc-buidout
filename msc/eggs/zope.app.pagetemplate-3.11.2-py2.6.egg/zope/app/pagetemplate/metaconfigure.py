##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""ZCML configuration directives for configuring the default zope:
namespace in TALES.

$Id: metaconfigure.py 116904 2010-09-25 13:20:53Z icemac $
"""
__docformat__ = 'restructuredtext'

# BBB
from zope.browserpage.metaconfigure import clear
from zope.browserpage.metadirectives import IExpressionTypeDirective
from zope.browserpage.metaconfigure import expressiontype
from zope.browserpage.metaconfigure import registerType

