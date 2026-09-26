__all__ = ['run_all']

# for importing from parent directory
import sys
from os.path import join, dirname, abspath
sys.path.insert(1, join(sys.path[0], '..'))

global TDIR 
TDIR = dirname(abspath(__file__))

# actual imports
import core
from core import *
from floydwarshall import *
import parsing

#
def test_no_reconstruction_linear() -> None:
    G = parsing.from_file(join(TDIR,'small_test.graph'))
    MC = parsing.from_text('''
        A A 0
        A B 0.5
        A C 1
        A D 1.3
        A E 1.4
        A F 1.6
        A UC_A infinity
        A UC_B infinity
        B B 0
        B C 0.5
        B D 0.8
        B E 0.9
        B F 1.1
        B UC_A infinity
        B UC_B infinity
        C C 0
        C D 0.3
        C E 0.4
        C F 0.6
        C UC_A infinity
        C UC_B infinity
        D D 0
        D E 0.1
        D F 0.3
        D UC_A infinity
        D UC_B infinity
        E E 0
        E F 0.2
        E UC_A infinity
        E UC_B infinity
        F F 0
        F UC_A infinity
        F UC_B infinity
        UC_A UC_A 0
        UC_A UC_B 0.7
        UC_B UC_B 0
    ''')
    M = floyd_warshall_no_reconstruction_linear(G)
    print(M)
    assert(core.compare_weighted_graphs(M, MC))
def run_all() -> None:
    test_no_reconstruction_linear()
    print(f"Tests from {__file__} passed.")

#
if __name__ == '__main__':
    run_all()