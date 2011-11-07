from Acquisition import Explicit

from zope import component
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import getAdapters
from zope.annotation import IAnnotations

from zope.contentprovider.interfaces import IContentProvider
from zope.viewlet.interfaces import IViewletManager
from zope.viewlet.interfaces import IViewlet

from kss.core import CommandSet
from kss.core.interfaces import IBeforeRenderKSSCommandsEvent
from interfaces import IZopeCommands


class ZopeCommands(CommandSet):
    implements(IZopeCommands)

    def refreshProvider(self, selector, name):
        renderer = getMultiAdapter((self.context, self.request, self.view),
                                    IContentProvider, name=name)
        if isinstance(renderer, Explicit):
            renderer = renderer.__of__(self.context)

        renderer.update()
        result = renderer.render()

        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(selector, result)

    def refreshViewlet(self, selector, manager, name):

        if isinstance(manager, basestring):
            manager = getMultiAdapter(
                (self.context, self.request, self.view, ), IViewletManager,
                name=manager)

        renderer = getMultiAdapter(
            (self.context, self.request, self.view, manager), IViewlet,
            name=name)
        renderer = renderer.__of__(self.context)

        renderer.update()
        result = renderer.render()

        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(selector, result)

    def refreshViewletByClass(self, selector, klass):
        annotations = IAnnotations(self.request)
        viewletByClass = annotations.get('viewletByClass', [])
        viewletByClass.append((selector, klass))
        annotations['viewletByClass'] = viewletByClass


@component.adapter(IBeforeRenderKSSCommandsEvent)
def addRefreshViewletCommands(event):
    view = event.view
    context = view.context
    request = view.request
    annotations = IAnnotations(request)
    viewletByClass = annotations.get('viewletByClass', [])
    if viewletByClass:
        for name, manager in getAdapters(
                (context, request, view, ), IViewletManager):
            for name, viewlet in  getAdapters(
                (context, request, view, manager), IViewlet):
                maybeRenderViewlet(viewlet, viewletByClass)


def maybeRenderViewlet(viewlet, viewletByClass):
    for selector, klass in viewletByClass:
        if isinstance(viewlet, klass):
            viewlet.update()
            result = viewlet.render()
            ksscore = viewlet.view.getCommandSet('core')
            ksscore.replaceHTML(selector, result)
            break
