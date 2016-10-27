Docker Stack by Kaliop `0.2`
============================

Usage
-----
```bash
Usage:
  docker-stack [-p <arg>...] [options] [COMMAND] [ARGS...]
  docker-stack -h|--help

Options:
  -p, --project-name NAME     Specify the project name

Commands:
  build              Build a new or existing project
  help               Get help on a command
  ps                 List all created projects
  rm                 Remove one or more projects
  start              Build and start a new project
  stop               Stop docker container(s) for the current project
  version            Display version number
```

Dependencies
------------
* Python 2.7.x
* GitPython `pip install gitpython`
* Jinja2 `pip install Jinja2`
* docopt `pip install docopt`

Contributing
------------
See [CONTRIBUTING.md](./CONTRIBUTING.md)
