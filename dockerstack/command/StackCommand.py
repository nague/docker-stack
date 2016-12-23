import os
import docker

from dockerstack.docopt_command import get_handler
from dockerstack.utils import get_version_info
from dockerstack.utils import clean_name
from inspect import getdoc
from prettytable import PrettyTable


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
        List all created projects

        Usage: ps [ARGS...]
        """
        home = os.path.join(os.path.expanduser('~'), 'DockerStackProjects')
        dirnames = []
        for dirname in os.listdir(home):
            dirnames.append(clean_name(dirname))
        client = docker.from_env()
        containers = client.containers.list(all)
        t = PrettyTable(['NAME', 'ID', 'STATUS'])
        for container in containers:
            container_name = container.name
            container_name = container_name.split('_')
            if container_name[0] in dirnames:
                t.add_row([container.name, container.id, container.status])
        print t

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
