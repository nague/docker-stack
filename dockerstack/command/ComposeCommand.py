from __future__ import print_function
import subprocess


class ComposeCommand(object):

    DOCKER_COMPOSE_CMD = 'docker-compose'
    SUDO_CMD = '/usr/bin/sudo'

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

    # ===========================================
    # Generator: execute command and yield result
    # ===========================================
    def execute(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        stdout_lines = iter(p.stdout.readline, "")
        for stdout_line in stdout_lines:
            yield stdout_line

        p.stdout.close()
        return_code = p.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, cmd)

    # ==========================
    # Return version information
    # ==========================
    def version(self):
        return subprocess.Popen([self.SUDO_CMD, self.DOCKER_COMPOSE_CMD, 'version'],
                                stdout=subprocess.PIPE).stdout.read()
