from git import RemoteProgress


class Progress(RemoteProgress):
    def line_dropped(self, line):
        print line

    def update(self, *args):
        print self._cur_line

    def new_message_handler(self):
        def handler(line):
            return self._parse_progress_line(line.rstrip())

        return handler
