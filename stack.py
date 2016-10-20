#!/usr/bin/python

from DockerStack import DockerStack
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--start', '-s', action=DockerStack)
    parser.add_argument('--version', action='version', version='version 1')

    return parser.parse_args()


def main():
    parse_args()


if __name__ == '__main__':
    main()
