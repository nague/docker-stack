#!/usr/bin/python

from DockerStack import DockerStack
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--start', '-s', action='store_true')
    parser.add_argument('--version', action='store_true')

    return parser


def main():
    parser = parse_args()

    docker_stack = DockerStack(parser)

    if docker_stack.args.version:
        docker_stack.version()
    elif docker_stack.args.start:
        docker_stack.start()

if __name__ == '__main__':
    main()
