
from kss.demo.interfaces import (
    IKSSDemoResource,
    IKSSSeleniumTestResource,
    )
from kss.demo.resource import (
    KSSDemo,
    KSSSeleniumTestDirectory,
    )
from zope.interface import implements
     
# Create a mesh of provided interfaces
# This is needed, because an utility must have a single interface.
class IResource(IKSSDemoResource, IKSSSeleniumTestResource):
    pass

class KSSCoreDemos(object):
    implements(IResource)

    demos = (
        KSSDemo('', '', "loglevel.html", "Log Level"),
        KSSDemo('', '', "basic_commands.html", "Change tag content"),
        KSSDemo('', '', "two_selects.html", "Two selects"),
        KSSDemo('', '', "autoupdate.html", "Auto update"),
        KSSDemo('', '', "inline_edit.html", "Inline edit"),
        KSSDemo('', '', "cancel_submit.html", "Cancel Submit Click"),
        KSSDemo('', '', "tree.html", "Tree"),
        KSSDemo('', '', "more_selectors.html", "More complex selectors"),
        KSSDemo('', '', "two_select_revisited.html", "Master-slave selects revisited"),
        KSSDemo('', '', "form_submit.html", "Form submit"),
        KSSDemo('', '', "effects.html", "Effects"),
        KSSDemo('', '', "error_handling.html", "Error handling"),
        KSSDemo('', '', "preventdefault.html", "Preventdefault (a.k.a. Safari workarounds)"),
        KSSDemo('', '', "html_inserts.html", "HTML insertions (Change tag content returns)"),
        KSSDemo('', '', "client-server-protocol", "Client server protocol"),
##      KSSDemo('', '',  "draganddrop.html", "Scriptaculous drag and drop"),
        KSSDemo('', 'Selectors', 'selectors.html', 'Parent node selector'),
        KSSDemo('', 'Core events', "kss_evt_preventbubbling.html", "Prevent bubbling KSS event parameter"),
        KSSDemo('', 'Core events', "kss_keyevents.html", "Key events"),
        KSSDemo('', 'Commands/Actions', "ca_focus.html", "Focus"),
        KSSDemo('', 'Commands/Actions', "ca_blur.html", "Blur"),
        KSSDemo('', 'Commands/Actions', "actions.html", "Class actions: toggle, add, remove"),
        KSSDemo('', 'Commands/Actions', "ca_cancel.html", "action-cancel"),
        KSSDemo('', 'Commands/Actions', "ca_kssattr.html", "setKssAttribute"),
        )

    # directories are relative from the location of this .py file
    selenium_tests = (
        KSSSeleniumTestDirectory('selenium_tests'),
        )
