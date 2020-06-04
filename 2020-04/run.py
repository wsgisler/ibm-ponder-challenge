import numpy as np
from itertools import combinations
from time import time
import networkx as nx

def infection_probability(v, infected_vertices, edges, r):
    # probability that v gets effected if all vertices in s1 are infected and the vertices are connected by edges and the probability of getting infected by one single neighboring vertice is r
    prob = 0
    dangerous_edges = 0
    for infected in infected_vertices:
        if (infected, v) in edges or (v, infected) in edges:
            dangerous_edges += 1
    return ((1/(1-r))**dangerous_edges-1)*(1-r)**dangerous_edges

def transition_probability(s1, s2, vertices, edges, r):
    s1 = set(s1)
    s2 = set(s2)
    if len(s1.intersection(s2)) < len(s1):
        return 0
    else:
        to_infect = s2 - s1
        prod = 1
        for v in to_infect:
            prod = prod*infection_probability(v, s1, edges, r)
        for v in vertices:
            if v not in to_infect and v not in s1:
                prod = prod*(1-infection_probability(v, s1, edges, r))
        return prod

def calculate_with_markov(vertices, edges, tt, r):
    states = []
    for num_nodes in range(1,len(vertices)+1):
        states += list(combinations(vertices, num_nodes))
    #print(states)
    tm = [[0 for st in states] for st in states]
    for i1,s1 in enumerate(states):
        for i2,s2 in enumerate(states):
            tm[i1][i2] = transition_probability(s1, s2, vertices, edges, r)
    #print(tm)
    m = np.matrix(tm)
    sv = np.matrix([1 if state in [('a', ), (0, )] else 0 for state in states])
    return (sv*m**tt)[0,-1]
    
def find_graph_with_probability(vertices, target_probability, num_phases, infection_rate):
    start_time = time()
    count = 0
    all_edges = list(combinations(vertices, 2))
    best_diff = 10000
    best_graph = {}
    for selected_num_edges in range(len(vertices)-1, len(all_edges)+1): # we look at all connected graphs. A condition for a graph to be connected is that the number of edges is at least |vertices|-1
        for edges in combinations(all_edges, selected_num_edges):
            count += 1
            diff = abs(calculate_with_markov(vertices, edges, num_phases, infection_rate)-target_probability)
            if diff < best_diff:
                best_diff = diff
                best_graph = edges
    print(best_graph)
    print(calculate_with_markov(vertices, best_graph, num_phases, infection_rate))
    end_time = time()
    print('Number of graphs evaluated: %i, time spent total: %f, graphs per second: %f'%(count, end_time-start_time, count/(end_time-start_time)))
    
def find_graph_with_probability_in_file(file_path, target_probability, num_phases, infection_rate):
    graphs = nx.read_graph6(file_path)
    best_diff = 10000
    best_graph = None
    for G in graphs:
        vertices = G.nodes()
        edges = G.edges()
        for v in vertices:
            edges_copied = [[e[0], e[1]] for e in edges]
            for index, edge in enumerate(edges_copied):
                if edge[0] == v:
                    edge[0] = -1
                if edge[1] == v:
                    edge[1] = -1
                if edge[0] == 0:
                    edge[0] = v
                if edge[1] == 0:
                    edge[1] = v
                if edge[0] == -1:
                    edge[0] = 0
                if edge[1] == -1:
                    edge[1] = 0
                edges_copied[index] = (edge[0], edge[1])
            diff = abs(calculate_with_markov(vertices, edges_copied, num_phases, infection_rate) - target_probability)
            if diff < best_diff:
                best_diff = diff
                best_graph = edges_copied
    print(best_graph)
    for row in vertices:
        line = ''
        for column in vertices:
            line += '1' if (row,column) in best_graph or (column, row) in best_graph else '0'
        print(line)
    print(calculate_with_markov(vertices, best_graph, num_phases, infection_rate))
        
vertices = ['a','b','c','d','e']
edges = {('a','b'),('a','c'),('a','d'),('b','e'),('e','d'),('c','d')}
tt = 10
r = 0.1
    
# find_graph_with_probability_in_file('g5.txt', 0.7, 10, 0.1) 
# find_graph_with_probability_in_file('g6.txt', 0.7, 10, 0.1)
# find_graph_with_probability_in_file('g7.txt', 0.7, 10, 0.1)
# find_graph_with_probability_in_file('g8.txt', 0.7, 10, 0.1)
print('with 19 days')
find_graph_with_probability_in_file('g5.txt', 0.7, 19, 0.1) 
find_graph_with_probability_in_file('g6.txt', 0.7, 19, 0.1)
find_graph_with_probability_in_file('g7.txt', 0.7, 19, 0.1)
find_graph_with_probability_in_file('g8.txt', 0.7, 19, 0.1)