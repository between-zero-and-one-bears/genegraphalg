__all__ = ['run_all']

# for importing from parent directory
import sys
from os.path import join, dirname, abspath
sys.path.insert(1, join(sys.path[0], '..'))

global TDIR 
TDIR = dirname(abspath(__file__))

# actual imports
from core import *
from linclust import *
import parsing

G = {
        1: {
            2: 0.5
        },
        2: {
            3: 0.22
        }
    }
def linclust_deorder_helper(original: list[tuple[list[Any], Any]]) -> frozenset[tuple[frozenset[Any], Any]]:
    rewritten = set()
    for cluster in original:
        rewritten.add((frozenset(cluster[0]), cluster[1]))
    return frozenset(rewritten)
    

#

def test_GIC_small() -> None:
    G = parsing.graph_from_file(TDIR+'\\small_test.graph')
    Cs_l: list[tuple[list[str], str]] = greedy_incremental_clustering(G)
    Cs = set()
    for C in Cs_l:
        Cs.add(fs(*C[0]))
    Cs_f = fs(*Cs)
    assert(Cs_f == fs(fs('B', 'C', 'D', 'E'), fs('A'), fs('UC_A', 'UC_B'), fs('F')))
    
    

def test_linclust_minimal() -> None:
    Tags = {
        1: [1],
        3: [2],
        2: [1,2],
    }
    Sim = lambda x, y: access({1:{1:1.0,2:0.5},2:{2:1.0,3:0.22},3:{3:1.0}}, x, y)
    correct = fs((fs(1, 2, 3), 2))
    output = linclust_deorder_helper(linclust(Tags=Tags, Similarity=Sim))
    assert(correct==output)    
def test_A() -> None:
    Tags = {
        1: [1],
        2: [1, 2],
        3: [1, 2,       96],
        4: [2, 3],
        5: [2, 3, 4,    97],
        6: [2, 4],
        7: [3],
        8: [3, 4],
        9: [4],
        10:[4, 5],
        11:[5, 6,       98],
        12:[5, 6],
        13:[5, 6],
        14:[7],
        15:[7, 8],
        16:[7, 8,       99],
        17:[7, 8],
        18:[8],
    }
    G = parsing.graph_from_file('src/tests/linclust_paper.graph')
    Sim = lambda x, y: access(G, x, y)
    output = linclust_deorder_helper(linclust(Tags=Tags, Similarity=Sim))
    print(output)
    InterruptedError
def run_all() -> None:
    #test_A()
    #test_linclust_minimal()
    test_GIC_small()
    print(f"Tests from {__file__} passed.")

#
if __name__ == '__main__':
    run_all()