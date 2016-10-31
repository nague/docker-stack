from __future__ import print_function
import subprocess

from dockerstack.command.AbstractDockerCommand import AbstractDockerCommand


class DockerComposeCommand(AbstractDockerCommand):
    DOCKER_COMPOSE_CMD = 'docker-compose'

    # ================
    # Start containers
    # ================
    def start(self, project):
        for path in self.execute([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'up', '-d']):
            print(path, end="")

    # =========================
    # Build or rebuild services
    # =========================
    def build(self, project):
        for path in self.execute([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'build']):
            print(path, end="")

    # =============
    # Stop services
    # =============
    def stop(self, project):
        for path in self.execute([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'stop']):
            print(path, end="")

    # ===============
    # Remove services
    # ===============
    def rm(self, project):
        for path in self.execute([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'rm', '-f']):
            print(path, end="")

    # ==========================
    # Return version information
    # ==========================
    def version(self):
        return subprocess.Popen([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, 'version'],
                                stdout=subprocess.PIPE).stdout.read()
