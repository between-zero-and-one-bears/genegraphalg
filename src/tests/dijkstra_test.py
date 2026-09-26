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
import dijkstra

# 
def basic_test() -> None:
    G = parsing.graph_from_file(join(TDIR,'small_test.graph'))
    res = dijkstra.very_naive_dijkstra(G, 'A', 'E', maximize_weight=False)
    assert(res != None)
    assert(res['path'] == ['A', 'B', 'C', 'D', 'E'])
    assert(res['cost'] == 1.4)
def failure_test() -> None:
    G = parsing.graph_from_file(join(TDIR,'small_test.graph'))
    res = dijkstra.very_naive_dijkstra(G, 'A', 'UC_A', maximize_weight=False)
    assert(res == None)

def run_all():
    basic_test()
    failure_test()
    print(f"Tests from {__file__} passed.")

#
if __name__ == '__main__':
    run_all()    