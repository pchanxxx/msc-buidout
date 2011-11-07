from zope.interface import Interface, implements, classImplements
from zope.component import adapts, provideAdapter
from Products.Archetypes.atapi import StringField, StringWidget
from Products.ATContentTypes.content.document import ATDocument
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.tests.base import TestCase


class IFoo(Interface):
    """ marker interface """


class FooField(ExtensionField, StringField):
    """ extension field """


class Extender(object):
    implements(ISchemaExtender)
    adapts(IFoo)

    fields = [
        FooField('foo',
            widget = StringWidget(label='foo', description='foo!')),
        FooField('bar',
            index_method = 'title_or_id',
            widget = StringWidget(label='bar', description='bar!')),
        FooField('hmm',
            index_method = lambda: 'hmm',
            widget = StringWidget(label='hmm', description='hmm!')),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class AccessorTests(TestCase):

    def afterSetUp(self):
        classImplements(ATDocument, IFoo)
        provideAdapter(Extender, name=u'foo')

    def testDefaultIndexAccessor(self):
        doc = self.folder[self.folder.invokeFactory('Document', 'doc', foo=23)]
        field = doc.getField('foo')
        self.assertEqual(field.getIndexAccessor(doc)(), 23)

    def testNamedIndexAccessor(self):
        doc = self.folder[self.folder.invokeFactory('Document', 'doc', bar=23)]
        field = doc.getField('bar')
        self.assertEqual(field.getAccessor(doc)(), 23)
        self.assertEqual(field.getIndexAccessor(doc)(), 'doc')

    def testInvalidIndexAccessor(self):
        doc = self.folder[self.folder.invokeFactory('Document', 'doc', hmm=23)]
        field = doc.getField('hmm')
        self.assertRaises(ValueError, field.getIndexAccessor, doc)


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
