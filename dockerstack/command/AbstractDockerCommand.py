import subprocess
from abc import ABCMeta


class AbstractDockerCommand(object):
    __metaclass__ = ABCMeta

    SUDO_CMD = '/usr/bin/sudo'

    # ===========================================
    # Generator: execute command and yield result
    # ===========================================
    @staticmethod
    def _execute(cmd):
        print ' '.join(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        stdout_lines = iter(p.stdout.readline, "")
        for stdout_line in stdout_lines:
            yield stdout_line

        p.stdout.close()
        return_code = p.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, cmd)
