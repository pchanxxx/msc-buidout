from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

class PloneAppUUID(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.uuid
        xmlconfig.file('configure.zcml', plone.app.uuid, context=configurationContext)
    
PLONE_APP_UUID_FIXTURE = PloneAppUUID()
PLONE_APP_UUID_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(PLONE_APP_UUID_FIXTURE,), name="plone.app.uuid:Integration")
PLONE_APP_UUID_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(PLONE_APP_UUID_FIXTURE,), name="plone.app.uuid:Functional")
