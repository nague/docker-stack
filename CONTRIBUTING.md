Contributing to Stack
=====================

Development environment
-----------------------
If you're looking contribute to _Stack_ but you're new to the project
or maybe even to Python, here are the steps that should get you started.

* Set up a development environment by running `python setup.py develop`.
 This will install the dependencies and set up a symlink from your
 `docker-stack` executable.
 When you now run `docker-stack` from anywhere on your machine,
 it will run your development version of _Stack_.
 
Building a distributed version
------------------------------
### tar.gz
`python setup.py bdist`
### deb
`pip install stdeb`
`python setup.py --command-packages=stdeb.command bdist_deb`
### standalone executable
`pip install bbfreeze`
`python setup.py bdist_bbfreeze`
> see: https://pypi.python.org/pypi/bbfreeze/
