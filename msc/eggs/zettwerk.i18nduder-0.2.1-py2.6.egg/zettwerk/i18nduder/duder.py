# -*- coding: utf-8 -*-
import os
import os.path
import optparse

from commands import create, update, mo, find


class UnformatedDescriptionFormatter(optparse.IndentedHelpFormatter):
    """ formater class to have unformated description output """

    def format_description(self, description):
        return description


def handle_command(command, options, parser):
    if command == 'create':
        create(options, parser)
    if command == 'update':
        update(options, parser)
    if command == 'find':
        find(options, parser)
    if command == 'mo':
        mo(options, parser)


def main():
    usage = 'usage: %prog command -p package.name or --help for details'
    description = u'''Available commands:
  create\t\tCreate the locales folder and/or add given languages
  update\t\tCall rebuild-pot and sync
  mo\t\t\tCall msgfmt to build the mo files
  find\t\t\tFind untranslated strings (domain independent)
'''
    parser = optparse.OptionParser(usage=usage,
                                   description=description,
                                   formatter=UnformatedDescriptionFormatter())

    parser.add_option('-p', '--package',
                      help="Name of the package")
    parser.add_option('-d', '--domain',
                      help="Name of the i18n domain. Only needed if it is " \
                          "different from the package name.")
    parser.add_option('-l', '--languages',
                      help="List of comma-separated names of language " \
                          "strings. Only used for create command. For " \
                          "example: -l en,de")

    options, args = parser.parse_args()
    if not args:
        parser.error('no commands given')

    if not options.package:
        parser.error('no package given')

    working_dir = os.getcwd()

    for command in args:
        os.chdir(working_dir)
        handle_command(command, options, parser)
