import os
from . import utils
DBDIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "dbs")
DATADIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data")
#
# __all__ = ["utils", DBDIR, DATADIR]
__all__ = ["utils"]
