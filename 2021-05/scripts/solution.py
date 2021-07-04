from docplex.mp.model import Model
import math
from sympy import factorint

def primefactors(n):
    res = set()
    for i in factorint(n):
        res.add(i)
    return res

def isprime(n):
    pfs = primefactors(n)
    return len(pfs) == 1 and list(pfs)[0] == n

T = 18
ts = range(T)
max_mk = 340 # we are just assuming this is big enough
possible_mks = list(range(2,max_mk))
possible_mks = [i for i in possible_mks if max(primefactors(i)) <= 5] # Taking advantage of the fact that we know that there is a solution where each m_k has no other primefactors than 2, 3 and 5
max_ak = 340 # we are just assuming this is big enough
possible_aks = list(range(1,max_ak))
max_pk = 5000 # we are just assuming this is big enough
possible_pks = [i for i in range(2,max_pk) if isprime(i)]
f = [0,1]
for i in range(100000):
    f.append(f[-2]+f[-1])

model = Model()

print('Set up variables')
pma = dict()
for m in possible_mks:
    fm = f[m]
    pfs = primefactors(fm)
    for a in possible_aks:
        if a <= m:
            for p in possible_pks:
                if p > fm:
                    break
                if p in pfs:
                    pma[(p,m,a)] = model.binary_var()
          
# Set size
print('Set size constraint')
model.add(model.sum(pma.values()) == T)
    
# 1. 1 <= a_k <= m_k
# part of variable definition
        
# 2. For every natural number n, we have that for some k, n is equivalent to  a_k modulo  m_k (i.e.  m_k divides  n-a_k ).
print('Adding constraint 2')
#for n in list(range(0,60))+list(range(110,125))+list(range(455,470)):
for n in range(0,2000):
    print(n)
    possible_options = []
    for p,m,a in pma.keys():
        if (n-a)/m == int((n-a)/m):
            possible_options.append(pma[(p,m,a)])
    model.add(model.sum(possible_options) >= 1)

# 3. p_k is a prime divisor of the Fibonacci number  F_{m_k}
# part of variable definition

# 4. All the  p_k are distinct (the  m_k and  a_k can be non-distinct)
print('Adding constraint 4')
for p2 in possible_pks:
    model.add(model.sum(pma[(p,m,a)] for p,m,a in pma.keys() if p == p2) <= 1)
    
model.solve(log_output = True)
model.export_as_lp('model.lp')

answers = []
for p,m,a in pma.keys():
    if pma[(p,m,a)].solution_value > 0.5:
        answers.append((p,m,a))
print(answers)

unsatisfied = []
for n in range(1000000):
    good = False
    for t in ts:
        if (n-answers[t][2])/answers[t][1] == int((n-answers[t][2])/answers[t][1]):
            good = True
            #print('%i-%i can be divided by %i'%(n, answers[t][2] , answers[t][1]))
            break
    if not good:
        #print('%i doesnt satisfy condition 2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'%n)
        unsatisfied.append(n)
print(unsatisfied)
print('Condition 2 unsatisfied for %i numbers'%len(unsatisfied))