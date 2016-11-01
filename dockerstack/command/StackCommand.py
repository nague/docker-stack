from dockerstack.docopt_command import get_handler
from dockerstack.utils import get_version_info
from inspect import getdoc


class StackCommand(object):
    """An utility to Dockerize your applications and generate minimal docker
    requires files.

    Usage:
      docker-stack [options] [COMMAND] [ARGS...]
      docker-stack -h|--help

    Commands:
      build              Build a new or existing project
      help               Get help on a command
      ps                 List all created projects
      rm                 Remove one or more projects
      start              Build and start a new project
      stop               Stop docker container(s) for the current project
      version            Display version number

    Run 'docker-stack COMMAND --help' for more information on a command.
    """

    # =======================
    # Building process method
    # =======================
    def build(self, project, options):
        """
        Build a new or existing project

        Usage: build [options] [PROJECT_NAME]

        Options:
          -f, --file FILE             Specify an alternate stack file.
                                      (default: docker-stack.yml)
        """
        if options.get('PROJECT_NAME'):
            project_name = options.get('PROJECT_NAME')
        else:
            project_name = raw_input("Please enter the project name: ")
        project.build(
            project_name=project_name,
            force_rebuild=True,
            config_file=(options.get('--file') or None)
        )

    # ====================
    # Help-printing method
    # ====================
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
        List all created projects

        Usage: ps [ARGS...]
        """
        pass

    # ==================================
    # Remove one or more projects method
    # ==================================
    def rm(self, project, options):
        """
        Remove one or more projects

        Usage: rm [PROJECTS...]
        """
        if options.get('PROJECTS'):
            projects = list(set(options.get('PROJECTS')))
        else:
            projects = [raw_input("Please enter the project name: ")]
        project.remove(projects=projects)

    # ===================================
    # Start building a new project method
    # ===================================
    def start(self, project, options):
        """
        Build and start a new project.

        Usage: start [options] [PROJECT_NAME]

        Options:
          -f, --file FILE             Specify an alternate stack file.
                                      (default: docker-stack.yml)
        """
        if options.get('PROJECT_NAME'):
            project_name = options.get('PROJECT_NAME')
        else:
            project_name = raw_input("Please enter the project name: ")
        project.build(
            project_name=project_name,
            config_file=(options.get('--file') or None)
        )
        project.start()

    # =======================================================
    # Stop docker container(s) for the current project method
    # =======================================================
    def stop(self, project, options):
        """
        Stop docker container(s) for the current project

        Usage: stop [PROJECT_NAME]
        """
        if options.get('PROJECT_NAME'):
            project_name = options.get('PROJECT_NAME')
        else:
            project_name = raw_input("Please enter the project name: ")
        project.stop(project_name=project_name)

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
