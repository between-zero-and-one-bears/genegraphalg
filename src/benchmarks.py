__all__ = []

from core import *
from random import random, choices

def power_law(n: int, exp:float, minimum: float = 1, maximum: float = inf) -> list[int]:
    """
    Sampling a discretized Pareto distribution.
    If exp > 1 and minimum is unset (∞), the mean is (exp ⋅ minimum) / (exp − 1).
    If exp ≤ 1, mean is ∞ .
    
    Args:
        n (int): Number of observations in sample > 0 .
        exp (float): Shape variable (falloff exponent) > 1.0 . Usually called α.
        minimum (float): Below this, no observations are found; the probability density here is highest. Usually called Xₘᵢₙ , or in the context of Pareto distributions, just xₘ .
        maximum (float): Maximum value from the distribution. Usually called Xₘₐₓ .

    Returns:
        list[int]: Sample with list of observations.
    """
    assert(n >= 0)
    scale = 1.0 if maximum == inf else (1-((minimum / maximum)**exp))
    cdf_heights = [random()*scale for _ in range(n)]
    v = map(lambda v: ((1-v)**(-(1/exp))), cdf_heights)
    final = map(lambda u: (round(minimum * u,)), v)
    return list(final)
def power_law_sum_defined(n: int, reqsum: int, exp:float, minimum: int = 1, maximum: int|None = None) -> list[int]:
    """

    Args:
        n (int): Number of observations in sample > 0 .
        reqsum (int): Sum of observations.
        exp (float): _description_
        minimum (int, optional): _description_. Defaults to 1.
        maximum (int | None, optional): _description_. Defaults to None.

    Returns:
        list[int]: _description_
    """
    assert(reqsum >= n * minimum)
    assignments = power_law(n=reqsum - n*minimum, exp=1.5, minimum=1, maximum=n)
    res: list[int] = [minimum]*n
    for i in assignments:
        res[i-1] += 1
    # Sorry. Not max-bounded.
    return res
def power_law_sum_defined_no_n(reqsum:int, exp:float, minimum:int=1, maximum:int|None=None):
    assert(reqsum == 0 or reqsum >= minimum)
    ma = reqsum if maximum == None else maximum
    so_far = 0
    res = []
    while so_far < reqsum:
        
        
    
    

print(power_law(n=50,exp=2.0, minimum=7.0, maximum=17.0))



def lancichinetti(N: int, average_degree: float, mixing_parameter: float, gamma: float, beta: float, ) -> tuple[WeightedGraph, dict[int, int]]:
    γ = gamma; β = beta; μ = mixing_parameter;
    degrees_unassigned = power_law(n=N, exp=1.5000000) # minimum, maximum, and exp chosen so mean is average_degree
    degrees_split = list(map(lambda x: (x*μ, x*(1-μ)), degrees_unassigned))
    community_sizes = power_law_sum_defined(exp=β)
    homeless = list(range(N))
    community_assignment: list[list[int]] = [[]]*len(community_sizes)
    while len(homeless) > 0:
        #homeless.sort(key=lambda x:random())
        assignment = choices(list(range(len(community_sizes))), k=len(homeless))
        still_homeless = []
        for node_i in homeless:
            if degrees_split[node_i][1] < community_sizes[assignment[node_i]]:
                community_assignment[assignment[node_i]].append(node_i)
                            
    
    
    
    
    return ...