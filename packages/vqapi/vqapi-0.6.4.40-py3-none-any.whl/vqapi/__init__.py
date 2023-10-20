"""
ViQi API for Python clients

Usage
------

.. code-block:: python

    import vqapi

"""

#
from .cmd import bisque_argument_parser, bisque_config, bisque_session
from .comm import BQServer, BQSession
from .exception import *
from .services import ResponseFile, ResponseFolder
from .vqclass import *

__author__    = "Dima Fedorov <dima@viqiai.com>, Kris Kvilekval <kris@viqiai.com>, Christian Lang <clang@viqiai.com>"
__version__   = "0.6.4.39"
__copyright__ = "2018-2023, ViQi Inc"
