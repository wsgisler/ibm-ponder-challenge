from docplex.mp.model import Model
from random import random

model = Model()

weapons = [0,1,2,3,4,5,6,7,8]
weapons = [0,1,2,3,4,5,6,7,8,9,10]
#weapons = [0,1,2,3,4]
num_automorphisms = 4

beats = {(w1,w2): model.binary_var() for w1 in weapons for w2 in weapons}

# Every weapon beats (n-1)/2 other weapons
for w1 in weapons:
    model.add(model.sum(beats[(w1,w2)] for w2 in weapons) == (len(weapons)-1)/2)
    model.add(beats[(w1,w1)] == 0) # can't beat itself

# If w1 beats w2, w2 can't beat w1
for w1 in weapons:
    for w2 in set(weapons)-{w1}:
        model.add(beats[(w1,w2)] + beats[(w2,w1)] <= 1)

permutations = {(a,w1,w2): model.binary_var() for a in range(num_automorphisms) for w1 in weapons for w2 in weapons}
for a in range(num_automorphisms):
    for w1 in weapons:
        model.add(model.sum(permutations[(a,w1,w2)] for w2 in weapons) == 1) # every weapon is matched to another weapon. Can be the same weapon
        model.add(model.sum(permutations[(a,w2,w1)] for w2 in weapons) == 1) # every weapon needs to be mapped to by another weapon. Can be the same weapon
        
# make sure that each automorphism is unique
for a1 in range(num_automorphisms):
    for a2 in set(range(num_automorphisms))-{a1}:
        difference = {(w1,w2): model.continuous_var(lb=0, ub=1) for w1 in weapons for w2 in weapons}
        for w1 in weapons:
            for w2 in weapons:
                model.add(difference[(w1,w2)] <= permutations[(a1,w1,w2)] + permutations[(a2,w1,w2)]) # If both are 0, there is no difference
                model.add(difference[(w1,w2)] <= 2 - permutations[(a1,w1,w2)] - permutations[(a2,w1,w2)]) # If both are 1, there is no difference
        model.add(model.sum(difference[(w1,w2)] for w1 in weapons for w2 in weapons) >= 1)
        
# an automorphism has to make at least one change
for a1 in range(num_automorphisms):
    model.add(model.sum(permutations[(a1, w1, w1)] for w1 in weapons) <= len(weapons)-1)
        
# the new rules that result from each automorphism need to stay identical to the original rules
for a1 in range(num_automorphisms):
    # mapping from beats to new_beats
    new_beats = {(w1,w2): model.binary_var() for w1 in weapons for w2 in weapons}
    for w1 in weapons:
        for w2 in weapons:
            for w3 in weapons:
                for w4 in weapons:
                    model.add(beats[(w1, w2)] + permutations[(a1, w1, w3)] + permutations[(a1, w2, w4)] - 2 <= new_beats[(w3, w4)])
    # Every weapon beats (n-1)/2 other weapons in the new set of rules after the mapping
    for w1 in weapons:
        model.add(model.sum(new_beats[(w1,w2)] for w2 in weapons) == (len(weapons)-1)/2)
        model.add(new_beats[(w1,w1)] == 0) # can't beat itself
    # If w1 beats w2, w2 can't beat w1
    for w1 in weapons:
        for w2 in set(weapons)-{w1}:
            model.add(new_beats[(w1,w2)] + new_beats[(w2,w1)] <= 1)
    # Identical set of rules
    for w1 in weapons:
        for w2 in weapons:
            model.add(beats[(w1,w2)] == new_beats[(w1,w2)])
            
# Remove symmetries by fixing the rules for the first weapon
for w1 in weapons:
    if w1 >= 1 and w1 <= (len(weapons)-1)/2:
        model.add(beats[(0,w1)] == 1)
            
# I used a random objective function to generate some random solutions without adding the automorphism constraint to see what percentage of solutions actually has multiple automorphisms
model.minimize(sum([random()*beats[(w1,w2)] for w1 in weapons for w2 in weapons]))
            
model.solve(log_output = True)

# Print set of rules

print('Rules:')
for w1 in weapons:
    stronger_than = []
    for w2 in weapons:
         if beats[(w1,w2)].solution_value > 0.5:
              stronger_than.append(str(w2))
    print('%i -> %s'%(w1, ', '.join(stronger_than)))
    
print('Rules: {')
for w1 in weapons:
    stronger_than = []
    for w2 in weapons:
         if beats[(w1,w2)].solution_value > 0.5:
              stronger_than.append(str(w2))
    print('%i: [%s],'%(w1, ', '.join(stronger_than)))
print('}')

# Print permutations:
for a in range(num_automorphisms):
    print('\nAutomorphism %i'%a)
    for w1 in weapons:
        for w2 in weapons:
            if permutations[(a,w1,w2)].solution_value > 0.5:
                 print('%i -> %i'%(w1,w2))
    