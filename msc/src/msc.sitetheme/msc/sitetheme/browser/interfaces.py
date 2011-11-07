#from plone.theme.interfaces import IDefaultPloneLayer

#class IThemeSpecific(IDefaultPloneLayer):
#    """Marker interface that defines a Zope 3 browser layer.
#    """
from plonetheme.classic.browser.interfaces import IThemeSpecific as IClassicTheme

class IThemeSpecific(IClassicTheme):
    """theme-specific layer """