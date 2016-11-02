from dockerstack.Platform import Platform


class Default(Platform):
    # Pre processing
    def pre_processing(self):
        return {'php_ini': '', 'dockerfile': '', 'docker_composer': ''}

    # Post processing scripts
    def post_processing(self):
        return
