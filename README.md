Docker Stack by Kaliop Canada
=============================

Usage
-----
```bash
usage: stack.py [-h] [-s [S]] [-b [B]] [-r [R [R ...]]] [-o [O]] [-ps]
                [-rm [RM]] [--version]

optional arguments:
  -h, --help      show this help message and exit

Commands:
  -s [S]          Build and start a new project
  -b [B]          Build a new or existing project
  -r [R [R ...]]  Run docker container(s), assuming files has been built
  -o [O]          Stop docker container(s) for the current project
  -ps             List all created projects
  -rm [RM]        Remove one or more projects
  --version, -v   Display version number
```

Dependencies
------------
* Python 2.7.x
* GitPython `pip install gitpython`
* Jinja2 `pip install Jinja2`

How to package application
--------------------------
* https://python-packaging.readthedocs.io/en/latest/