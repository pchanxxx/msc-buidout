import os
import sys
import doctest
import unittest

from zope import component
from zope import interface
from zope.component import testing
from zope.app.testing.functional import ZCMLLayer
import zope.traversing.adapters
import zope.traversing.namespace
import zope.publisher.interfaces.browser
import z3c.form.testing

import plone.z3cform.templates

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

def create_eventlog(event=interface.Interface):
    value = []
    @component.adapter(event)
    def log(event):
        value.append(event)
    component.provideHandler(log)
    return value

def setup_defaults():
    # Set up z3c.form defaults
    z3c.form.testing.setupFormDefaults()

    # Make traversal work; register both the default traversable
    # adapter and the ++view++ namespace adapter
    component.provideAdapter(
        zope.traversing.adapters.DefaultTraversable, [None])
    component.provideAdapter(
        zope.traversing.namespace.view, (None, None), name='view')

    # Setup ploneform macros, simlulating the ZCML directive
    plone.z3cform.templates.Macros.index = ViewPageTemplateFile(plone.z3cform.templates.path('macros.pt'))

    component.provideAdapter(
        plone.z3cform.templates.Macros,
        (None, None),
        zope.publisher.interfaces.browser.IBrowserView,
        name='ploneform-macros')

    # setup plone.z3cform templates
    from zope.pagetemplate.interfaces import IPageTemplate

    component.provideAdapter(
        plone.z3cform.templates.wrapped_form_factory,
        (None, None),
        IPageTemplate)

    component.provideAdapter(
        z3c.form.error.ErrorViewSnippet,
        (None, None, None, None, None, None),
        z3c.form.interfaces.IErrorViewSnippet)

testing_zcml_path = os.path.join(os.path.dirname(__file__), 'testing.zcml')
testing_zcml_layer = ZCMLLayer(
    testing_zcml_path, 'plone.z3cform', 'testing_zcml_layer')

def test_suite():
    layout_txt = doctest.DocFileSuite('layout.txt')
    layout_txt.layer = testing_zcml_layer

    inputs_txt = doctest.DocFileSuite('inputs.txt')
    inputs_txt.layer = testing_zcml_layer

    fieldsets_txt = doctest.DocFileSuite('fieldsets/README.txt')
    fieldsets_txt.layer = testing_zcml_layer

    if sys.version_info[:2] > (2, 4):
        # Zope 2.10 raises TraversalError instead of LocationError
        traversal_txt = doctest.DocFileSuite('traversal.txt')
        traversal_txt.layer = testing_zcml_layer
    else:
        import tempfile
        tmp = tempfile.NamedTemporaryFile()
        test = open(os.path.join(os.path.dirname(__file__), 'traversal.txt')).read()
        tmp.write(test.replace('LocationError', 'TraversalError'))
        tmp.flush()
        traversal_txt = doctest.DocFileSuite(tmp.name, module_relative=False)
        traversal_txt.layer = testing_zcml_layer        

    return unittest.TestSuite([
        layout_txt, inputs_txt, fieldsets_txt, traversal_txt,

        doctest.DocFileSuite(
           'crud/README.txt',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        doctest.DocFileSuite(
           'crud/batch.txt',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        doctest.DocTestSuite(
           'plone.z3cform.crud.crud',
           setUp=testing.setUp, tearDown=testing.tearDown,
           ),

        ])
