from dockerstack.docopt_command import get_handler
from dockerstack.utils import get_version_info
from inspect import getdoc


class StackCommand(object):
    """Define and run multi-container applications with Docker.

    Usage:
      docker-stack [-p <arg>...] [options] [COMMAND] [ARGS...]
      docker-stack -h|--help

    Options:
      -p, --project-name NAME     Specify the project name

    Commands:
      build              Build a new or existing project
      help               Get help on a command
      ps                 List all created projects
      rm                 Remove one or more projects
      start              Build and start a new project
      stop               Stop docker container(s) for the current project
      version            Display version number
    """

    # =======================
    # Building process method
    # =======================
    def build(self, project):
        """
        Build a new or existing project

        Usage: build [PROJECT...]
        """
        project.build

    # ====================
    # Help-printing method
    # ====================
    @classmethod
    def help(cls, options):
        """
        Get help on a command.

        Usage: help [COMMAND]
        """
        if options['COMMAND']:
            subject = get_handler(cls, options['COMMAND'])
        else:
            subject = cls

        print getdoc(subject)

    # ================================
    # List all created projects method
    # ================================
    def ps(self, project, options):
        """

        """
        pass

    # ==================================
    # Remove one or more projects method
    # ==================================
    def rm(self, project, options):
        """
        Remove one or more projects

        Usage: rm [PROJECT...]
        """
        project.remove()

    # ===================================
    # Start building a new project method
    # ===================================
    def start(self, project, options):
        """
        Build and start a new project.

        Usage: start [PROJECT...]
        """
        project.build
        print "\n"
        project.start()

    # =======================================================
    # Stop docker container(s) for the current project method
    # =======================================================
    def stop(self, project, options):
        """

        """
        pass

    # ==========================
    # Show version number method
    # ==========================
    @classmethod
    def version(cls, options):
        """
        Display version number.

        Usage: version
        """
        print get_version_info()
