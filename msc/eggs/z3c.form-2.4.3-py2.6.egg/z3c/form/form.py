##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Form Implementation

$Id: form.py 114824 2010-07-18 18:58:01Z icemac $
"""
__docformat__ = "reStructuredText"
import sys
import zope.interface
import zope.component
import zope.event
import zope.lifecycleevent
from zope.publisher import browser
from zope.pagetemplate.interfaces import IPageTemplate
from zope.schema.fieldproperty import FieldProperty

from z3c.form import button, field, interfaces, util
from z3c.form.i18n import MessageFactory as _
from z3c.form import ptcompat


def applyChanges(form, content, data):
    changes = {}
    for name, field in form.fields.items():
        # If the field is not in the data, then go on to the next one
        if name not in data:
            continue
        # If the value is NOT_CHANGED, ignore it, since the widget/converter
        # sent a strong message not to do so.
        if data[name] is interfaces.NOT_CHANGED:
            continue
        # Get the datamanager and get the original value
        dm = zope.component.getMultiAdapter(
            (content, field.field), interfaces.IDataManager)
        # Only update the data, if it is different
        # Or we can not get the original value, in which case we can not check
        # Or it is an Object, in case we'll never know
        if (not dm.canAccess() or
            dm.query() != data[name] or
            zope.schema.interfaces.IObject.providedBy(field.field)):
            dm.set(data[name])
            # Record the change using information required later
            changes.setdefault(dm.field.interface, []).append(name)
    return changes


def extends(*args, **kwargs):
    frame = sys._getframe(1)
    f_locals = frame.f_locals
    if not kwargs.get('ignoreFields', False):
        f_locals['fields'] = field.Fields()
        for arg in args:
            f_locals['fields'] += getattr(arg, 'fields', field.Fields())
    if not kwargs.get('ignoreButtons', False):
        f_locals['buttons'] = button.Buttons()
        for arg in args:
            f_locals['buttons'] += getattr(arg, 'buttons', button.Buttons())
    if not kwargs.get('ignoreHandlers', False):
        f_locals['handlers'] = button.Handlers()
        for arg in args:
            f_locals['handlers'] += getattr(arg, 'handlers', button.Handlers())


@zope.component.adapter(interfaces.IActionErrorEvent)
def handleActionError(event):
    # Only react to the event, if the form is a standard form.
    if not (interfaces.IFormAware.providedBy(event.action) and
            interfaces.IForm.providedBy(event.action.form)):
        return
    # If the error was widget-specific, look up the widget.
    widget = None
    if isinstance(event.error, interfaces.WidgetActionExecutionError):
        widget = event.action.form.widgets[event.error.widgetName]
    # Create an error view for the error.
    action = event.action
    form = action.form
    errorView = zope.component.getMultiAdapter(
        (event.error.error, action.request, widget,
         getattr(widget, 'field', None), form, form.getContent()),
        interfaces.IErrorViewSnippet)
    errorView.update()
    # Assign the error view to all necessary places.
    if widget:
        widget.error = errorView
    form.widgets.errors += (errorView,)
    # If the form supports the ``formErrorsMessage`` attribute, then set the
    # status to it.
    if hasattr(form, 'formErrorsMessage'):
        form.status = form.formErrorsMessage


class BaseForm(browser.BrowserPage):
    """A base form."""
    zope.interface.implements(interfaces.IForm,
                              interfaces.IFieldsForm)

    fields = field.Fields()

    label = None
    labelRequired = _('<span class="required">*</span>&ndash; required')
    prefix = 'form.'
    status = ''
    template = None
    widgets  = None

    mode = interfaces.INPUT_MODE
    ignoreContext = False
    ignoreRequest = False
    ignoreReadonly = False

    def getContent(self):
        '''See interfaces.IForm'''
        return self.context

    def updateWidgets(self):
        '''See interfaces.IForm'''
        self.widgets = zope.component.getMultiAdapter(
            (self, self.request, self.getContent()), interfaces.IWidgets)
        self.widgets.mode = self.mode
        self.widgets.ignoreContext = self.ignoreContext
        self.widgets.ignoreRequest = self.ignoreRequest
        self.widgets.ignoreReadonly = self.ignoreReadonly
        self.widgets.update()

    @property
    def requiredInfo(self):
        if self.labelRequired is not None and self.widgets is not None \
            and self.widgets.hasRequiredFields:
            return zope.i18n.translate(self.labelRequired, context=self.request)

    def extractData(self, setErrors=True):
        '''See interfaces.IForm'''
        self.widgets.setErrors = setErrors
        return self.widgets.extract()

    def update(self):
        '''See interfaces.IForm'''
        self.updateWidgets()

    def render(self):
        '''See interfaces.IForm'''
        # render content template
        if self.template is None:
            template = zope.component.getMultiAdapter((self, self.request),
                IPageTemplate)
            return template(self)
        return self.template()


class DisplayForm(BaseForm):

    zope.interface.implements(interfaces.IDisplayForm)

    mode = interfaces.DISPLAY_MODE
    ignoreRequest = True


class Form(BaseForm):
    """The Form."""
    zope.interface.implements(
        interfaces.IInputForm, interfaces.IButtonForm,
        interfaces.IHandlerForm, interfaces.IActionForm)

    buttons = button.Buttons()

    method = FieldProperty(interfaces.IInputForm['method'])
    enctype = FieldProperty(interfaces.IInputForm['enctype'])
    acceptCharset = FieldProperty(interfaces.IInputForm['acceptCharset'])
    accept = FieldProperty(interfaces.IInputForm['accept'])

    actions = FieldProperty(interfaces.IActionForm['actions'])
    refreshActions = FieldProperty(interfaces.IActionForm['refreshActions'])

    # common string for use in validation status messages
    formErrorsMessage = _('There were some errors.')

    @property
    def action(self):
        """See interfaces.IInputForm"""
        return self.request.getURL()

    @property
    def name(self):
        """See interfaces.IInputForm"""
        return self.prefix.strip('.')

    @property
    def id(self):
        return self.name.replace('.', '-')

    def updateActions(self):
        self.actions = zope.component.getMultiAdapter(
            (self, self.request, self.getContent()), interfaces.IActions)
        self.actions.update()

    def update(self):
        super(Form, self).update()
        self.updateActions()
        self.actions.execute()
        if self.refreshActions:
            self.updateActions()

    def __call__(self):
        self.update()

        # Don't render anything if we are doing a redirect
        if self.request.response.getStatus() in (300, 301, 302, 303, 304, 305, 307,):
            return u''

        return self.render()


class AddForm(Form):
    """A field and button based add form."""
    zope.interface.implements(interfaces.IAddForm)

    ignoreContext = True
    ignoreReadonly = True

    _finishedAdd = False

    @button.buttonAndHandler(_('Add'), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    def createAndAdd(self, data):
        obj = self.create(data)
        zope.event.notify(zope.lifecycleevent.ObjectCreatedEvent(obj))
        self.add(obj)
        return obj

    def create(self, data):
        raise NotImplementedError

    def add(self, object):
        raise NotImplementedError

    def nextURL(self):
        raise NotImplementedError

    def render(self):
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())
            return ""
        return super(AddForm, self).render()


class EditForm(Form):
    """A simple edit form with an apply button."""
    zope.interface.implements(interfaces.IEditForm)

    successMessage = _('Data successfully updated.')
    noChangesMessage = _('No changes were applied.')

    def applyChanges(self, data):
        content = self.getContent()
        changes = applyChanges(self, content, data)
        # ``changes`` is a dictionary; if empty, there were no changes
        if changes:
            # Construct change-descriptions for the object-modified event
            descriptions = []
            for interface, names in changes.items():
                descriptions.append(
                    zope.lifecycleevent.Attributes(interface, *names))
            # Send out a detailed object-modified event
            zope.event.notify(
                zope.lifecycleevent.ObjectModifiedEvent(content, *descriptions))
        return changes

    @button.buttonAndHandler(_('Apply'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage


class FormTemplateFactory(object):
    """Form template factory."""

    def __init__(self, filename, contentType='text/html', form=None,
        request=None):
        self.template = ptcompat.ViewPageTemplateFile(
            filename, content_type=contentType)
        zope.component.adapter(
            util.getSpecification(form),
            util.getSpecification(request))(self)
        zope.interface.implementer(IPageTemplate)(self)

    def __call__(self, form, request):
        return self.template
