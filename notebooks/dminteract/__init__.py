import os
from .version import __version__

__DBDIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".dbs")
__DATADIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")

if not os.path.exists(__DBDIR):
    os.mkdir(DBDIR)

if not os.path.exists(__DATADIR):
    os.mkdir(DATADIR)

def _dbdir():
    return __DBDIR
def _datadir():
    return __DATADIR






