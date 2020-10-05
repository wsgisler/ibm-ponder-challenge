from itertools import permutations
import networkx as nx

weapons = [0,1,2,3,4]
beats = {0: [1,3], 1: [2,4], 2: [0,3], 3: [1,4], 4: [0,2]}

# this one can solve the challenge
weapons = [0,1,2,3,4,5,6,7,8]
beats = {0: [2,3,4,6], 
         1: [0,3,5,7], 
         2: [1,4,7,8], 
         3: [2,4,5,6], 
         4: [1,6,7,8], 
         5: [0,2,4,6], 
         6: [1,2,7,8], 
         7: [0,3,5,8], 
         8: [0,1,3,5]}
         
beats = {
0: [1, 2, 4, 5],
1: [3, 4, 6, 7],
2: [1, 4, 5, 8],
3: [0, 2, 7, 8],
4: [3, 5, 6, 7],
5: [1, 3, 6, 7],
6: [0, 2, 3, 8],
7: [0, 2, 6, 8],
8: [0, 1, 4, 5]
}

# bonus question
# weapons = [0,1,2,3,4,5,6,7,8,9,10]
# beats = {
# 0: [1, 2, 3, 4, 5],
# 1: [2, 5, 7, 9, 10],
# 2: [3, 4, 8, 9, 10],
# 3: [1, 4, 6, 7, 9],
# 4: [1, 5, 6, 8, 10],
# 5: [2, 3, 6, 7, 8],
# 6: [0, 1, 2, 8, 9],
# 7: [0, 2, 4, 6, 10],
# 8: [0, 1, 3, 7, 10],
# 9: [0, 4, 5, 7, 8],
# 10: [0, 3, 5, 6, 9]
# }

counter = 0
for perm in permutations(weapons):
    new_beats = dict()
    for old_index, new_index in enumerate(perm):
        new_beats[new_index] = beats[old_index]
    for i in new_beats:
        ne = []
        for j in new_beats[i]:
            ne.append(perm[j])
        new_beats[i] = sorted(ne)
    good = True
    for i in beats:
        if beats[i] != new_beats[i]:
            good = False
            break
    if good:
        counter += 1
        special = ''
        G = nx.Graph()
        for i,j in enumerate(perm):
            if i != j:
                G.add_edge(i,j)
        if G.size() == 0 or nx.is_connected(G):
            special = ' *' # an asterix is added if the permutation can be expressed in one single connected graph
        print(str(perm) + special)

print(counter)