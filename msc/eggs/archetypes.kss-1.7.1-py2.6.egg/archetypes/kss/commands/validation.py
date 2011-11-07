from Acquisition import aq_inner

from kss.core.kssview import CommandSet


class ValidationCommands(CommandSet):

    __allow_access_to_unprotected_subobjects__ = 1

    def issueFieldError(self, fieldname, error, warning_only=False):
        'Issue this error message for the field'
        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')
        selector = ksscore.getCssSelector('div#archetypes-fieldname-%s div.fieldErrorBox' % fieldname)
        if error and not warning_only:
            ksscore.replaceInnerHTML(selector, error)
            errorklass = ' error'
        elif error and warning_only:
            ksscore.clearChildNodes(selector)
            errorklass = ' error warning'
        else:
            ksscore.clearChildNodes(selector)
            errorklass = ''
        klass = "field%s Archetypes%sfield" % (errorklass, fieldname)
        kssattr = context.restrictedTraverse('kss_field_decorator_view').getKssClasses(fieldname)
        if kssattr:
            klass += ' ' + kssattr
        # set the field style in the required way
        ksscore.setAttribute(
            ksscore.getHtmlIdSelector('archetypes-fieldname-%s' % fieldname),
            'class', klass)
