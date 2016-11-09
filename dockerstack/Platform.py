from abc import ABCMeta


class Platform(object):
    __metaclass__ = ABCMeta

    # Properties
    docker_file = ''
    docker_compose = ''
    php_ini = ''

    # Pre processing
    def pre_processing(self): raise NotImplementedError

    # Post processing scripts
    def post_processing(self, compose_command): raise NotImplementedError

    # Add data to Dockerfile
    def set_docker_data(self, data):
        self.docker_file += data

    # Get pre processed list of data
    def get_pre_processing_data(self):
        return {'php_ini': self.php_ini, 'dockerfile': self.docker_file, 'docker_composer': self.docker_compose}

    # Install Composer and make it available in the PATH
    @staticmethod
    def install_composer_cmd():
        script = "# Install Composer and make it available in the PATH\n"
        script += "RUN wget https://getcomposer.org/composer.phar && " \
                  "chmod +x composer.phar && " \
                  "mv composer.phar /usr/local/bin/composer"
        return script
