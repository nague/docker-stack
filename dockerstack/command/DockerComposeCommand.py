from __future__ import print_function
import subprocess

from dockerstack.command.AbstractDockerCommand import AbstractDockerCommand


class DockerComposeCommand(AbstractDockerCommand):
    DOCKER_COMPOSE_CMD = 'docker-compose'

    # ==========================
    # Start existing containers.
    # ==========================
    def start(self, project):
        for path in self._execute([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'up', '-d']):
            print(path, end="")

    # ==========================
    # Build or rebuild services.
    # ==========================
    def build(self, project):
        for path in self._execute([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'build']):
            print(path, end="")

    # ==============================================
    # Stop running containers without removing them.
    # ==============================================
    def stop(self, project):
        for path in self._execute([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'stop']):
            print(path, end="")

    # ===================================
    # Removes stopped service containers.
    # ===================================
    def rm(self, project):
        for path in self._execute([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'rm', '-f']):
            print(path, end="")

    # =================================
    # Creates containers for a service.
    # =================================
    def create(self, project, force=False):
        command = [self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'create']
        if force is True:
            command = [self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, '-p', project, 'create', '--force-recreate']
        for path in self._execute(command):
            print(path, end="")

    # ========================
    # Show version information
    # ========================
    def version(self):
        return subprocess.Popen([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, 'version'],
                                stdout=subprocess.PIPE).stdout.read()

    # ========================================
    # Execute a command in a running container
    # ========================================
    def execute(self, service='web', command=''):
        for path in self._execute([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, 'exec', service, command]):
            print(path, end="")
