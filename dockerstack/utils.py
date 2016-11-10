from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import datetime
import dockerstack


# Prompt the user for a yes or no.
def yesno(prompt, default=None):
    """
    Prompt the user for a yes or no.
    Can optionally specify a default value, which will only be
    used if they enter a blank line.
    Unrecognised input (anything other than "y", "n", "yes",
    "no" or "") will return None.
    """
    answer = raw_input(prompt).strip().lower()

    if answer == "y" or answer == "yes":
        return True
    elif answer == "n" or answer == "no":
        return False
    elif answer == "":
        return default
    else:
        return None


# Get version info
def get_version_info():
    return '{} version {}, build {}'.format(dockerstack.__program__, dockerstack.__version__, get_build_version())


# Get build version
def get_build_version():
    return datetime.datetime.now().time()
