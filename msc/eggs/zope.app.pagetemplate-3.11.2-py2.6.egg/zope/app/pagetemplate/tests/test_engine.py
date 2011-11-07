import unittest

class BBBTests(unittest.TestCase):

    def test_BBB_imports(self):
        from zope.app.pagetemplate.engine import InlineCodeError
        from zope.app.pagetemplate.engine import ZopeTraverser
        from zope.app.pagetemplate.engine import zopeTraverser
        from zope.app.pagetemplate.engine import trustedZopeTraverser
        from zope.app.pagetemplate.engine import ZopePathExpr
        from zope.app.pagetemplate.engine import TrustedZopePathExpr
        from zope.app.pagetemplate.engine import ZopePythonExpr
        from zope.app.pagetemplate.engine import ZopeContextBase
        from zope.app.pagetemplate.engine import ZopeContext
        from zope.app.pagetemplate.engine import TrustedZopeContext
        from zope.app.pagetemplate.engine import AdapterNamespaces
        from zope.app.pagetemplate.engine import ZopeBaseEngine
        from zope.app.pagetemplate.engine import ZopeEngine
        from zope.app.pagetemplate.engine import TrustedZopeEngine
        from zope.app.pagetemplate.engine import TraversableModuleImporter
        from zope.app.pagetemplate.engine import Engine
        from zope.app.pagetemplate.engine import TrustedEngine
        from zope.app.pagetemplate.engine import AppPT
        from zope.app.pagetemplate.engine import TrustedAppPT

def test_suite():
    return unittest.makeSuite(BBBTests)
