"""Monkey patch in a bug fix for Choice terms. No longer needed in z3c.form
2.0.
"""

import logging
import types
from zope.schema.interfaces import IContextSourceBinder

def patched_init(self, context, request, form, field, widget):
    self.context = context
    self.request = request
    self.form = form
    self.field = field
    self.widget = widget
    if field.vocabulary is None or IContextSourceBinder.providedBy(field.vocabulary):
        field = field.bind(context)
    self.terms = field.vocabulary

def apply_patch():
    try:
        import pkg_resources
        from z3c.form.term import ChoiceTerms
    except ImportError:
        return False

    if not isinstance(ChoiceTerms, types.TypeType):
        return False
    try:
        version = pkg_resources.get_distribution('z3c.form').version
    except AttributeError:
        return False

    if version != '1.9.0':
        return False

    logging.getLogger('plone.z3cform').warn("Monkey patching z3c.form.term.ChoiceTerms to correctly bind fields")
    ChoiceTerms.__init__ = patched_init
