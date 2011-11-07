from kss.base.plugin import Plugin

def core_demos():
    try:
        from kss.demo.resource import (
            KSSDemo,
            KSSSeleniumTestDirectory,
            )
    except ImportError: # no demo package installed
        return Plugin()

    class CoreDemos(Plugin):

        zope_demos = (
            KSSDemo('', '', "basic_commands.html", "Change tag content"),
            KSSDemo('', '', "two_selects.html", "Two selects"),
            KSSDemo('', '', "autoupdate.html", "Auto update"),
            KSSDemo('', '', "inline_edit.html", "Inline edit"),
            KSSDemo('', '', "cancel_submit.html", "Cancel Submit Click"),
            KSSDemo('', '', "tree.html", "Tree"),
            KSSDemo('', '', "more_selectors.html", "More complex selectors"),
            KSSDemo('', '', "two_select_revisited.html", "Master-slave selects revisited"),
            KSSDemo('', '', "form_submit.html", "Form submit"),
            KSSDemo('', '', "error_handling.html", "Error handling"),
            KSSDemo('', '', "preventdefault.html", "Preventdefault (a.k.a. Safari workarounds)"),
            KSSDemo('', '', "html_inserts.html", "HTML insertions (Change tag content returns)"),
            KSSDemo('', '', "client-server-protocol", "Client server protocol"),
            KSSDemo('', 'Selectors', 'selectors.html', 'Parent node selector'),
            KSSDemo('', 'Core events', "kss_evt_preventbubbling.html", "Prevent bubbling KSS event parameter"),
            KSSDemo('', 'Core events', "kss_keyevents.html", "Key events"),
            KSSDemo('', 'Commands/Actions', "ca_focus.html", "Focus"),
            KSSDemo('', 'Commands/Actions', "ca_blur.html", "Blur"),
            KSSDemo('', 'Commands/Actions', "actions.html", "Class actions: toggle, add, remove"),
            KSSDemo('', 'Commands/Actions', "ca_cancel.html", "action-cancel"),
            KSSDemo('', 'Commands/Actions', "ca_kssattr.html", "setKssAttribute"),
            # XXX this should go to the other plugin wuth all its stuff
            KSSDemo('Effects', '', "effects.html", "Effects"),
            )

        # directories are relative from the location of this .py file
        zope_selenium_testsuites = (
            KSSSeleniumTestDirectory('selenium_tests'),
            )
    return CoreDemos()
