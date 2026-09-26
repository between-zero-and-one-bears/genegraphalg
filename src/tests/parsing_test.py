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

#
def testingtesting() -> None:
    G = parsing.from_file(join(TDIR,'testingtesting.graph'))
    print(G)
    correct = "{'nom': {'om': 0.99, 'yom': 0.67}, 'om': {'yom': 0.8777}, 'GCA_016865505.2': {'GCF_003330725.1': 0.734}, 'sandwiches': {'soups': 0.78}}"
    assert(str(G) == correct)
def small_test() -> None:
    G = parsing.from_file(join(TDIR, 'small_test.graph'))
    correct = "{'A': {'B': 0.5}, 'B': {'C': 0.5}, 'C': {'D': 0.3, 'E': 0.5}, 'D': {'E': 0.1}, 'E': {'F': 0.2}, 'UC_A': {'UC_B': 0.7}}"
    print(G)
    assert(str(G) == correct)
    
def run_all() -> None:
    testingtesting()
    small_test()
    print(f"Tests from {__file__} passed.")

#
if __name__ == '__main__':
    run_all()