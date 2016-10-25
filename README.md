Docker Stack by Kaliop Canada
=============================

Usage
-----
### Start
Build and start a new project
```bash
./stash.py -s project
```

### Build
Build a new or existing project
```bash
./stash.py -b project
```

### Run
Run docker container(s), assuming files has been built
```bash
./stash.py -r project1 project2
```

### Stop
Stop docker container(s) for the current project
```bash
./stash.py -s project1 project2
```

### Remove
Remove one or more projects
```bash
./stash.py -rm project1 project2
```

### List projects
List all created projects
```bash
./stash.py -ps
```

### Version
Display version number
```bash
./stash.py -v
```


Dependencies
------------
* Python 2.7.x
* GitPython `pip install gitpython`
* Jinja2 `pip install Jinja2`

How to package application
--------------------------
* https://python-packaging.readthedocs.io/en/latest/