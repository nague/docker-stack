import argparse


class DockerStack(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")

        super(DockerStack, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print '%r %r %r' % (namespace, values, option_string)

        setattr(namespace, self.dest, values)
    # def __init__(self):
    #     print "========= Welcome to Kaliop Docker Stack project ==========\n"
