##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""PythonScript export / import support.

$Id: exportimport.py 110425 2010-04-01 17:19:14Z tseaver $
"""

from zope.component import adapts

from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import BodyAdapterBase

from interfaces import IPythonScript


class PythonScriptBodyAdapter(BodyAdapterBase):

    """Body im- and exporter for PythonScript.
    """

    adapts(IPythonScript, ISetupEnviron)

    def _exportBody(self):
        """Export the object as a file body.
        """
        return self.context.read()

    def _importBody(self, body):
        """Import the object from the file body.
        """
        self.context.write(body)

    body = property(_exportBody, _importBody)

    mime_type = 'text/plain'

    suffix = '.py'
