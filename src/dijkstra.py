__all__ = ['naive_dijkstra', 'very_naive_dijkstra']

from core import *

pos_inf = float('inf')

def naive_dijkstra(G: WeightedGraph, origin: Any, target: Any, /) -> None|dict[str, list[Any]|float]:
    """
    Runs a probably-badly-optimized Dijkstra path search algorithm.

    Args:
        G (two-layer dict to float): A simple weighted graph.
        origin (Any): Start node for finding a path.
        target (Any): End node for finding a path.
        max_steps (int, optional): Maximum number of steps to attempt, stopping the function from hanging if the nodes are actually in disconnected components of G. Defaults to 1000.
    Returns:
        None, if the algorithm fails;
        {'path': list[Any], 'cost': float}, if it finds a path. 'path' is the sequence of nodes (including the beginning and end point) and 'cost' is the sum of the weights of the edges between consecutive nodes in the path.
    """
    
    def update_best(best: dict[str, dict], node, source, edge_cost: float) -> None:
        if not node in best.keys():
            best[node] = {'src':None, 'cost':pos_inf}
        if best[node]['cost'] > best[source]['cost'] + edge_cost:
            best[node] = {'src':source, 'cost':best[source]['cost'] + edge_cost}
    def update_queue(Q: list, best: dict[str, dict], new: list) -> None:
        # Q: the queue [...[node, current min dist]...]
        # new: the new elements to the queue [...node...]
        # best: as below
        for node in [v for v in new if not v in [I[0] for I in Q]]:
            keys = [I[0] for I in Q]
            locs = [i for i in range(len(Q)) if keys[i] in new]
            locs.reverse()
            for loc in locs:
                Q.pop(loc)
#            Q.remove([node, best[node]])
        for node in new:
            cost = best[node]['cost']
            spot = binary_search([I[1] for I in Q], cost)
            Q.insert(spot, [node, cost])
    
    done = False
    queued_nodes = [[origin, 0.0]]
    explored_nodes = []
    best = {origin: {'src':None, 'cost':0.0}}
    # best = {node: [previous, total]}
    step_no = 0
    while (not done) and len(queued_nodes) > 0:
        step_no += 1
        node = queued_nodes.pop(0)[0]
        new = []
        for neighbor in neighbors(G, node):
            if neighbor in explored_nodes:
                continue
            cost = access(G, neighbor, node)
            update_best(best, neighbor, node, cost)
            new.append(neighbor)
        update_queue(queued_nodes, best, new)
        if node == target:
            done = True
            break
        explored_nodes.append(node)
    if done:
        cost = 0.0
        focus = target
        path = [target]
        for _ in range(step_no + 1): # just in case a loop happened or sth
            cost += best[focus]['cost']
            focus = best[focus]['src']
            if focus == None: # as in, once the origin node has been parsed since it has a best[origin] = {'src':None, 'cost':0.0}
                path.reverse()
                return {'path':path, 'cost':cost}
            path.append(focus)
            
        print("DEBUG: failed to reconstruct path in the max number of steps.")
        return None
    else:
        print("DEBUG: Never found a path.")
        print(best)
        return None

def very_naive_dijkstra(G: WeightedGraph, origin: Any, target: Any, /, maximize_weight=True) -> None | dict[str, list[Any]|float]:
    """
    A completely unoptimized dijkstra implementation.
    Finds the shortest path between the origin and target.
    If the parameter 'maximize_weight' is True, it maximizes the weight rather than minimizing.
    Args:
        G (WeightedGraph): ...
        origin (Any): the start of the path being found
        target (Any): the end of the path being found

    Returns:
        None: if there is no such path.
        {'path':list[Any],'cost':float}: Path and cost, if a path exists.
    """
    proc: Callable[[float], float] = (lambda x: 1/x) if maximize_weight else (lambda x: x)   

    def update_best(best: dict[str, dict[str, Any|float]], node, source, edge_cost: float) -> None:
        if not node in best.keys():
            best[node] = {
                'src':None, 
                'total':pos_inf
                }
        if best[node]['total'] > best[source]['total'] + edge_cost:
            best[node] = {
                'src':source, 
                'total':best[source]['total'] + edge_cost
                }
    def finish_up(best: dict[str, dict[str, Any|float]], target: Any, max_steps: int) -> dict[str, list[Any]|float] | None:
        cost: float = best[target]['total']
        focus: Any = target
        path: list[Any] = [target]
        for _ in range(max_steps + 1): # just in case a loop happened or sth
            focus = best[focus]['src']
            if focus == None: # as in, once the origin node has been parsed.
                path.reverse()
                return {'path':path, 'cost':cost}
            path.append(focus)
        # RecursionError("Failed to reconstruct path in the max number of steps.")
        return None
    def get_lowest(border: list[Any], best: dict[str, dict[str, Any|float]]) -> Any:
        bar: float = pos_inf
        opt: Any = None
        for node in border:
            if best[node]['total'] < bar:
                opt = node
                bar = best[node]['total']
        return opt
    
    done = False
    border = [origin]
    explored_nodes = []
    best = {origin: {'src':None, 'total':0.0}}
    step_no = 0
    while (not done) and len(border) > 0:
        step_no += 1
        node = get_lowest(border, best)
        if node == target:
            done = True
            return finish_up(best, target, step_no)
        
        border.remove(node)
        explored_nodes.append(node)
        for neighbor in neighbors(G, node):
            if neighbor in explored_nodes:
                continue
            #print(f"explored_nodes: \n\t\t{explored_nodes}\nG: \n\t\t{G}\nneighbour: \n\t\t{neighbor}\nnode: \n\t\t{node}")
            inc_cost = proc(access(G, neighbor, node))
            update_best(best, neighbor, node, inc_cost)
            if neighbor not in border:
                border.append(neighbor)
    return None
                
            
            
            
            
            
            

    
                    
                