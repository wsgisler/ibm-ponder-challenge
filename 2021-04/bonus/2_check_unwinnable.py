# This takes a sequence of eliminated numbers and then returns a q that gives this sequence
# Test sequences: 

# q = 62981
# removes: [1, 16, 14, 9, 15, 8, 2]
# should leave: [3, 4, 5, 6, 7, 10, 11, 12, 13, 17, 18, 19, 20]

# q = 39283
# removes: [3, 13, 20, 15, 18, 14, 11]
# should leave: [12, 16, 17, 19, 1, 2, 4, 5, 6, 7, 8, 9, 10]

from itertools import combinations, permutations
from time import time
from docplex.mp.model import Model
from math import gcd

def one_step(numbers, q):
    x = q%len(numbers)
    x = x-1 if x > 0 else len(numbers)-1
    new_numbers = numbers[x+1:] + numbers[:x]
    return new_numbers
    
def simulate(numbers, q, steps, output = True):
    for i in range(steps):
        numbers = one_step(numbers, q)
        if output:
            print(numbers)
    return sorted(numbers)
    
def reconstruct(numbers, seq):
    m = Model()
    vv = m.integer_var()
    a = len(numbers)
    b = numbers.index(seq[0])+1
    numbers = one_step(numbers, b)
    coefficients = []
    for n in seq[1:]:
        i = numbers.index(n)
        d = 0 
        e = 0
        for qq in range(1,100):
            qqq = (a*qq+b-(i+1))/len(numbers)
            if qqq == int(qqq):
                if d:
                    e = qq
                    break
                else:
                    d = qq
        if not d:
            return None
        v = m.integer_var()
        m.add(d+v*(e-d) == vv)
        v2 = m.integer_var()
        m.add(v2*len(numbers) + i + 1 == vv*a+b)
        if coefficients: # We are applying the euclydian algorithm here to check if overlaps are at all possible: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm , https://math.stackexchange.com/questions/1656120/formula-to-find-the-first-intersection-of-two-arithmetic-progressions
            for cs in coefficients:
                divisor = gcd(cs[0], len(numbers))
                if (i+1-cs[1])/divisor != int((i+1-cs[1])/divisor):
                    return None
        coefficients.append((len(numbers), i+1))
        numbers = one_step(numbers, i+1)
    m.minimize(vv)
    solution = m.solve(log_output = True)
    if solution:
        return vv.solution_value*a+b
    else:
        return None
        
def check_unwinnable(numbers, uwnumbers):
    to_eliminate = [n for n in numbers if n not in uwnumbers]
    count = 0
    for perm in permutations(to_eliminate):
        print(count)
        count += 1
        tt = reconstruct(numbers, perm)
        if tt:
            print('This set is winnable with the following q: '+str(tt))
            return False
    print('This set is unwinnable')
    return True    


n = 28
numbers = [i+1 for i in range(n)]
uwnumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 21, 22, 23, 24, 25, 26, 27, 28] # unwinnable
a = check_unwinnable(numbers, uwnumbers)