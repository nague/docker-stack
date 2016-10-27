import ConfigParser
import os
import errno
import string
from jinja2 import Environment, PackageLoader


class DockerStackConfig(object):

    DEFAULT_TIMEZONE = 'America/Toronto'
    config_parser = ConfigParser.ConfigParser()

    # Constructor
    def __init__(self, path):
        self.config_path = path
        self.env = Environment(loader=PackageLoader('dockerstack', 'templates'))

    # Parse config file
    def parse_config(self):
        array = {
            'docker': {},
            'docker-compose': {
                'services': {},
                'links': {}
            },
            'php': {}
        }
        self.config_parser.read(self.config_path)
        general = self.config_section_map('general')

        # Database path
        if self.config_parser.has_option('general', 'db_path'):
            array['db'] = general['db_path']

        # Dockerfile variables
        array['docker']['image'] = self.config_section_map('php')['version']
        array['docker']['vhost'] = self.config_section_map('webserver')['vhost']
        array['docker']['server_engine'] = self.config_section_map('webserver')['engine']
        array['docker']['site'] = os.path.basename(array['docker']['vhost'])
        array['docker']['libs'] = string.split(self.config_section_map('general')['libs'], ',')
        array['docker']['extensions'] = string.split(self.config_section_map('php')['extensions'], ',')
        array['docker']['type'] = self.config_section_map('general')['type']
        if self.config_parser.has_option('php', 'enable'):
            array['docker']['enable'] = string.split(self.config_section_map('php')['enable'], ',')
        if self.config_parser.has_option('php', 'pecl'):
            array['docker']['pecl'] = string.split(self.config_section_map('php')['pecl'], ',')

        # docker-compose.yml variables
        array['docker-compose']['ports'] = string.split(self.config_section_map('webserver')['ports'], ',')
        for k, v in self.config_section_map('services').items():
            array['docker-compose']['links'][v] = self.config_section_map(k)['link']
            array['docker-compose']['services'][v] = self.config_section_map(k)

        # php.ini variables
        if self.config_parser.has_option('php', 'timezone'):
            array['php']['timezone'] = self.config_section_map('php')['timezone']
        else:
            array['php']['timezone'] = self.DEFAULT_TIMEZONE

        return array

    # Get config by section
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

    # Build php.ini file
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
