#!/usr/bin/python

from DockerStack import DockerStack
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-s', '--start', nargs='?', const=1, type=str,
                        help='build and start a new project using DockerCompose')
    parser.add_argument('-b', '--build', action='store_true', help='build a project without running the container')
    parser.add_argument('-r', '--run', action='store_true',
                        help='run docker container(s), assuming files has been built')
    parser.add_argument('-o', '--stop', action='store_true', help='stop docker container(s) for the current project')
    parser.add_argument('-t', '--reset', action='store_true', help='remove docker container(s) and all generated files')
    parser.add_argument('-v', '--version', action='store_true', help='display version number')

    return parser


def main():
    parser = parse_args()

    docker_stack = DockerStack(parser)

    if docker_stack.args.version:
        docker_stack.version()
    elif docker_stack.args.start:
        docker_stack.start()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
