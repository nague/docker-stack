import ConfigParser
import os
import errno
import string
from jinja2 import Environment, PackageLoader


class Config(object):

    DEFAULT_TIMEZONE = 'America/Toronto'
    config_parser = ConfigParser.ConfigParser()

    # ===========
    # Constructor
    # ===========
    def __init__(self, path):
        self.config_path = path
        self.config_parser.read(self.config_path)
        self.env = Environment(loader=PackageLoader('dockerstack', 'templates'))

    # =================
    # Parse config file
    # =================
    def parse_config(self):
        # Return array with key
        array = {
            'docker': {},
            'docker-compose': {
                'services': {},
                'links': {}
            },
            'php': {}
        }

        # List required sections/options from 'docker-stack.ini'
        required = {
            'webserver': ['engine', 'vhost'],
            'php': ['version']
        }
        # Checking default required sections/options exists
        for section, options in required.items():
            # 1. Check section exists
            if not self.config_parser.has_section(section):
                raise Exception('Error, section "{}" is required'.format(section))
            # 2. Check option exists
            for option in options:
                if not self.config_parser.has_option(section, option):
                    raise Exception('Error, option "{}" in section "{}" is required'.format(option, section))

        # Get main sections
        general = self.config_section_map('general')
        webserver = self.config_section_map('webserver')
        php = self.config_section_map('php')

        # Database path
        if self.config_parser.has_option('general', 'db_path'):
            array['db'] = general['db_path']

        # Dockerfile variables
        array['docker']['server_engine'] = webserver['engine']
        array['docker']['vhost'] = webserver['vhost']
        array['docker']['site'] = os.path.basename(webserver['vhost'])
        array['docker']['image'] = php['version']
        if self.config_parser.has_option('general', 'libs'):
            array['docker']['libs'] = string.split(general['libs'], ',')
        if self.config_parser.has_option('php', 'extensions'):
            array['docker']['extensions'] = string.split(php['extensions'], ',')
        if self.config_parser.has_option('general', 'platform'):
            array['docker']['platform'] = general['platform']
        if self.config_parser.has_option('php', 'enable'):
            array['docker']['enable'] = string.split(php['enable'], ',')
        if self.config_parser.has_option('php', 'pecl'):
            array['docker']['pecl'] = string.split(php['pecl'], ',')

        # docker-compose.yml variables
        if self.config_parser.has_option('webserver', 'ports'):
            array['docker-compose']['ports'] = string.split(webserver['ports'], ',')
        if self.config_parser.has_section('services'):
            for k, v in self.config_section_map('services').items():
                array['docker-compose']['links'][v] = self.config_section_map(k)['link']
                array['docker-compose']['services'][v] = self.config_section_map(k)

        # php.ini variables
        if self.config_parser.has_option('php', 'timezone'):
            array['php']['timezone'] = php['timezone']
        else:
            array['php']['timezone'] = self.DEFAULT_TIMEZONE

        return array

    # =====================
    # Get config by section
    # =====================
    def config_section_map(self, section):
        array = {}
        options = self.config_parser.options(section)
        for option in options:
            try:
                array[option] = self.config_parser.get(section, option)
                if array[option] == -1:
                    print("skip: %s" % option)
            except ValueError:
                print("exception on %s!" % option)
                array[option] = None
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
