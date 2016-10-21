import ConfigParser
import os

class Docker(object):

    config_parser = ConfigParser.ConfigParser()
    TEMPLATES_DIRECTORY = './templates/'

    def __init__(self, project_directory):
        self.project_directory = project_directory
        print "Docker class constructor"

    def build(self):
        print self.config_parser.read(os.path.join(self.TEMPLATES_DIRECTORY, 'docker', 'Dockerfile'))
