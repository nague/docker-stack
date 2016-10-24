import os
from jinja2 import Environment, PackageLoader


class Builder(object):

    # Constructor
    def __init__(self, project_directory):
        self.project_directory = project_directory
        self.env = Environment(loader=PackageLoader('DockerStack', 'templates'))

    # Build 'Dockerfile' file
    def build_dockerfile(self, source, destination, args):
        tmpl = self.env.get_template(source)

        # Arguments to pass to template
        args['extra'] = ''
        # Check extra template part
        extra = os.path.join('./templates', 'extra', args['type'], 'Dockerfile')
        if os.path.exists(extra):
            e = open(extra)
            args['extra'] = e.read()

        # PHP ext configure
        args['configure'] = []
        for ext in args['extensions']:
            ext_configure = os.path.join('./templates', 'php', 'ext-configure', 'Dockerfile-' + ext)
            if os.path.exists(ext_configure):
                c = open(ext_configure)
                args['configure'] += [c.read()]

        # Write final file including variables
        with open(destination, 'w') as f:
            f.write(tmpl.render(**args))

    # Build 'docker-compose.yml' file
    def build_docker_compose(self, source, destination, services_dir, args):
        tpl = self.env.get_template(source)
        args['services_render'] = ''

        for k, s in args['services'].items():
            service_file = os.path.join('services', k + '.yml')
            if os.path.exists(os.path.join(services_dir, k + '.yml')):
                s_tpl = self.env.get_template(service_file)
                args['services_render'] += s_tpl.render(**s)
                args['services_render'] += "\n\n"

        # Write final file including variables
        with open(destination, 'w') as f:
            f.write(tpl.render(**args))

    # Build 'php.ini' file
    def build_php_ini(self, source, destination, args):
        tpl = self.env.get_template(source)

        # Write final file including variables
        with open(destination, 'w') as f:
            f.write(tpl.render(**args))
