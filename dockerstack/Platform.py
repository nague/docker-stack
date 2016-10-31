from abc import ABCMeta


class Platform(object):
    __metaclass__ = ABCMeta

    # Constructor
    def __init__(self):
        pass

    # Pre processing
    def pre_processing(self): raise NotImplementedError

    # Post processing scripts
    def post_processing(self): raise NotImplementedError

    # Install Composer and make it available in the PATH
    @staticmethod
    def install_composer_cmd():
        script = "# Install Composer and make it available in the PATH\n"
        script += "RUN wget https://getcomposer.org/composer.phar && " \
                  "chmod +x composer.phar && " \
                  "mv composer.phar /usr/local/bin/composer"
        return script
