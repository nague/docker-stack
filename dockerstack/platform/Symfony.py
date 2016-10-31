from dockerstack.Platform import Platform


class Symfony(Platform):
    # Pre processing
    def pre_processing(self):
        # 1. Add composer install script in Dockerfile
        return {
            'php_ini': '',
            'dockerfile': self.install_composer_cmd(),
            'docker_composer': ''
        }

    # Post processing scripts
    def post_processing(self):
        # 1. Run `composer install`
        # 2. Run `assets:install`
        # 3. Run `assetic:dump`
        # 4. Run `chmod 777`
        # 5. Run `apache2-foreground`
        pass
