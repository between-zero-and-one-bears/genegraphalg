__all__ = ['run_all']

# for importing from parent directory
import sys
from os.path import join, dirname, abspath
sys.path.insert(1, join(sys.path[0], '..'))

global TDIR 
TDIR = dirname(abspath(__file__))

# actual imports
from core import *
import parsing
from communitydetection import *

#
def test_A() -> None:
    G = parsing.from_file(join(TDIR, 'butter.graph'))
    expected = set([
        fs('LA1', 'LA2', 'LA3', 'LB1', 'LB2', 'LB3'),
        fs('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'C')
    ])
    print(louvain(G))
def run_all() -> None:
    test_A()
    print(f"Tests from {__file__} passed.")

#
if __name__ == '__main__':
    run_all()