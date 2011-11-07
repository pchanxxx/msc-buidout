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
            # List your demos here. 
            # (Second parameter can be a subcategory within the demo if needed.)
            KSSDemo('', 'Core syntax', 'binderids.html', 'Binder ids'),
            )

        # directories are relative from the location of this .py file
        zope_selenium_testsuites = (
            # if you only have one test directory, you
            # need not change anything here.
            KSSSeleniumTestDirectory('selenium_tests'),
            )
    return CoreDemos()

