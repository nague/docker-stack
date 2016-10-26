#!/usr/bin/python

from DockerStack import DockerStack
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="")

    commands = parser.add_argument_group('Commands')
    commands.add_argument('-s', nargs='?', const=1, type=str, help='Build and start a new project')
    commands.add_argument('-b', nargs='?', const=1, type=str, help='Build a new or existing project')
    commands.add_argument('-r', nargs='*', help="Run docker container(s), assuming files has been built")
    commands.add_argument('-o', nargs='?', const=1, type=str, help='Stop docker container(s) for the current project')
    commands.add_argument('-ps', action='store_true', help='List all created projects')
    commands.add_argument('-rm', nargs='?', const=1, help='Remove one or more projects')
    commands.add_argument('--version', '-v', action='store_true', help='Display version number')

    return parser


def main():
    parser = parse_args()

    # Init project
    docker_stack = DockerStack(parser)

    # Commands
    if docker_stack.args.s:
        docker_stack.start()
    elif docker_stack.args.b:
        docker_stack.build()
    elif docker_stack.args.r:
        pass
    elif docker_stack.args.o:
        docker_stack.stop()
    elif docker_stack.args.ps:
        pass
    elif docker_stack.args.rm:
        docker_stack.remove()
    elif docker_stack.args.version:
        docker_stack.version()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
