import zope.i18nmessageid
MessageFactory = zope.i18nmessageid.MessageFactory('plone.z3cform')

# backport bug fixes
from bbb import term
term.apply_patch()