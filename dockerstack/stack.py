#!/usr/bin/python

from DockerStack import DockerStack
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="")
    # parser.add_argument('-b', '--build', action='store_true', help='build a project without running the container')
    # parser.add_argument('-r', '--run', action='store_true',
    #                     help='run docker container(s), assuming files has been built')
    # parser.add_argument('-o', '--stop', action='store_true', help='stop docker container(s) for the current project')
    # parser.add_argument('-t', '--reset', action='store_true', help='remove docker container(s) and all generated files')

    commands = parser.add_argument_group('Commands')
    commands.add_argument('-s', nargs='?', const=1, type=str, help='Build and start a new project')
    commands.add_argument('-ps', help='List projects and status')
    commands.add_argument('-rm', nargs='?', const=1, help='Remove one or more projects')
    commands.add_argument('-v', action='store_true', help='Display version number')

    return parser


def main():
    parser = parse_args()

    # Init project
    docker_stack = DockerStack(parser)

    # Commands
    if docker_stack.args.s:
        docker_stack.start()
    elif docker_stack.args.rm:
        docker_stack.remove()
    elif docker_stack.args.v:
        docker_stack.version()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
