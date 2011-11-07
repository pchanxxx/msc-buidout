from zope import component
from zope.component import getMultiAdapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from kss.core.interfaces import IKSSView

from plone.app.kss.portlets import attributesModified
from plone.app.layout.viewlets.common import PathBarViewlet
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.app.layout.viewlets.common import GlobalSectionsViewlet

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerPortalTabsReload(obj, view, event):
    triggeringAttributes = ('title', 'description')
    if attributesModified(triggeringAttributes, event):
        ksscore = view.getCommandSet('core')
        selector = ksscore.getHtmlIdSelector('portal-globalnav')
        zopecommands = view.getCommandSet('zope')
        zopecommands.refreshViewletByClass(selector, GlobalSectionsViewlet)

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerDocumentBylineReload(obj, view, event):
    ksscore = view.getCommandSet('core')
    selector = ksscore.getHtmlIdSelector('plone-document-byline')
    zopecommands = view.getCommandSet('zope')
    zopecommands.refreshViewletByClass(selector, DocumentBylineViewlet)

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerBreadcrumbsReload(obj, view, event):
    triggeringAttributes = ('title', 'description')
    if attributesModified(triggeringAttributes, event):
        ksscore = view.getCommandSet('core')
        selector = ksscore.getHtmlIdSelector('portal-breadcrumbs')
        zopecommands = view.getCommandSet('zope')
        zopecommands.refreshViewletByClass(selector, PathBarViewlet)

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerHeadTitleReload(obj, view, event):
    triggeringAttributes = ('title', )
    if attributesModified(triggeringAttributes, event):
        htmlhead = getMultiAdapter((obj, view.request, view), name=u'plone.htmlhead')
        headtitle = getMultiAdapter((obj, view.request, view, htmlhead), name=u'plone.htmlhead.title')
        headtitle.update()
        ksscore = view.getCommandSet('core')
        ksscore.replaceHTML(
            'head title',
            headtitle.render(),
            withKssSetup='False')
