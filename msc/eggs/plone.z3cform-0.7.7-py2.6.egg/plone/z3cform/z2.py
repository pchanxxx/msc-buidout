from zope import interface

from zope.publisher.browser import isCGI_NAME
from zope.publisher.interfaces.browser import IBrowserApplicationRequest

from zope.i18n.interfaces import IUserPreferredLanguages, IUserPreferredCharsets
from zope.i18n.locales import locales, LoadLocaleError

import z3c.form.interfaces

class IFixedUpRequest(interface.Interface):
    """Marker interface used to ensure we don't fix up the request twice
    """

class IProcessedRequest(interface.Interface):
    """Marker interface used to ensure we don't process the request inputs
    twice.
    """

# Safer versions of the functions in Products.Five.browser.decode

def processInputs(request, charsets=None):
    """Process the values in request.form to decode strings to unicode, using
    the passed-in list of charsets. If none are passed in, look up the user's
    preferred charsets. The default is to use utf-8.
    """

    if IProcessedRequest.providedBy(request):
        return

    if charsets is None:
        envadapter = IUserPreferredCharsets(request, None)
        if envadapter is None:
            charsets = ['utf-8']
        else:
            charsets = envadapter.getPreferredCharsets() or ['utf-8']

    for name, value in request.form.items():
        if not (isCGI_NAME(name) or name.startswith('HTTP_')):
            if isinstance(value, str):
                request.form[name] = _decode(value, charsets)
            elif isinstance(value, (list, tuple,)):
                newValue = []
                for val in value:
                    if isinstance(val, str):
                        val = _decode(val, charsets)
                    newValue.append(val)

                if isinstance(value, tuple):
                    newValue = tuple(value)

                request.form[name] = newValue

    interface.alsoProvides(request, IProcessedRequest)

def _decode(text, charsets):
    for charset in charsets:
        try:
            text = unicode(text, charset)
            break
        except UnicodeError:
            pass
    return text

# This is ripped from zope.publisher.http.HTTPRequest; it is only
# necessary in Zope < 2.11
def setup_locale(request):
    envadapter = IUserPreferredLanguages(request, None)
    if envadapter is None:
        return None

    langs = envadapter.getPreferredLanguages()
    for httplang in langs:
        parts = (httplang.split('-') + [None, None])[:3]
        try:
            return locales.getLocale(*parts)
        except LoadLocaleError:
            # Just try the next combination
            pass
    else:
        # No combination gave us an existing locale, so use the default,
        # which is guaranteed to exist
        return locales.getLocale(None, None, None)

# XXX Add a getURL method on the request object; this is only necessary in
# Zope < 2.11
def add_getURL(request):
    def getURL(level=0, path_only=False):
        assert level == 0 and path_only == False
        return request['ACTUAL_URL']
    request.getURL = getURL

def switch_on(view, request_layer=z3c.form.interfaces.IFormLayer):
    """Fix up the request and apply the given layer. This is mainly useful
    in Zope < 2.10 when using a wrapper layout view.
    """

    request = view.request

    if (not IFixedUpRequest.providedBy(request) and
        not IBrowserApplicationRequest.providedBy(request)
    ):

        interface.alsoProvides(request, IFixedUpRequest)
        interface.alsoProvides(request, request_layer)

        if getattr(request, 'locale', None) is None:
            request.locale = setup_locale(request)

        if not hasattr(request, 'getURL'):
            add_getURL(request)
