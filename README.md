Docker Stack by Kaliop
======================

Usage
-----
```bash
An utility to Dockerize your applications and generate minimal docker
requires files.

Usage:
  docker-stack [options] [COMMAND] [ARGS...]
  docker-stack -h|--help

Commands:
  build              Build a new or existing project
  help               Get help on a command
  ps                 List all created projects
  rm                 Remove one or more projects
  start              Build and start a new project
  stop               Stop docker container(s) for the current project
  version            Display version number

Run 'docker-stack COMMAND --help' for more information on a command.
```

Dependencies
------------
* Python 2.7.x
* GitPython `pip install gitpython`
* Jinja2 `pip install Jinja2`
* docopt `pip install docopt`
* PyYAML `pip install pyyaml`
