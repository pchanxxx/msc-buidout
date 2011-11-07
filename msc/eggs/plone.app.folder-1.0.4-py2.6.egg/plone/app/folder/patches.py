from Products.CMFCore.utils import getToolByName
from plone.app.folder.nogopip import GopipIndex


# monkey patch for Plone 3.x:
# if the `getObjPositionInParent` index doesn't exist or else was replaced
# by something else (e.g. like in Plone 4.x), there's no need to wake up
# all those objects and `reindexOnReorder` can be cut short...


def reindexOnReorder(self, parent):
    """ reindexing of "gopip" is probably no longer needed :) """
    catalog = getToolByName(self, 'portal_catalog')
    index = catalog.Indexes.get('getObjPositionInParent')
    if not isinstance(index, GopipIndex):
        return self.__nogopip_old_reindexOnReorder(parent)


def applyPatches():
    try:
        from plone.app import upgrade       # is this plone 4?
        upgrade                             # make pyflakes happy :p
    except ImportError:
        from Products.CMFPlone.PloneTool import PloneTool
        PloneTool.__nogopip_old_reindexOnReorder = PloneTool.reindexOnReorder
        PloneTool.reindexOnReorder = reindexOnReorder
