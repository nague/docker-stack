import ConfigParser
import os
import errno
import string
from jinja2 import Environment, PackageLoader


class DockerStackConfig(object):

    config_parser = ConfigParser.ConfigParser()

    # Constructor
    def __init__(self, path):
        self.config_path = path
        self.env = Environment(loader=PackageLoader('DockerStack', 'templates'))

    # Parse config file
    def parse_config(self):
        array = {
            'docker': {},
            'docker-compose': {}
        }
        self.config_parser.read(self.config_path)

        # Main
        array['db'] = self.config_section_map('db')['path']

        # Dockerfile variables
        array['docker']['image'] = self.config_section_map('php')['version']
        array['docker']['vhost'] = self.config_section_map('webserver')['vhost']
        array['docker']['site'] = os.path.basename(array['docker']['vhost'])
        array['docker']['libs'] = string.split(self.config_section_map('general')['libs'], ',')
        array['docker']['extensions'] = string.split(self.config_section_map('php')['extensions'], ',')
        array['docker']['type'] = self.config_section_map('general')['type']

        # docker-compose.yml variables
        array['docker-compose']['port'] = self.config_section_map('webserver')['port']

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
