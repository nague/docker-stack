import dockerstack
import os
import re
import shutil

from dockerstack.platform.Default import Default
from dockerstack.platform.EzPublish import EzPublish
from dockerstack.platform.Symfony import Symfony
from dockerstack.platform.WordPress import WordPress
from dockerstack.utils import yesno
from git import Repo

from dockerstack.command.DockerComposeCommand import DockerComposeCommand
from dockerstack.Config import Config
from dockerstack.Builder import Builder
from dockerstack.Progress import Progress


class Project(object):
    # Constants
    CURRENT_PATH = os.path.dirname(dockerstack.__file__)
    CONFIG_DIRECTORY = os.path.join(os.path.expanduser('~'), '.config', 'docker-stack')
    PROJECTS_DIRECTORY = os.path.join(os.path.expanduser('~'), 'DockerStackProjects')
    SITE_DIRECTORY = 'www'
    TEMPLATES_DIRECTORY = 'templates'
    PHP_INI_FILE = 'php.ini'
    DOCKERFILE_FILE = 'Dockerfile'
    DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    DEFAULT_LIBS = ['wget', 'git', 'curl', 'zip']

    # Properties
    project_name = None
    config_file = 'docker-stack.json'
    compose_command = DockerComposeCommand()
    platform = Default()

    # ===========
    # Constructor
    # ===========
    def __init__(self):
        # Welcome message when stating app
        print "========= Welcome to {} by {}  ==========".format(dockerstack.__name__, dockerstack.__maintainer__)

        # Create main config directory, it will contains logs, ...
        if not os.path.exists(self.CONFIG_DIRECTORY):
            os.makedirs(self.CONFIG_DIRECTORY)

        # Create projects directory, it will contains all docker-stack projects
        if not os.path.exists(self.PROJECTS_DIRECTORY):
            os.makedirs(self.PROJECTS_DIRECTORY)

    # =============================
    # Get project name from options
    # =============================
    @staticmethod
    def get_project_name(project_name):
        if project_name:
            return re.sub(r'[^a-z0-9]', '', project_name.lower())
        return None

    # ============================
    # Start building a new project
    # ============================
    def start(self):
        # Move at root project directory
        os.chdir(os.path.join(self.PROJECTS_DIRECTORY, self.project_name))
        # Start using `docker-compose up` command
        self.compose_command.start(self.project_name)
        # After starting container, execute post processing commands
        # docker_command = DockerCommand()
        # docker_command.docker_exec(self.project_name)
        self.platform.post_processing()

    # ================
    # Building process
    # ================
    def build(self, project_name, force_rebuild=False, config_file=None):
        # 0. Arguments
        if config_file is not None:
            self.config_file = config_file

        #  1. Save project name
        self.project_name = project_name

        # 2. Set project directory
        project_directory = os.path.join(self.PROJECTS_DIRECTORY, self.project_name)

        # 3. Create project main directory if not exists
        if not os.path.exists(project_directory):
            os.makedirs(project_directory)

        # 4. Symlink existing sources or Git clone project to self.SITE_DIRECTORY directory
        if not os.path.exists(os.path.join(project_directory, self.SITE_DIRECTORY)):
            print 'Please choose one of the following:'
            print ' 1. Create a Symlink from existing sources (default)'
            print ' 2. Cloning a Git repository'
            cloning = raw_input('Enter your choose now: ') or 1
            print "\n"
            if int(cloning) is 1:
                source = raw_input("Please provide the full path of your sources directory (e.g. using 'pwd'):\n")
                print "We are about to create a symlink from '{}' to '{}'\n".format(
                    source,
                    os.path.join(project_directory, self.SITE_DIRECTORY)
                )
                validation = yesno("Do you want to continue [Y/n]: ", default=True)
                if validation is True:
                    os.symlink(source, os.path.join(project_directory, self.SITE_DIRECTORY))
                    print "Creating symlink ... done\n"
            else:
                source = raw_input('Please provide a Git valid URL (http or ssh): ')
                branch = raw_input(
                    'From witch branch do you want to clone the repository (default: master): ') or 'master'
                print "We are about to clone your repo '{}' from branch '{}'\n".format(source, branch)
                validation = yesno("Do you want to continue [Y/n]: ", default=True)
                print validation
                if validation is True:
                    Repo.clone_from(
                        source,
                        os.path.join(project_directory, self.SITE_DIRECTORY),
                        branch=branch,
                        progress=Progress()
                    )
                    print "Cloning Git repository ... done\n"
                else:
                    raise Exception("Aborting ...")

        # 5. Read 'docker-stack.json' file
        config_path = os.path.join(project_directory, self.SITE_DIRECTORY, self.config_file)
        if not os.path.exists(config_path):
            raise Exception("Error: '{}' not found ... aborting".format(self.config_file))
        docker_stack_config = Config(config_path)
        config = docker_stack_config.parse_config()

        # 6. Database
        if 'db' in config:
            # Create 'db' directory
            db_dir = os.path.join(project_directory, 'db')
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
                print "Creating directory '{}' ... done\n".format(os.path.join('projects', self.project_name, 'db'))
            db_destination_file = os.path.join(db_dir, os.path.basename(config['db']))
            db_source_file = os.path.join(project_directory, self.SITE_DIRECTORY, config['db'])
            # Check database source file exists
            if not os.path.exists(db_source_file):
                raise Exception("Database file '{}' does not exists ... aborting".format(db_source_file))
            # Copy database file to 'db' directory if not exists already
            if not os.path.exists(db_destination_file):
                print "Database file '{}' found".format(os.path.basename(config['db']))
                shutil.copyfile(
                    db_source_file,
                    db_destination_file
                )
                print "Copying database file ... done\n"
            # Updating database file if source has been updated
            elif not os.path.getsize(db_destination_file) == os.path.getsize(db_source_file):
                shutil.rmtree(db_destination_file)
                shutil.copyfile(
                    db_source_file,
                    db_destination_file
                )
                print "Updating database file ... done\n"

        # 7. Find current platform from config file
        if 'platform' in config['docker']:
            self.get_platform(config)

        self.platform.pre_processing()

        # 8. Init builder
        builder = Builder(project_directory)

        # 9. Generate 'php.ini'
        conf_php_path = os.path.join(project_directory, 'conf', 'php')
        destination = os.path.join(conf_php_path, self.PHP_INI_FILE)
        if not os.path.isdir(conf_php_path):
            os.makedirs(conf_php_path)
            print "Creating '{}' directory ... done".format(conf_php_path)
        if not os.path.exists(destination):
            builder.build_php_ini(
                destination,
                config['php']
            )
            print "Creating 'php.ini' ... done"

        # 10. Copy virtual host file
        destination_directory = os.path.join(project_directory, 'conf', 'apache2', 'sites-available')
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        destination_path = os.path.join(destination_directory, config['docker']['site'])
        if not os.path.exists(destination_path):
            shutil.copyfile(
                os.path.join(project_directory, self.SITE_DIRECTORY, config['docker']['vhost']),
                destination_path
            )
            print "Copy virtual host file ... done"

        # 11. Generate 'Dockerfile'
        destination = os.path.join(project_directory, self.DOCKERFILE_FILE)
        if 'libs' in config['docker']:
            config['docker']['libs'] = set(config['docker']['libs'] + self.DEFAULT_LIBS)
        if not os.path.exists(destination):
            config['docker']['maintainer'] = dockerstack.__maintainer__
            builder.build_dockerfile(
                os.path.join('docker', self.DOCKERFILE_FILE),
                destination,
                config['docker']
            )
            print "Creating 'Dockerfile' ... done"

        # 12. Generate 'docker-compose.yml'
        destination = os.path.join(project_directory, self.DOCKER_COMPOSE_FILE)
        if not os.path.exists(destination):
            builder.build_docker_compose(
                destination,
                config['docker-compose']
            )
            print "Creating 'docker-compose.yml' ... done"

        # 13. Force rebuild
        if force_rebuild is True:
            print "Starting rebuilding containers ...\n"
            os.chdir(os.path.join(self.PROJECTS_DIRECTORY, self.project_name))
            self.compose_command.create(self.project_name, force=True)
            print "Containers rebuilding ... done"

        # 14. Return project name
        return self.project_name

    # =========================
    # Stop one or more projects
    # =========================
    def stop(self, project_name):
        #  1. Save project name
        self.project_name = project_name

        # 2. If project exists
        project_path = os.path.join(self.PROJECTS_DIRECTORY, self.project_name)
        if os.path.exists(project_path):
            # Stop containers
            os.chdir(project_path)
            self.compose_command.stop(self.project_name)
            print "Stopping '{}' project ... done".format(self.project_name)
        else:
            raise Exception("No such project: '{}'".format(self.project_name))

    # ===========================
    # Remove one or more projects
    # ===========================
    def remove(self, projects):
        for project in projects:
            project_path = os.path.join(self.PROJECTS_DIRECTORY, project)
            if os.path.exists(project_path):
                # Stop containers
                os.chdir(project_path)
                self.compose_command.stop(project)
                self.compose_command.rm(project)
                # Remove project directory
                shutil.rmtree(project_path)
                print "Removing '{}' project ... done".format(project)
            else:
                print "No such project: '{}'".format(project)

    # ==========================================
    # Get platform class from configuration file
    # ==========================================
    def get_platform(self, config):
        if str(config['docker']['platform']).lower() == 'symfony':
            self.platform = Symfony()
        elif str(config['docker']['platform']).lower() == 'ez' \
                or str(config['docker']['platform']).lower() == 'ezpublish':
            self.platform = EzPublish()
        elif str(config['docker']['platform']).lower() == 'wp' \
                or str(config['docker']['platform']).lower() == 'wordpress':
            self.platform = WordPress()

        return self.platform
