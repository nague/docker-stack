import argparse


class DockerStack(argparse.Action):
    args = []
    VERSION = 1.0

    def __call__(self, parser, namespace, values, option_string=None):
        print '%r %r %r' % (namespace, values, option_string)

    def __init__(self, parser):
        self.parser = parser
        self.args = parser.parse_args()
        print vars(self.args)
        if not vars(self.args):
            print self.parser.print_help()
            parser.exit(1)

        super(DockerStack, self).__init__(self, parser)

    def start(self):
        print "========= Welcome to Kaliop Docker Stack project ==========\n"

    def version(self):
        print "Docker Stack version", self.VERSION
