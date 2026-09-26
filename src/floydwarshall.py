# The Floyd-Warshall Algorithm
# https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
# Finds the lengths of shortest paths between all vertices in a directed weighted graph.

from core import *

def floyd_warshall_no_reconstruction_linear(G: WeightedGraph) -> WeightedGraph:
    nodes: list[Any] = list(nodes_set(G))
    M: WeightedGraph = {}
    for a in range(len(nodes)-1):
        for b in range(a+1, len(nodes)):
            assign(M, nodes[a], nodes[b], access(G, nodes[a], nodes[b], default_to_inf=True))
    for n in nodes:
        assign(M, n, n, 0.0)
    for k in nodes:
        for i  in nodes:
            for j in nodes:
                c = access(M,i,k)+access(M,j,k)
                if access(M, i, j) > c:
                    assign(M,i,j,c)
    return M
