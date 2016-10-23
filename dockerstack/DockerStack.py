import argparse
import logging
import os
import shutil
from git import Repo
from Builder import Builder
from DockerStackConfig import DockerStackConfig
from DockerCompose import DockerCompose


class DockerStack(argparse.Action):
    # Define properties/constants
    args = []
    VERSION = 1.0
    PROJECT_NAME = 'Docker Stack'
    PROJECT_MAINTAINER = 'Kaliop Canada'
    PROJECTS_DIRECTORY = os.path.join(os.getcwd(), 'projects')
    TEMPLATES_DIRECTORY = './templates/'
    SITE_DIRECTORY = 'www'
    CONFIG_FILE = 'docker-stack.ini'
    DOCKERFILE_FILE = 'Dockerfile'
    DOCKER_COMPOSE_FILE = 'docker-compose.yml'
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

        # DockerCompose
        self.docker_compose = DockerCompose()

        super(DockerStack, self).__init__(self, parser)

    # Start building a new project
    def start(self):
        # 1. Build new project
        project = self.build()
        # 2. Start DockerCompose
        os.chdir(os.path.join(self.PROJECTS_DIRECTORY, project))
        print self.docker_compose.start(project)

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

        # 4. Read 'docker-stack.ini' file if exists otherwise generate it
        config_path = os.path.join(project_directory, self.SITE_DIRECTORY, self.CONFIG_FILE)
        docker_stack_config = DockerStackConfig(config_path)
        if not os.path.exists(config_path):
            # Build 'docker-stack.ini' file
            pass
            # config = docker_stack_config.parse_config()
            # docker_stack_config.build_php_ini(os.path.join('php', 'php.ini'),
            #                                   os.path.join(project_directory, self.SITE_DIRECTORY, 'conf', 'php',
            #                                                'php.ini'))
        config = docker_stack_config.parse_config()

        # 5. Database
        db_dir = os.path.join(project_directory, 'db')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print "Directory '%s' created successfully!" % db_dir
        db_destination_file = os.path.join(db_dir, os.path.basename(config['db']))
        db_source_file = os.path.join(project_directory, self.SITE_DIRECTORY, config['db'])
        if os.path.exists(db_source_file) and not os.path.exists(db_destination_file):
            os.symlink(
                db_source_file,
                db_destination_file
            )
            print "Database '%s' mapped successfully from '%s' to '%s'" % (
                os.path.basename(config['db']),
                db_source_file,
                db_destination_file
            )

        # 6. Generate 'Dockerfile'
        builder = Builder(project_directory)
        destination = os.path.join(project_directory, self.DOCKERFILE_FILE)
        if not os.path.exists(destination):
            config['docker']['maintainer'] = self.PROJECT_MAINTAINER
            builder.build_dockerfile(
                os.path.join('docker', self.DOCKERFILE_FILE),
                destination,
                config['docker']
            )
        else:
            print 'Dockerfile already exists, do nothing!'

        # 7. Generate 'docker-compose.yml'
        destination = os.path.join(project_directory, self.DOCKER_COMPOSE_FILE)
        if not os.path.exists(destination):
            builder.build_docker_compose(
                os.path.join('docker', self.DOCKER_COMPOSE_FILE),
                destination,
                config['docker-compose']
            )

        return project

    # Stop one or more projects
    def stop(self):
        project = self.args.o
        self.docker_compose.stop(project)

    # Remove one or more projects
    def remove(self):
        project = self.args.rm
        # Remove all projects
        if project is 1:
            shutil.rmtree(self.PROJECTS_DIRECTORY)
            print "All projects removed successfully"
            self.LOG.info('Deleting all projects')
        # Remove multiple projects
        elif isinstance(project, list):
            for p in project:
                if os.path.exists(os.path.join(self.PROJECTS_DIRECTORY, p)):
                    shutil.rmtree(os.path.join(self.PROJECTS_DIRECTORY, p))
                    print "Project '%s' removed successfully" % p
                    self.LOG.info("Deleting '%s' project" % p)
        # Remove single project
        else:
            if os.path.exists(os.path.join(self.PROJECTS_DIRECTORY, project)):
                # Stop containers
                os.chdir(os.path.join(self.PROJECTS_DIRECTORY, project))
                print self.docker_compose.stop(project)
                print self.docker_compose.rm(project)
                # Remove project directory
                shutil.rmtree(os.path.join(self.PROJECTS_DIRECTORY, project))
                print "Project '%s' removed successfully" % project
                self.LOG.info('Deleting %s project' % project)
            else:
                print "The project '%s' does not exists!" % project

    # Show version number
    def version(self):
        print '%s version %s' % (self.PROJECT_NAME, self.VERSION)
