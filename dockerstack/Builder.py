import ConfigParser
import os
import dockerstack
import yaml

from jinja2 import Environment, PackageLoader


class Builder(object):

    CURRENT_PATH = os.path.dirname(dockerstack.__file__)

    # Constructor
    def __init__(self, project_directory):
        self.project_directory = project_directory
        self.env = Environment(loader=PackageLoader('dockerstack', 'templates'))

    # Build 'Dockerfile' file
    def build_dockerfile(self, source, destination, args):
        tmpl = self.env.get_template(source)

        # PHP ext configure
        args['configure'] = []
        if 'extensions' in args:
            for ext in args['extensions']:
                ext_configure = os.path.join(self.CURRENT_PATH, 'templates', 'php', 'ext-configure', 'Dockerfile-' + ext)
                if os.path.exists(ext_configure):
                    c = open(ext_configure)
                    args['configure'] += [c.read()]

        # Write final file including variables
        with open(destination, 'w') as f:
            f.write(tmpl.render(**args))

    # Build 'docker-compose.yml' file
    @staticmethod
    def build_docker_compose(destination, args):
        # Default values
        data = {
            'version': '2',
            'services': {
                'web': {
                    'build': '.',
                    'restart': 'yes',
                    'volumes': ['./www:/var/www/html']
                }
            }
        }
        # Set ports if provided
        if 'ports' in args:
            data['services']['web']['ports'] = args['ports']
        # Add additional services
        if 'services' in args:
            data['services'].update(args['services'])
        # Set volumes if provided
        if 'volumes' in args:
            data['volumes'] = args['volumes']

        # Write final file including variables
        with open(destination, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False, explicit_start=False)

    # Build 'php.ini' file
    @staticmethod
    def build_php_ini(destination, args):
        config_parser = ConfigParser.ConfigParser()
        php_ini = open(destination, 'w')
        config_parser.add_section('Date')
        config_parser.set('Date', 'date.timezone', args['timezone'])
        config_parser.write(php_ini)
        php_ini.close()
