__all__ = ['run_all']

# for importing from parent directory
import sys
from os.path import join, dirname, abspath
sys.path.insert(1, join(sys.path[0], '..'))

global TDIR 
TDIR = dirname(abspath(__file__))

# actual imports
from core import *

#
def test_A() -> None:
    ...
def run_all() -> None:
    test_A()
    print(f"Tests from {__file__} passed.")

#
if __name__ == '__main__':
    run_all()