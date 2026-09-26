__all__ = ['graph_from_file']

from core import *

def _parsing_assign(D: WeightedGraph, Key1, Key2, Value: float) -> None:
    if Key1 > Key2:
        Key1, Key2 = Key2, Key1
    if Key1 in D.keys():
        if Key2 in D[Key1].keys():
            D[Key1][Key2] = max(D[Key1][Key2], Value)
        else:
            D[Key1][Key2] = Value
    else:
        D[Key1] = {Key2: Value}
def _parsing_note(D, Key):
    if not Key in D.keys():
        D[Key] = {}
def graph_from_file(file_location: str) -> WeightedGraph:
    
    G = {}
    file = open(file_location, mode='rt')
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        comps = [C for C in line.split() if C != '']
        if len(comps) >= 3:
            v = float(comps[2])
            if 0.0 < v <= 1:
                _parsing_assign(G, comps[0], comps[1], v)
        elif 0 < len(comps) < 3:
            _parsing_note(G, comps[0])
    return G




