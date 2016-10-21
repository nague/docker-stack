import argparse
import logging
import os
import cgitb


class DockerStack(argparse.Action):
    args = []
    VERSION = 1.0
    PROJECT_NAME = 'Docker Stack'
    PROJECTS_DIRECTORY = './projects/'
    TEMPLATES_DIRECTORY = './templates/'
    LOG = logging.getLogger(__name__)

    # Magic call method
    def __call__(self, parser, namespace, values, option_string=None):
        print '%r %r %r' % (namespace, values, option_string)

    # Constructor
    def __init__(self, parser):
        self.parser = parser
        self.args = parser.parse_args()
        logging.basicConfig(filename='stack.log', level=logging.DEBUG)

        print "========= Welcome to Kaliop %s project ==========\n" % self.PROJECT_NAME

        if not os.path.exists(self.PROJECTS_DIRECTORY):
            os.makedirs(self.PROJECTS_DIRECTORY)
            self.LOG.info('create \'projects\' directory')

        super(DockerStack, self).__init__(self, parser)

    # Start building a new project
    def start(self):

        project = self.args.start
        if project is 1:
            project = raw_input("Please enter the project name: ")

        if not os.path.exists(self.PROJECTS_DIRECTORY + project):
            os.makedirs(self.PROJECTS_DIRECTORY + project)
            self.LOG.info('create main directory for project: %s' % project)

    # Show version number
    def version(self):
        print '%s version %s' % (self.PROJECT_NAME, self.VERSION)
