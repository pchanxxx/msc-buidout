##############################################################################
#
# Copyright (c) 2006 Lovely Systems and Contributors.
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
"""Tag test setup

$Id: tests.py 92078 2008-10-12 14:46:38Z ccomb $
"""
__docformat__ = "reStructuredText"

import doctest, unittest
from z3c.batching import batch

def test_suite():

    return unittest.TestSuite((
        doctest.DocFileSuite(
                'README.txt',
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
                ),
        doctest.DocTestSuite(batch,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
                )
        ))
