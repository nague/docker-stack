from subprocess import Popen, PIPE


class DockerCompose(object):

    # Start containers
    def start(self, project):
        p = Popen(['/usr/bin/sudo', 'docker-compose', '-p', project, 'up', '-d'], stdout=PIPE)
        return p.stdout.read()

    # Build or rebuild services
    def build(self):
        pass

    # Stop services
    def stop(self, project):
        p = Popen(['/usr/bin/sudo', 'docker-compose', '-p', project, 'stop'], stdout=PIPE)
        return p.stdout.read()

    #
    def run(self):
        pass

    def rm(self, project):
        p = Popen(['/usr/bin/sudo', 'docker-compose', '-p', project, 'rm', '-f'], stdout=PIPE)
        return p.stdout.read()
