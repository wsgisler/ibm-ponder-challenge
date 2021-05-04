from itertools import combinations
from time import time

def one_step(numbers, q):
    x = q%len(numbers)
    x = x-1 if x > 0 else len(numbers)-1
    new_numbers = numbers[x+1:] + numbers[:x]
    removed = numbers[x]
    return new_numbers, removed
    
def simulate(numbers, q, steps, output = True):
    rem = []
    for i in range(steps):
        numbers, removed = one_step(numbers, q)
        rem.append(removed)
        if output:
            print(numbers)
    print(rem)
    print(numbers)
    return sorted(numbers)

numberrange = 15000000000
n = 28 # up to 17: no unwinnable sets (numberrange of 100000), 18: numrange 500000, 19: 700000
steps = 8
numbers = [i+1 for i in range(n)]

combdict= dict()
for c in combinations(numbers, n-steps):
    combdict[tuple(sorted(c))] = 0
        
st = time()
for i in range(1,numberrange):
    if i%int(numberrange/200) == 0:
        perc = i/int(numberrange/100)
        passed = time()-st
        remain = passed/perc*(100-perc)
        print(str(perc)+'% done - '+str(round(passed, 2))+' seconds passed. '+str(round(remain,2))+' seconds remaining')
    print(i)
    sss = simulate(numbers, i, steps, False)
    sss = tuple(sss)
    combdict[sss] += 1
    #(sss)
    
print('Unwinnable:')
print(len([1 for c in combdict.values() if c == 0]))
for c in combdict:
    if combdict[c] == 0:
        print(c)