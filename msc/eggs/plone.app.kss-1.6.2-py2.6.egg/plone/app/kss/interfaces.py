from zope.interface import Interface
from kss.core.interfaces import IKSSView

# contentish + folderish (incl. site root)
class IPortalObject(Interface):
    'All portal objects including AT ones'

class IPloneKSSView(IKSSView):
    '''View for Plone'''
