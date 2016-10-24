import ConfigParser
import os
from jinja2 import Environment, PackageLoader


class Builder(object):

    config_parser = ConfigParser.ConfigParser()

    # Constructor
    def __init__(self, project_directory):
        self.project_directory = project_directory
        self.env = Environment(loader=PackageLoader('DockerStack', 'templates'))

    # Build 'Dockerfile'
    def build_dockerfile(self, source, destination, config):
        tmpl = self.env.get_template(source)

        # Arguments to pass to template
        config['extra'] = ''

        # Check extra template part
        extra = os.path.join('./templates', 'extra', config['type'], 'Dockerfile')
        if os.path.exists(extra):
            e = open(extra)
            config['extra'] = e.read()
            pass

        # Write final file including variables
        with open(destination, 'w') as f:
            f.write(tmpl.render(**config))

    # Build 'docker-compose.yml'
    def build_docker_compose(self, source, destination, services_dir, config):
        tpl = self.env.get_template(source)
        config['services_render'] = ''

        for k, s in config['services'].items():
            service_file = os.path.join('services', k + '.yml')
            if os.path.exists(os.path.join(services_dir, k + '.yml')):
                s_tpl = self.env.get_template(service_file)
                config['services_render'] += s_tpl.render(**s)
                config['services_render'] += "\n\n"

        # Write final file including variables
        with open(destination, 'w') as f:
            f.write(tpl.render(**config))
