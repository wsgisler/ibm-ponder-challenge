from docplex.mp.model import Model
from random import random
from time import time

def solve(g):
    n = len(g)
    
    model = Model()

    choice = {(r,c): model.binary_var(name = 'choice_%i_%i'%(r,c)) for r in range(n) for c in range(n)}
    changes = {(r,c): model.integer_var(lb = 0, ub = n, name = 'changes_%i_%i'%(r,c)) for r in range(n) for c in range(n)} # ub = n: it makes no sense to toggle a light bulb twice; hence, in the worst case, for a position, each bulb in the same row and in the same column are toggled once, resulting in n changes
    
    # Calculate the number of toggles for each cell
    num_toggles = dict()
    for r in range(n):
        for c in range(n):
            num_toggles[(r,c)] = model.sum(choice[(r2,c2)] for r2 in range(n) for c2 in range(n) if r2 == r or c2 == c)
            
    # relation between the number of toggles and the light being toggled or not
    for r in range(n):
        for c in range(n):
            if g[r][c] == 1:
                model.add(num_toggles[r,c] == changes[r,c]*2) # If the grid already contains a 1, the light has to be switched on and off an even number of times
            else:
                model.add(num_toggles[r,c] == changes[r,c]*2+1) # If the grid contains a 0, the light has to be switched on and off an uneven number of times (at least once)

    model.minimize(model.sum(choice[r,c] for r in range(n) for c in range(n)))

    solved = model.solve(log_output = True)

    #model.export_as_lp('model.lp')
    
    if solved:
        solution_sequence = []
        ss = []
        for r in range(n):
            for c in range(n):
                if choice[r,c].solution_value > 0.5:
                    solution_sequence.append((c+1,n-r))
                    ss.append((r,c))
        print(solution_sequence)
        return ss
        
def clone_and_modify_grid(g, choice):
    n = len(g)
    newg = []
    r,c = choice[0],choice[1]
    for i in range(n):
        newg.append(g[i].copy())
    for r2 in range(n):
        newg[r2][c] = 1-g[r2][c]
    for c2 in range(n):
        newg[r][c2] = 1-g[r][c2]
    return newg
    
def priority(g, choice, priorities = [1,3,2]):
    row = sum(g[choice[0]])
    col = sum(g[i][choice[1]] for i in range(len(g)))
    if row%2 == 1 and col%2 == 1:
        return priorities[0]+random()/1000
    elif row%2 == 0 and col%2 == 0:
        return priorities[1]+random()/1000
    else:
        return priorities[2]+random()/1000
        
def rsf(g, choices, seq = [], time_limit = 10, start_time = time(), prios = [1,2,3]): # recursive sequence finder
    n = len(g)
    if time()-start_time > time_limit:
        return False
    
    priorities = {ch:priority(g,ch) for ch in choices}
    choices = sorted(choices, key=lambda ch: priority(g, ch, priorities = prios))
    for ch in choices:
        if g[ch[0]][ch[1]] == 0:
            newchoices = choices.copy()
            newchoices.remove(ch)
            newseq = seq.copy()
            newseq.append((ch[1]+1,n-ch[0]))
            if len(newchoices) == 0:
                return newseq
            if time()-start_time > time_limit:
                return False
            else:
                result = rsf(clone_and_modify_grid(g, ch),newchoices, newseq, time_limit, start_time)
            if result:
                return result 
    # if len(seq) < 420:
#         print(len(seq)) # Whenever it fails, print the sequence
    return False
    
ig = [[0,0,1,1],
[1,1,0,1],
[0,1,1,0],
[0,0,0,1]]

ig2 = [[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1],
[1,1,0,1,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,1,0,0,1,1],
[0,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1,1,1,0],
[0,0,0,1,1,0,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,1,0,0],
[1,0,1,1,0,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,1,0,1,0],
[1,1,1,0,0,0,1,0,0,1,0,1,1,1,0,1,0,0,1,0,1,0,0,0],
[1,1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
[1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0],
[0,0,0,1,1,0,0,1,0,0,1,0,1,1,0,1,1,0,1,0,1,0,0,1],
[0,1,1,1,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,0,0,0,0],
[0,1,1,0,0,0,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,1,0,0],
[1,0,0,0,1,1,1,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,1,1],
[0,0,0,1,1,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,1,1,1,0],
[0,1,1,0,0,1,0,1,0,0,0,1,0,0,1,1,1,1,1,1,0,1,0,1],
[1,1,0,0,0,1,0,0,0,0,1,0,1,1,1,0,0,0,1,0,0,0,0,0],
[0,0,0,0,0,0,1,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1],
[1,1,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,1,1,1,0,1,1,0],
[1,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,0,1,1,0,1,0],
[1,1,0,1,0,0,0,0,0,0,1,1,1,0,0,1,0,0,1,1,0,0,1,0],
[1,0,1,0,0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,1,0,0,0,0],
[1,1,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,0,1],
[1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,0,0,0,1,0,1,0,1],
[0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,1,1,1,0,0,0,0,0],
[1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1]]

ig3 = [[1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,0,1,1,0,0,1,0,0,0],
[0,1,0,1,0,0,0,0,1,1,0,0,0,1,1,1,0,1,0,1,0,1,1,1,1,0,0,1,1,0],
[0,0,0,1,1,0,0,1,1,0,1,0,0,1,1,1,1,1,1,0,0,0,1,0,1,0,0,0,1,0],
[1,1,1,1,0,1,1,1,0,1,1,0,0,1,1,1,0,1,1,1,0,1,0,0,1,1,0,0,0,1],
[0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,0,1,0],
[1,0,1,1,1,1,0,0,1,1,1,0,1,1,0,0,1,0,1,1,1,1,0,1,0,0,1,1,1,1],
[0,0,1,1,1,0,0,0,0,1,0,1,1,0,1,0,0,1,1,0,1,0,0,0,0,0,1,1,0,1],
[1,1,1,0,0,1,1,1,0,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0],
[1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,1,0,0],
[1,1,1,0,0,1,1,1,0,1,0,0,1,1,1,1,1,0,0,0,1,1,1,0,1,1,1,0,1,1],
[1,1,1,0,1,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,1,1,0,0],
[0,1,0,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,0,1,0,0,0,0,1,0,0,1],
[0,1,0,1,0,0,1,1,1,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0],
[0,1,0,0,0,1,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,0,1],
[1,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,0,0,1,0,1,1,0,0,1,1,0,1,1,0],
[1,0,1,0,0,0,1,1,0,1,1,0,0,1,0,1,1,1,1,1,1,0,1,1,0,0,1,0,0,1],
[1,1,1,0,1,1,0,0,0,1,0,0,1,0,1,1,1,1,1,0,1,0,0,1,1,0,0,0,1,0],
[1,0,1,0,0,1,1,0,0,0,1,1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
[1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,0,1,1,1,1,1,0,0,1,0],
[0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1],
[1,1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1,0,0,1,1,0,1,1,0],
[0,1,1,1,0,0,1,1,0,0,0,1,1,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0],
[1,1,1,1,1,0,1,0,0,1,0,1,0,1,0,0,0,0,1,0,0,0,1,1,0,1,1,0,1,0],
[1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,1,1,1,1],
[1,1,1,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,0,1,0,0],
[1,0,1,0,1,1,0,0,0,0,1,1,0,0,1,1,1,0,1,0,1,0,1,1,0,0,0,0,1,1],
[0,0,1,1,0,1,0,1,1,1,0,1,0,0,0,0,0,1,1,0,0,1,0,1,1,0,1,0,0,1],
[0,1,0,0,1,0,1,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,0,1,0,1,0,0,0,1],
[0,1,0,1,1,1,1,0,1,0,0,1,1,1,0,1,0,0,0,1,0,1,1,0,0,1,0,0,1,0],
[1,1,0,0,0,0,0,1,1,0,1,0,1,1,1,1,1,0,1,0,0,1,1,0,0,0,0,0,1,0]]

# # Solving with the first grid
# ss = solve(ig2)
# st = time()
# seq = False
# time_limit = 2
# i = 1
# while not seq:
#     seq = rsf(ig2[:], ss[:], time_limit = time_limit, start_time = time(), prios = (2,1,3))
#     print('Time Limit reached '+str(i))
#     i += 1
# print(time()-st)
# print(seq)

# Solving with the "bonus grid"
ss = solve(ig3)
st = time()
seq = False
time_limit = 10
i = 1
while not seq:
    seq = rsf(ig3[:], ss[:], time_limit = time_limit, start_time = time(), prios = (2,1,3))
    print('Time Limit reached, restart '+str(i))
    i += 1
print(time()-st)
print(seq)


# This part was just to figure out which priorities for the pairings worked best
# stats = {p:0 for p in [(1,2,3),(1,3,2),(2,1,3),(2,3,1),(3,1,2),(3,2,1)]}
# for prios in [(1,2,3),(1,3,2),(2,1,3),(2,3,1),(3,1,2),(3,2,1)]:
#     for i in range(1000):
#         seq = rsf(ig2[:], ss[:], time_limit = time_limit, start_time = time(), prios = prios)
#         if seq:
#             stats[prios] += 1
#       
# print('Solve statistics, time limit = '+str(time_limit))      
# print(stats)