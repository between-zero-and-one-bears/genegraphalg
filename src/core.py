__all__ = ['Any', 'Callable', 'TypeVar', 'Iterable', 'Sequence', 'access', 'assign', 'pop_edge', 'neighbors', 'binary_search', 'WeightedGraph', 'nodes_set', 'intersection', 'asym_difference', 'fs', 'invert_map', 'map_to_set']

# For static typing.
from typing import Any, TYPE_CHECKING, Callable, TypeVar, Iterable, Sequence, Mapping
type WeightedGraph = dict[Any, dict[Any, float]]


# There's no way to natively make symmetric dictionaries in Python, so I just wrote a few small functions.
def access(D: WeightedGraph, Key1: Any, Key2: Any, /, default_to_inf = False) -> float:
    """
    Args:
        D (two-layer dict to float): the graph
        Key1 (Any): one node
        Key2 (Any): other node

    Returns:
        float: weight of edge between Key1 and Key2
    """
    if Key1 > Key2:
        Key1, Key2 = Key2, Key1    
    if Key1 in D.keys():
        if Key2 in D[Key1].keys():
            return D[Key1][Key2]
    
    return float('infinity') if default_to_inf else 0.0
...
def compare_weighted_graphs(G1: WeightedGraph, G2: WeightedGraph, /, tolerance: float = 0.01) -> bool:
    """
    Checks if two weighted graphs are the same, up to isomorphism with respect to vertex labels

    Args:
        G₁ (WeightedGraph)
        G₂ (WeightedGraph)
        tolerance (float): Maximum error on any edge before returning False.

    Returns:
        bool: If the set of vertex names V is the same for each, and ∀ v, w ∈ V, (G₁[v w] ≈ G₂[v w]) within the provided tolerance, then return True.
    """
    ns = nodes_set(G1)
    if ns != nodes_set(G2):
        return False
    nl = list(ns)
    for a in range(len(ns)):
        for b in range(a, len(ns)):
            if access(G1, nl[a], nl[b]) - access(G2, nl[a], nl[b]) > 0.01:
                return False
    return True
def assign(D: WeightedGraph, Key1: Any, Key2: Any, Value: float) -> None:
    if Key2 > Key1:
        Key1, Key2 = Key2, Key1
    if Key1 in D.keys():
        D[Key1][Key2] = Value
    else:
        D[Key1] = {Key2: Value}
def pop_edge(D: WeightedGraph, Key1: Any, Key2: Any) -> float|None:
    if Key1 > Key2:
        Key1, Key2 = Key2, Key1
    if Key1 in D.keys():
        if Key2 in D[Key1].keys():
            return D[Key1].pop(Key2)
    return None
def neighbors(D: WeightedGraph, Key1: Any) -> list[Any]:
    neighbors_list: list[Any] = []
    if Key1 in D.keys():
        neighbors_list.extend(D[Key1].keys())
    for Key2 in D.keys():
        if Key1 in D[Key2].keys():
            neighbors_list.append(Key2)
    return neighbors_list
def binary_search(L: list, V: Any, /, comparison = lambda x, y: (x < y)) -> int:
    # L: a list of values comparable to V via the < operator
    # V: a value comparable to the elements of L
    # comparison: a comparison operator, defaulting to < .
    #--> index I to insert V (pushing elements I, I+1, I+2, etc over).
    minspot = 0
    maxspot = len(L) - 1
    while minspot < maxspot:
        med = (minspot + maxspot) // 2
        if comparison(V, L[med]):
            maxspot = med
        else:
            minspot = med
    return minspot
def nodes_set(G: WeightedGraph):
    keys = set()
    for key1 in G.keys():
        keys.add(key1)
        for key2 in G[key1].keys():
            keys.add(key2)
    return keys
def intersection(L1: Iterable[Any], L2: Iterable[Any]) -> set[Any]:
    out = set()
    for i in L1:
        if i in L2:
            out.add(i)
    return out
def asym_difference(L1: Iterable[Any], L2: Iterable[Any]) -> set[Any]:
    out = set()
    for i in L1:
        if not i in L2:
            out.add(i)
    return out
def fs(*args: Any) -> frozenset[Any]:
    """
    Args:
        a, b, c, ...

    Returns:
        {a, b, c, ...} as a frozenset
    """
    s = set()
    for item in args:
        s.add(item)
    return frozenset(s)
def invert_map(D: Mapping[Any, Any]) -> dict[Any, frozenset[Any]]:
    """
    Args:
        Mapping[A, B]

    Returns:
        dict[B, frozenset[A]]
    """
    I: dict[Any, set[Any]] = {}
    V: set[Any] = set()
    for v in D.keys():
        v = D[v]
        if v in V:
            I[v].add(v)
        else:
            V.add(v)
            I[v] = {v}
    F: dict[Any, frozenset[Any]] = {}
    for v in I.keys():
        F[v] = frozenset(I[v])
    return F
def map_to_set(D: Mapping[Any, Any]) -> set[Any]:
    """
    Args:
        Mapping[A, B]

    Returns:
        set[B]
    """
    V: set[Any] = set()
    for key in D.keys():
        V.add(D[key])
    return V