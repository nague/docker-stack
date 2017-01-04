from __future__ import print_function
import subprocess

from dockerstack.command.AbstractDockerCommand import AbstractDockerCommand


class DockerCommand(AbstractDockerCommand):
    DOCKER_CMD = 'docker'

    # ========================================
    # Execute a command in a running container
    # ========================================
    def execute(self, project_name='', service='web', command=''):
        command = [
            self.SUDO_CMD,
            self.DOCKER_CMD,
            'exec',
            '-i',
            project_name + '_' + service + '_1'
         ] + command.split(' ')

        for path in self._execute(command):
            print(path, end="")
