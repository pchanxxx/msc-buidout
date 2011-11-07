import logging
from types import ListType, TupleType

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import ISetupTool

_marker = []

logger = logging.getLogger('plone.app.upgrade')


def null_upgrade_step(tool):
    """ This is a null upgrade, use it when nothing happens """
    pass


def safeEditProperty(obj, key, value, data_type='string'):
    """ An add or edit function, surprisingly useful :) """
    if obj.hasProperty(key):
        obj._updateProperty(key, value)
    else:
        obj._setProperty(key, value, data_type)


def addLinesToProperty(obj, key, values):
    if obj.hasProperty(key):
        data = getattr(obj, key)
        if type(data) is TupleType:
            data = list(data)
        if type(values) is ListType:
            data.extend(values)
        else:
            data.append(values)
        obj._updateProperty(key, data)
    else:
        if type(values) is not ListType:
            values = [values]
        obj._setProperty(key, values, 'lines')


def saveCloneActions(actionprovider):
    try:
        return True, actionprovider._cloneActions()
    except AttributeError:
        # Stumbled across ancient dictionary actions
        if not hasattr(aq_base(actionprovider), '_convertActions'):
            return False, ("Can't convert actions of %s! Jumping to next "
                           "action." % actionprovider.getId(), logging.ERROR)
        else:
            actionprovider._convertActions()
            return True, actionprovider._cloneActions()


def testSkinLayer(skinsTool, layer):
    """Make sure a skin layer exists"""
    # code adapted from CMFCore.SkinsContainer.getSkinByPath
    ob = aq_base(skinsTool)
    for name in layer.strip().split('/'):
        if not name:
            continue
        if name.startswith('_'):
            return 0
        ob = getattr(ob, name, None)
        if ob is None:
            return 0
    return 1


def cleanupSkinPath(portal, skinName, test=1):
    """Remove invalid skin layers from skins"""
    skinstool = getToolByName(portal, 'portal_skins')
    selections = skinstool._getSelections()
    old_path = selections[skinName].split(',')
    new_path = []
    for layer in old_path:
        if layer and testSkinLayer(skinstool, layer):
            new_path.append(layer)
    skinstool.addSkinSelection(skinName, ','.join(new_path), test=test)


def installOrReinstallProduct(portal, product_name, out=None, hidden=False):
    """Installs a product

    If product is already installed test if it needs to be reinstalled. Also
    fix skins after reinstalling
    """
    qi = getToolByName(portal, 'portal_quickinstaller')
    if not qi.isProductInstalled(product_name):
        qi.installProduct(product_name, hidden=hidden)
        # Refresh skins
        portal.clearCurrentSkin()
        portal.setupCurrentSkin(portal.REQUEST)
        logger.info("Installed %s" % product_name)
    else:
        info = qi._getOb(product_name)
        installed_version = info.getInstalledVersion()
        product_version = qi.getProductVersion(product_name)
        if installed_version != product_version:
            qi.reinstallProducts([product_name])
            logger.info("%s is out of date (installed: %s/ filesystem: %s), "
                        "reinstalled." % (product_name, installed_version,
                                          product_version))
        else:
            logger.info('%s already installed.' % product_name)


def loadMigrationProfile(context, profile, steps=_marker):
    if not ISetupTool.providedBy(context):
        context = getToolByName(context, "portal_setup")
    if steps is _marker:
        context.runAllImportStepsFromProfile(profile, purge_old=False)
    else:
        for step in steps:
            context.runImportStepFromProfile(profile,
                                             step,
                                             run_dependencies=False,
                                             purge_old=False)
