# Louvain community detection method
#  https://en.wikipedia.org/wiki/Louvain_method
#
from typing import Mapping
from core import *
def get_modularities(G: WeightedGraph, communities: Iterable[Iterable[Any]]) -> list[float]:
    m = 0.0
    for key1 in G.keys():
        for key2 in G[key1].keys():
            m += G[key1][key2]
    modularities = []
    for C in communities:
        sum_internal = 0.0
        sum_overall = 0.0
        for n1 in C:
            for n2 in C:
                sum_internal += access(G, n1, n2)
            for n2 in neighbors(G, n2):
                sum_overall += access(G, n1, n2)
        modularity = (sum_internal / (2*m)) - (sum_overall / (2*m))**2
        modularities.append(modularity)
    return modularities
def get_modularity(G: WeightedGraph, C: Mapping[Any, Any]) -> float:
    m = 0.0
    for key1 in G.keys():
        for key2 in G[key1].keys():
            m += G[key1][key2]
    nl = list(nodes_set(G))
    k = {}
    for n in nl:
        k[n] = sum([access(G, n, j) for j in neighbors(G, n)])
    
    modularity = 0.0
    for i in nl:
        for j in nl:
            if C[i] == C[j]:
                modularity += access(G, i, j) - (k[i]*k[j])/(2*m)
    modularity /= (2*m)
    return modularity

def louvain(G: WeightedGraph):
    
    ...
    # def phase_1(G: WeightedGraph, C: dict[Any, int], nl: list[int]) -> tuple[dict[Any, int], float]:
    #     # results in a new partition C
    #     old_modularity = get_modularity(G, C)
    #     for n in nl:
    #         old_c = C[n]
    #         alt_c = set()
    #         for b in neighbors(G, n):
    #             alt_c.add(C[b])
    #         alt = {}
    #         found = False
    #         for c in alt_c:
    #             C[n] = c
    #             new_modularity = get_modularity(G, C)
    #             if new_modularity - old_modularity > 0:
    #                 alt[new_modularity] = c
    #                 found = True
    #         if found:
    #             new_modularity  = max(alt.keys())
    #             C[n] = alt[new_modularity]
    #             old_modularity = new_modularity
    #         else:
    #             C[n] = old_c
    #     return (C, old_modularity)
    
    def phase_1(CG: WeightedGraph, C: dict[Any, int], nl: list[int], old_modularity: float) -> tuple[dict[Any, int], dict[int, int], float]:
        """

        Args:
            CG (WeightedGraph): graph of communities & their relatedness
            C (dict[Any, int]): mapping from real nodes to communities
            nl (list[int]): list of real nodes
            old_modularity (float): modularity before (given to reduce wasted calculations)

        Returns:
            tuple[dict[Any, int], float]: 
            (
                new real mapping from nodes to communities,
                fake mapping from previous-iteration communities to new-iteration communities,
                new modularity
            )
        """
        cl = set(nodes_set(CG))
        false_map = {c:c for c in cl}
        for n in cl:
            alt_c: set[int] = set()
            for b in neighbors(CG, n):
                alt_c.add(false_map[b])
            alt: dict[float, int] = {}
            found = False
            for b in alt_c:
                false_map[n] = b
                new_modularity = get_modularity(CG, false_map)
                if new_modularity - old_modularity > 0:
                    alt[new_modularity] = b
                    found = True
            if found:
                new_modularity = max(alt.keys())
                false_map[n] = alt[new_modularity]
                old_modularity = new_modularity
                for r_n in nl:
                    if C[r_n] == n:
                        C[r_n] = false_map[n]
            else:
                false_map[n] = n
        return (C, false_map, new_modularity) 
    
    
    def phase_2(G: WeightedGraph, C: dict[Any, int]) -> WeightedGraph:
        # the names of the nodes of the output are the names of the communities they represent.
        Gn: WeightedGraph = {}
        nl = list(C.keys())
        N: int = len(nl)
        for i in range(N):
            for  b in nl[i:]:
                a = nl[i]
                to_add = access(G, a, b)
                old_v = access(Gn, C[a], C[b])
                assign(Gn, C[a], C[b], to_add + old_v)
        return Gn
    nl = list(nodes_set(G))
    C: dict[Any, int] = {}
    i = 0
    for n in nl:
        C[n] = i
        i += 1
    modularity = get_modularity(G, C)
    G_communities = phase_2(G, C)
    while True:
        C, false_mapping, new_modularity = phase_1(G_communities, C, nl, modularity)
        if new_modularity <= modularity:
            break 
        G_communities = phase_2(G_communities, false_mapping)
    
    return C
    
    