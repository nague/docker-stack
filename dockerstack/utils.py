from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import dockerstack


def get_version_info():
    version_info = '{} version {}'.format(dockerstack.__program__, dockerstack.__version__)
    return version_info
