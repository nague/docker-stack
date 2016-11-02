from __future__ import print_function

from dockerstack.command.AbstractDockerCommand import AbstractDockerCommand


class DockerCommand(AbstractDockerCommand):
    DOCKER_CMD = 'docker'

    def docker_exec(self, project):
        for path in self.execute([self.SUDO_CMD, self.DOCKER_CMD, 'exec', '-i', 'skeleton_web_1',
                                  '/bin/sh']):
            print(path, end="")