import os
import dockerstack
import yaml

from dockerstack.Services import Services
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

        # Arguments to pass to template
        args['extra'] = ''
        # Check extra template
        if 'platform' in args:
            extra = os.path.join(self.CURRENT_PATH, 'templates', 'extra', args['platform'], 'Dockerfile')
            if os.path.exists(extra):
                e = open(extra)
                args['extra'] = e.read()

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
    def build_docker_compose(self, destination, args):
        # Default values
        data = {
            'version': '2',
            'services': {
                'web': {
                    'restart': 'yes',
                    'build': '.',
                    'ports': args['ports'],
                    'volumes': ['./www:/var/www/html']
                }
            }
        }

        # If services exists, call Services().<service_name>() and add links to 'web'
        service_class = Services()
        if 'services' in args:
            data['services']['web']['links'] = []
            for k, s in args['services'].items():
                service = s['link']
                data['services']['web']['links'] += ['{}:{}'.format(service, k)]
                if hasattr(service_class, service):
                    data['services'][service] = getattr(service_class, service)(s)

        # Write final file including variables
        with open(destination, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False, explicit_start=False)

    # Build 'php.ini' file
    def build_php_ini(self, source, destination, args):
        tpl = self.env.get_template(source)

        # Write final file including variables
        with open(destination, 'w') as f:
            f.write(tpl.render(**args))
