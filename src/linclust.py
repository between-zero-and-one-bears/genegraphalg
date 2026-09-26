__all__ = ['greedy_incremental_clustering', 'linclust']

from core import *
import parsing

def greedy_incremental_clustering(G: WeightedGraph, /, quality: Callable[[Any], float] | None = None, include_ctr_in_clust_list=True) -> list[tuple[list[Any], Any]]:
    """
    Separates G into disjoint clusters, where each cluster's connectedness to its center is maximized.

    Args:
        G (WeightedGraph): 
            A weighted graph from which to create clusters.
        quality (Callable[[Any], float] | None, optional): 
            Higher 'quality(item)' means 'item' is more likely to be the center of a cluster.
            Defaults to None, where the quality of the node is the sum of weights of its incident edges.
        include_ctr_in_clust_list (bool, optional): 
            See Returns. 
            Defaults to True.

    Returns:
        list[tuple[Any, list[Any]]]: 
            A list of (cluster, center) pairs, where 'cluster' is a list of nodes and 'center' is a node.
            'cluster' includes the 'center' iff 'include_ctr_in_clust_list' is true.
            
    """
    nodes = nodes_set(G)
    nodes_list: list[Any] = list(nodes)
    if quality == None:
        # sum all weights of edges to node
        priorities_pre: dict[Any, float] = dict(map(lambda x: (x, 0.0), nodes_list))
        for key1 in G.keys():
            for key2 in G.keys():
                v: float = access(G, key1, key2)
                priorities_pre[key1] += v
        # prep for sorting
        priorities_pre2: list[tuple[Any, float]] = [(key, priorities_pre[key]) for key in priorities_pre.keys()]
    else:
        # prep for sorting
        priorities_pre2 = list(map(lambda x: (x, quality(x)), nodes_list))
    priorities: list[tuple[Any, float]] = sorted(priorities_pre2, key=lambda x:x[1], reverse=True)
    order = [i[0] for i in priorities]
    
    
    centers: list[Any] = []
    while len(order) > 0:
        top = order.pop(0)
        centers.append(top)
        for other in neighbors(G, top):
            if other in order:
                order.remove(other)
    
    assignment: dict[Any, Any] = dict()
    for node in nodes.difference(set(centers)):
        best_ctr: Any = None
        best_conn: float = 0.0
        for center in centers: 
            v = access(G, center, node)
            if v > best_conn:
                best_ctr = center
                best_conn = v
        assignment[node] = best_ctr
    
    clusters_dict: dict[Any, set[Any]] = {center: set() for center in centers}
    for node in assignment.keys():
        clusters_dict[assignment[node]].add(node)
    clusters_nf: list[tuple[Any, set[Any]]] = [(key, clusters_dict[key]) for key in clusters_dict.keys()]
    if include_ctr_in_clust_list:
        for item in clusters_nf:
            item[1].add(item[0])
    clusters: list[tuple[Any, list[Any]]] = []
    for item in clusters_nf:
        clusters.append((list(item[1]), item[0]))
    # list[tuple[CENTER, {*LEAVES}]]
    return clusters



import random
from collections.abc import Mapping
def linclust(Tags: Mapping[Any, Sequence[Any]], Similarity: Callable[[Any, Any], float], tag_groups_per_seq: int = 20) -> list[tuple[list[Any], Any]]:
    """
    An implementation of the Linclust algorithm:
        Steinegger, M., Söding, J. Clustering huge protein sequence sets in linear time. Nat Commun 9, 2542 (2018). https://doi.org/10.1038/s41467-018-04964-5
    It is recommended to have tags and nodes be numbers, and map back to the original values afterward and within the comparison.

    Arguments:
        Tags (dict[Any, Iterable[Any]]): 
            A mapping from nodes to lists of tags. 
            All nodes must be in this dictionary, though they may map to an empty set.
            Elements in the same cluster at output are likely to share a tag. 
            In the the paper, the tags represent particular 'k-mers'.
        Similarity (Callable[[Any, Any], float]): 
            Costly comparison for similarity between Item1 and Item2, resulting in a float between 0 and 1. 
            Linclust minimizes usage of this comparison.
        tag_groups_per_seq (int): 
            Number of tags per sequence to fully explore.
            In the paper, this is the value m .
    Returns:
        list[tuple[list[Any], Any]]:
            A list of tuples of a cluster and its center.

    """
    nodes_by_centerness = sorted([(key, len(Tags[key])) for key in Tags.keys()], key=lambda x: x[1], reverse=True)
    # nodes_list is the same as the original, but now sorted in order of decreasing number of applied tags.
    nodes_list = list(map(lambda x: x[0], nodes_by_centerness))
    
    # tags_to_explore is a set of tags which have been picked to ensure every node has at least a minimum number of its tags as possible clusters it would belong to.
    tags_to_explore: set[Any] = set()
    # not_done tracks the set of nodes which have not had this process done upon them.
    for node in nodes_list:
        lacking = tag_groups_per_seq - len(intersection(Tags[node], tags_to_explore))
        if lacking <= 0:
            continue
        options = list(asym_difference(Tags[node], tags_to_explore))
        if len(options) <= lacking:
            tags_to_explore.update(options)
        else:
            tags_to_explore.update(random.choices(options, k=lacking))
    
    # tag_groups_sans_center lists each tag along with its elements.
    tag_groups_sans_center: dict[Any, Sequence[Any]] = dict()
    for tag in tags_to_explore: 
        items = []
        for node in nodes_list: 
            if tag in Tags[node]:
                items.append(node)
        tag_groups_sans_center[tag] = items
    
    # centers_set lists the centers of all tag groups, i.e. whichever node in the group has the most tags (maximizing center intersection).
    centers_set = set()
    # item_center_assignment lists the possible centers that a given node could be clustered with.
    item_center_assignment: dict[Any, set[Any]] = dict()
    for tag in tag_groups_sans_center.keys():
        tag_g = tag_groups_sans_center[tag]
        center = None
        for center_candidate in nodes_list:
            if center_candidate in tag_g:
                # Since the nodes are listed in order of decreasing number of tags, the first candidate that is in the tag group is one with a maximum number of tags.
                center = center_candidate
                break
        # All tags should have at least one node, otherwise they would not even be on the list of tags. Really, this and the first assignment of center can both be removed.
        assert(center != None)
        centers_set.add(center)
        for item in tag_g:
            if item in item_center_assignment.keys():
                item_center_assignment[item].add(center)
            else:
                item_center_assignment[item] = {center}
    print(centers_set)
    print(item_center_assignment)
    clusters_dict: dict[Any, list[Any]] = {center:[] for center in centers_set}
    for item in item_center_assignment.keys():
        # Compare to every relevant cluster's center.
        chosen = None
        bar = 0.0
        for center in item_center_assignment[item]:
            sim = Similarity(item, center)
            if sim > bar:
                chosen = center
                bar = sim
        # Send it off to whichever center has the best similarity to the node.
        print(item, chosen)
        clusters_dict[chosen].append(item)
    
    return [(clusters_dict[cent], cent) for cent in clusters_dict.keys()]
    
                        
        
                
                
        
    
    
        
        
    
    
    
    
    
    
    
            
    

    
    
    
    
                        
        
        































































































# https://web.archive.org/web/20260904030127/https://watermark02.silverchair.com/bioinformatics_32_9_1323.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAAAm8wggJrBgkqhkiG9w0BBwagggJcMIICWAIBADCCAlEGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMNWAELyIDgoGqGFUDAgEQgIICIlud0SUJeB8N4P3ff3P4usjAKqYXFvM2pV_rQTCo_toViYMFihXxj5VT0ZhGwMltf3Y-9J1MTHGsaSx49EbfYzB0waiQBIWMGTyVrUq7nUE4TPwNuyTYQTfUURZQcQRMmPmMs5GJhoWF9JWP2r3reJTZm8GPFIUBcB-wCnbMEFiE1Xn4DuTyU2cs6MqYwVRfe3qfPBzXPzXVLOhsFZVF-h0ltwq0fvFo9cam8UzgeiuS2IKb92KsHOMfjxwAMnHvAcr6A9BBqk6blirVngVeJ8j3ECMyvMd7AvlxgeHt-BiMCpM7oQm7_aL6DWkHTHo4eeXbyg1t9uca8SXyJskqVxq4BEKSHTUVqycRGtM038L7DzzEjOU-3-xhFdTOjAZFvaBgmB8uYbcD0D9OjmviSWf445JsZmnYIGsOdZKtaHvHVM7wqVvMIOo0LDN40vvYSvF9MMrqKeg-1sVu-4jO8QA122awtyxs2GKoIivjs-GYBXv0B0Ac-RBw7dvcgpKWPBCOIAVmoc72OvLsHuEFWpxMCwmAEIcGvq9QJXlbP9MAKRIH7kfX958xdtlIrQrf1YC8YDcw7RhEQY2lKoibqrdpCbSxIw8WD4DKj0HQ21G6j0uhgty-nT7D_rM0Esmwd4VB87T1FbQsekvXH1PZdWMpI88rO4hdQp7S3YjHAnXuFRh_tcqSHPFzgmQ56sMnKF_UsXfSyTQ8Vy3ffR

### based on:
# MMseqs software suite for fast and deep clustering and searching of large protein sequence sets
# Hauser, Steinegger, and So¨ding 
# Bioinformatics
# Jan 2016

# specifically, their (iii) clustering module.
# i'm assuming that data given will give the 
#       "[...] Smith-Waterman alignments between query-target pairs that pass a prefilter Z-score threshold."
# that are necessary.

# found their code (at 11:51 PM 9/3/2026):
# https://github.com/martin-steinegger/setcover
# can't read c++ though, so...
# and anyways it's copyrighted.






















