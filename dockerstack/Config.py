import os
import errno
import yaml
from jinja2 import Environment, PackageLoader


class Config(object):
    # Constants
    DEFAULT_TIMEZONE = 'America/Toronto'
    DEFAULT_PORT = [80]

    # Properties
    data = []

    # ===========
    # Constructor
    # ===========
    def __init__(self, path):
        self.config_path = path

        # Load data from YAML file
        with open(self.config_path, 'r') as stream:
            self.data = yaml.load(stream)

        self.env = Environment(loader=PackageLoader('dockerstack', 'templates'))

    # =================
    # Parse config file
    # =================
    def parse_config(self):
        # Return array with key
        array = {
            'docker': {},
            'docker-compose': {
                'ports': self.DEFAULT_PORT,
                'services': {},
                'links': []
            },
            'php': {
                'timezone': self.DEFAULT_TIMEZONE
            }
        }

        # List required sections/options from 'docker-stack.ini'
        required = {
            'webserver': ['engine', 'vhost'],
            'php': ['version']
        }
        # Checking default required sections/options exists
        for key, values in required.items():
            # 1. Check section exists
            if key not in self.data:
                raise Exception('Error, section "{}" is required'.format(key))
            # 2. Check option exists
            for value in values:
                if value not in self.data[key]:
                    raise Exception('Error, option "{}" in section "{}" is required'.format(value, key))

        # Get main sections
        general = self.data['general']
        webserver = self.data['webserver']
        php = self.data['php']
        services = None
        if 'services' in self.data:
            services = self.data['services']

        # Database path
        if 'db_path' in general:
            array['db'] = general['db_path']

        # Dockerfile variables
        array['docker']['server_engine'] = webserver['engine']
        array['docker']['vhost'] = webserver['vhost']
        array['docker']['site'] = os.path.basename(webserver['vhost'])
        array['docker']['image'] = php['version']
        if 'libs' in general:
            array['docker']['libs'] = general['libs']
        if 'extensions' in php:
            array['docker']['extensions'] = php['extensions']
        if 'platform' in general:
            array['docker']['platform'] = general['platform']
        if 'enable' in php:
            array['docker']['enable'] = php['enable']
        if 'pecl' in php:
            array['docker']['pecl'] = php['pecl']
        if 'modules' in webserver:
            array['docker']['modules'] = webserver['modules']

        # docker-compose.yml variables
        if 'ports' in webserver:
            array['docker-compose']['ports'] = webserver['ports']
        if services:
            for k, v in services.items():
                array['docker-compose']['services'][k] = v

        # php.ini variables
        if 'timezone' in php:
            array['php']['timezone'] = php['timezone']

        return array

    # ==================
    # Build php.ini file
    # ==================
    def build_php_ini(self, source, destination):
        tmpl = self.env.get_template(source)
        if not os.path.exists(os.path.dirname(destination)):
            try:
                os.makedirs(os.path.dirname(destination))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with open(destination, 'w') as f:
            f.write(tmpl.render(timezone='test'))
