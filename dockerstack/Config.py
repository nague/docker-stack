import hashlib
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
    updated = False

    # ===========
    # Constructor
    # ===========
    def __init__(self, path, checksum_file):
        self.config_path = path

        # Load data from YAML file
        with open(self.config_path, 'r') as stream:
            self.data = yaml.load(stream)

        self.checksum_md5_config_file(checksum_file)

        self.env = Environment(loader=PackageLoader('dockerstack', 'templates'))

    # =================================================
    # Checking MD5 checksum for `docker-stack.yml` file
    # =================================================
    def checksum_md5_config_file(self, checksum_file):
        hash_md5 = hashlib.md5(open(self.config_path, 'rb').read()).hexdigest()
        if not os.path.exists(checksum_file):
            config_dir = os.path.dirname(checksum_file)
            if not os.path.isdir(config_dir):
                os.makedirs(config_dir)
            with open(checksum_file, 'w') as cfg:
                cfg.write(hash_md5)
        else:
            md5 = open(checksum_file, 'r').read()
            if md5 != hash_md5:
                self.updated = True
                os.remove(checksum_file)

    # =================
    # Parse config file
    # =================
    def parse_config(self):
        # Return array with key
        array = {
            'docker': {
                'image': 'php'
            },
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

        # Database path
        if 'db_path' in general:
            array['db'] = general['db_path']

        # Dockerfile variables
        array['docker']['server_engine'] = webserver['engine']
        array['docker']['sites'] = []
        array['docker']['vhost'] = []
        if type(webserver['vhost']) is dict:
            if 'available' in webserver['vhost']:
                array['docker']['vhost'].extend(webserver['vhost']['available'])
            if 'enable' in webserver['vhost']:
                array['docker']['vhost'].extend(webserver['vhost']['enable'])
            for key, value in webserver['vhost'].items():
                if key == 'enable':
                    for site in value:
                        array['docker']['sites'].append(os.path.basename(site))
        else:
            array['docker']['vhost'].append(webserver['vhost'])
            array['docker']['sites'] = [os.path.basename(webserver['vhost'])]
        array['docker']['version'] = php['version']
        if 'libs' in general:
            array['docker']['libs'] = general['libs']
        if 'image' in php:
            array['docker']['image'] = php['image']
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
        if 'restart' in general:
            array['docker-compose']['general'] = general['restart']
        if 'ports' in webserver:
            array['docker-compose']['ports'] = webserver['ports']
        if 'links' in general:
            array['docker-compose']['links'] = general['links']
        if 'services' in self.data:
            array['docker-compose']['services'] = self.data['services']
        if 'volumes' in self.data:
            array['docker-compose']['volumes'] = self.data['volumes']

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
