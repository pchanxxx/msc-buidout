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
"""Container-related interfaces

$Id: interfaces.py 99932 2009-05-13 21:33:55Z tseaver $
"""
__docformat__ = 'restructuredtext'

# BBB
from zope.browser.interfaces import IAdding

# BBB
from zope.container.interfaces import (
    DuplicateIDError,
    ContainerError,
    InvalidContainerType,
    InvalidItemType,
    InvalidType,
    IContained,
    IItemContainer,
    ISimpleReadContainer,
    IReadContainer,
    IWriteContainer,
    IItemWriteContainer,
    IContainer,
    IBTreeContainer,
    IOrderedContainer,
    IContainerNamesContainer,
    IObjectMovedEvent,
    UnaddableError,
    IObjectAddedEvent,
    INameChooser,
    IObjectRemovedEvent,
    IContainerModifiedEvent,
    IFind,
    IObjectFindFilter,
    IIdFindFilter
)
