from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from dockerstack.Project import Project
from dockerstack.command.StackCommand import StackCommand
from dockerstack.docopt_command import DocoptDispatcher
from dockerstack.docopt_command import NoSuchCommand
from . import signals
from .utils import get_version_info

import os
import sys
import functools
import logging
import re
import inspect
import yaml

log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stderr)


def main():
    command = dispatch()

    try:
        command()
    except (KeyboardInterrupt, signals.ShutdownException):
        log.error("Aborting.")
        sys.exit(1)


def dispatch():
    setup_logging()
    dispatcher = DocoptDispatcher(StackCommand, {'options_first': True, 'version': get_version_info()})

    try:
        options, handler, command_options = dispatcher.parse(sys.argv[1:])
    except NoSuchCommand as e:
        commands = "\n".join(parse_doc_section("commands:", inspect.getdoc(e.supercommand)))
        log.error("No such command: %s\n\n%s", e.command, commands)
        sys.exit(1)

    return functools.partial(perform_command, options, handler, command_options)


def perform_command(options, handler, command_options):
    if options['COMMAND'] in ('help', 'version'):
        handler(command_options)
        return

    try:
        if os.getuid() == 0:
            raise Exception("Since docker-stack is a user command, there is no need to execute it with superuser "
                            "permissions.\nIf you're having permission errors when using 'docker-stack' without sudo.\n"
                            "Please spend a few minutes learning more about how your system should work and make any "
                            "necessary repairs.")

        project = Project()
        handler(StackCommand(), project, command_options)
    except yaml.YAMLError, exc:
        print "Error in configuration file:", exc
    except Exception as e:
        print e.message


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

    # Disable requests logging
    logging.getLogger("requests").propagate = False


# stolen from docopt master
def parse_doc_section(name, source):
    pattern = re.compile('^([^\n]*' + name + '[^\n]*\n?(?:[ \t].*?(?:\n|$))*)', re.IGNORECASE | re.MULTILINE)
    return [s.strip() for s in pattern.findall(source)]
