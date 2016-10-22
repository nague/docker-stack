import ConfigParser
import os
from jinja2 import Environment, PackageLoader


class Docker(object):

    config_parser = ConfigParser.ConfigParser()

    # Constructor
    def __init__(self, project_directory):
        self.project_directory = project_directory
        self.env = Environment(loader=PackageLoader('DockerStack', 'templates'))

    # Build 'Dockerfile'
    def build(self, source, destination, config):
        tmpl = self.env.get_template(source)

        # Arguments to pass to template
        args = config['docker']
        args['extra'] = ''

        # Check extra template part
        extra = os.path.join('./templates', 'extra', config['docker']['type'], 'Dockerfile')
        if os.path.exists(extra):
            e = open(extra)
            args['extra'] = e.read()
            pass

        # Write final file including variables
        with open(destination, 'w') as f:
            f.write(tmpl.render(**args))

        print 'Dockerfile successfully created!'
