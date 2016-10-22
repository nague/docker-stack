import argparse
import logging
import os
import shutil
from git import Repo
from Docker import Docker
from DockerStackConfig import DockerStackConfig


class DockerStack(argparse.Action):
    # Define properties/constants
    args = []
    VERSION = 1.0
    PROJECT_NAME = 'Docker Stack'
    PROJECT_MAINTAINER = 'Kaliop Canada'
    PROJECTS_DIRECTORY = './projects/'
    TEMPLATES_DIRECTORY = './templates/'
    SITE_DIRECTORY = 'www'
    CONFIG_FILE = 'docker-stack.ini'
    LOG = logging.getLogger(__name__)

    # Magic call method
    def __call__(self, parser, namespace, values, option_string=None):
        print '%r %r %r' % (namespace, values, option_string)

    # Constructor
    def __init__(self, parser):
        self.parser = parser
        self.args = parser.parse_args()
        logging.basicConfig(filename='stack.log', level=logging.DEBUG)

        # Welcome message when stating app
        print "========= Welcome to %s by Kaliop project ==========\n" % self.PROJECT_NAME

        # Create 'projects' directory when initializing app
        if not os.path.exists(self.PROJECTS_DIRECTORY):
            os.makedirs(self.PROJECTS_DIRECTORY)
            self.LOG.info('Create \'projects\' directory')

        super(DockerStack, self).__init__(self, parser)

    # Start building a new project
    def start(self):
        # 1. Build new project
        self.build()
        # 2. Start DockerCompose

    # Building process
    def build(self):
        # 1. Ask for project name if not provided
        project = self.args.s or self.args.b
        if project is 1:
            project = raw_input("Please enter the project name: ")
        project_directory = os.path.join(self.PROJECTS_DIRECTORY, project)

        # 2. Create project main directory
        if not os.path.exists(project_directory):
            os.makedirs(project_directory)
            self.LOG.info('Create main directory for project: %s' % project)

        # 3. Symlink existing sources or Git clone project to self.SITE_DIRECTORY directory
        if not os.path.exists(os.path.join(project_directory, self.SITE_DIRECTORY)):
            print 'You have 2 possibilities (Cloning a Git repository or create a symlink from existing sources).'
            cloning = raw_input('Do you want have project sources? (Y/n): ').lower() or 'y'
            if cloning is 'y':
                source = raw_input("Please provide the full path of your sources directory (e.g. 'pwd'): ")
                validation = raw_input(
                    "We are about to create a symlink from '%s' to '%s', do you accept (Y/n): " % (
                        source, os.path.join(project_directory, self.SITE_DIRECTORY))).lower() or 'y'
                if validation is 'y':
                    os.symlink(source, os.path.join(project_directory, self.SITE_DIRECTORY))
                    self.LOG.info(
                        'Create symlink from %s to %s' % (source, os.path.join(project_directory, self.SITE_DIRECTORY)))
            else:
                source = raw_input('Please provide a Git valid URL (http or ssh): ')
                branch = raw_input('From witch branch do you want to clone the repository (default: master): ')
                validation = raw_input(
                    "We are about to clone your repo '%s' from branch '%s', do you accept (Y/n): " % (
                        source, branch)).lower() or 'y'
                if validation is 'y':
                    Repo.clone_from(source, os.path.join(project_directory, self.SITE_DIRECTORY))
                    self.LOG.info(
                        'Cloning Git repository from %s to %s' % (
                            source, os.path.join(project_directory, self.SITE_DIRECTORY)))

        # 4. Read 'docker-stack.ini' file if exists
        config_path = os.path.join(project_directory, self.SITE_DIRECTORY, self.CONFIG_FILE)
        docker_stack_config = DockerStackConfig(config_path)
        if not os.path.exists(config_path):
            # Build 'docker-stack.ini' file
            pass
            # config = docker_stack_config.parse_config()
            # docker_stack_config.build_php_ini(os.path.join('php', 'php.ini'),
            #                                   os.path.join(project_directory, self.SITE_DIRECTORY, 'conf', 'php',
            #                                                'php.ini'))

        # 5. Generate Docker files
        docker = Docker(project_directory)
        destination = os.path.join(project_directory, self.SITE_DIRECTORY, 'Dockerfile')
        if not os.path.exists(destination):
            config = docker_stack_config.parse_config()
            config['docker']['maintainer'] = self.PROJECT_MAINTAINER
            docker.build(
                os.path.join('docker', 'Dockerfile'),
                os.path.join(project_directory, self.SITE_DIRECTORY, 'Dockerfile'),
                config
            )

    # Remove one or more projects
    def remove(self):
        # Remove all projects
        if self.args.rm is 1:
            shutil.rmtree(self.PROJECTS_DIRECTORY)
            print "All projects removed successfully"
            self.LOG.info('Deleting all projects')
        # Remove projects
        elif isinstance(self.args.rm, list):
            for project in self.args.rm:
                if os.path.exists(os.path.join(self.PROJECTS_DIRECTORY, project)):
                    shutil.rmtree(os.path.join(self.PROJECTS_DIRECTORY, project))
                    print "Project '%s' removed successfully" % project
                    self.LOG.info('Deleting %s project' % project)
        # Remove single project
        else:
            if os.path.exists(os.path.join(self.PROJECTS_DIRECTORY, self.args.rm)):
                shutil.rmtree(os.path.join(self.PROJECTS_DIRECTORY, self.args.rm))
                print "Project '%s' removed successfully" % self.args.rm
                self.LOG.info('Deleting %s project' % self.args.rm)

    # Show version number
    def version(self):
        print '%s version %s' % (self.PROJECT_NAME, self.VERSION)
