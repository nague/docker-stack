import argparse
import logging
import os
import shutil
import string
from git import Repo
from Builder import Builder
from DockerStackConfig import DockerStackConfig
from DockerCompose import DockerCompose


class DockerStack(argparse.Action):
    # Define properties/constants
    args = []
    VERSION = 1.0
    PROJECT_NAME = '[DSK] Docker Stack'
    PROJECT_MAINTAINER = 'Kaliop'
    PROJECTS_DIRECTORY = os.path.join(os.getcwd(), 'projects')
    TEMPLATES_DIRECTORY = './templates/'
    SITE_DIRECTORY = 'www'
    CONFIG_FILE = 'docker-stack.ini'
    DOCKERFILE_FILE = 'Dockerfile'
    DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    PHP_INI_FILE = 'php.ini'
    DEFAULT_LIBS = ['wget', 'git', 'curl', 'zip']
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
        print "========= Welcome to %s by %s  ==========\n" % (self.PROJECT_NAME, self.PROJECT_MAINTAINER)

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
        print "\n"
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
            print 'Please choose one of the following:'
            print ' 1. Create a Symlink from existing sources (default)'
            print ' 2. Cloning a Git repository'
            cloning = raw_input('Enter your choose now: ') or 1
            print "\n"
            if int(cloning) is 1:
                source = raw_input("Please provide the full path of your sources directory (e.g. using 'pwd'):\n")
                validation = raw_input(
                    "We are about to create a symlink from '%s' to '%s', do you accept (Y/n): \n" % (
                        source, os.path.join(project_directory, self.SITE_DIRECTORY))).lower() or 'y'
                if validation is 'y':
                    os.symlink(source, os.path.join(project_directory, self.SITE_DIRECTORY))
                    print "Creating symlink... done\n"
                    self.LOG.info(
                        'Create symlink from %s to %s' % (source, os.path.join(project_directory, self.SITE_DIRECTORY)))
            else:
                source = raw_input('Please provide a Git valid URL (http or ssh): ')
                branch = raw_input(
                    'From witch branch do you want to clone the repository (default: master): ') or 'master'
                validation = raw_input(
                    "We are about to clone your repo '%s' from branch '%s', do you accept (Y/n): \n" % (
                        source, branch)).lower() or 'y'
                if validation is 'y':
                    Repo.clone_from(source, os.path.join(project_directory, self.SITE_DIRECTORY))
                    print "Cloning Git repository... done\n"
                    self.LOG.info(
                        'Cloning Git repository from %s to %s' % (
                            source, os.path.join(project_directory, self.SITE_DIRECTORY)))

        # 4. Read 'docker-stack.ini' file if exists otherwise generate it
        config_path = os.path.join(project_directory, self.SITE_DIRECTORY, self.CONFIG_FILE)
        docker_stack_config = DockerStackConfig(config_path)
        if not os.path.exists(config_path):
            # Build 'docker-stack.ini' file
            exit(1);
            # config = docker_stack_config.parse_config()
            # docker_stack_config.build_php_ini(os.path.join('php', 'php.ini'),
            #                                   os.path.join(project_directory, self.SITE_DIRECTORY, 'conf', 'php',
            #                                                'php.ini'))
        config = docker_stack_config.parse_config()

        # 5. Database
        db_dir = os.path.join(project_directory, 'db')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print "Creating directory '%s' ... done\n" % os.path.join('projects', project, 'db')
        db_destination_file = os.path.join(db_dir, os.path.basename(config['db']))
        db_source_file = os.path.join(project_directory, self.SITE_DIRECTORY, config['db'])
        if os.path.exists(db_source_file) and not os.path.exists(db_destination_file):
            print "Database file '%s' found" % os.path.basename(config['db'])
            os.symlink(
                db_source_file,
                db_destination_file
            )
            print "Mapping database ... done\n"

        # Builder
        builder = Builder(project_directory)

        # 6. Generate 'php.ini'
        conf_php_path = os.path.join(project_directory, 'conf', 'php')
        destination = os.path.join(conf_php_path, self.PHP_INI_FILE)
        if not os.path.exists(destination):
            os.makedirs(conf_php_path)
            builder.build_php_ini(
                os.path.join('php', self.PHP_INI_FILE),
                destination,
                config['php']
            )
            print "Creating 'php.ini'... done"

        # 7. Generate symlink for virtual host
        destination = os.path.join(project_directory, 'conf', 'apache2', 'sites-available')
        if not os.path.exists(destination):
            os.makedirs(destination)
        shutil.copyfile(
            os.path.join(project_directory, self.SITE_DIRECTORY, config['docker']['vhost']),
            os.path.join(destination, config['docker']['site'])
        )
        print "Copy virtual host file... done"

        # 8. Generate 'Dockerfile'
        destination = os.path.join(project_directory, self.DOCKERFILE_FILE)
        config['docker']['libs'] = set(config['docker']['libs'] + self.DEFAULT_LIBS)
        if not os.path.exists(destination):
            config['docker']['maintainer'] = self.PROJECT_MAINTAINER
            builder.build_dockerfile(
                os.path.join('docker', self.DOCKERFILE_FILE),
                destination,
                config['docker']
            )
            print "Creating 'Dockerfile' ... done"
        else:
            print "Dockerfile already exists, do nothing!"

        # 9. Generate 'docker-compose.yml'
        destination = os.path.join(project_directory, self.DOCKER_COMPOSE_FILE)
        if not os.path.exists(destination):
            builder.build_docker_compose(
                os.path.join('docker', self.DOCKER_COMPOSE_FILE),
                destination,
                os.path.join(self.TEMPLATES_DIRECTORY, 'services'),
                config['docker-compose']
            )
            print "Creating 'docker-compose.yml' ... done"

        return project

    # Stop one or more projects
    def stop(self):
        project = self.args.o
        os.chdir(os.path.join(self.PROJECTS_DIRECTORY, project))
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
                    print "Removing '%s' project ... done" % p
                    self.LOG.info("Deleting '%s' project" % p)
        # Remove single project
        elif os.path.exists(os.path.join(self.PROJECTS_DIRECTORY, project)):
            # Stop containers
            os.chdir(os.path.join(self.PROJECTS_DIRECTORY, project))
            print self.docker_compose.stop(project)
            print self.docker_compose.rm(project)
            # Remove project directory
            shutil.rmtree(os.path.join(self.PROJECTS_DIRECTORY, project))
            print "Removing '%s' project ... done" % project
            self.LOG.info('Deleting %s project' % project)
        else:
            print "No such project: '%s'" % project
            self.LOG.error("Error response from app: No such project: %s" % project)

    # Show version number
    def version(self):
        print 'version %s' % self.VERSION
