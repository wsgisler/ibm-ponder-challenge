from time import time

sol = [(2, 3, 1), (3, 4, 3), (5, 5, 4), (7, 8, 5), (17, 9, 6), (11, 10, 2), (61, 15, 8), (47, 16, 9), (19, 18, 18), (41, 20, 20), (23, 24, 17), (31, 30, 26), (2161, 40, 30), (1103, 48, 33), (541, 90, 48), (181, 90, 66), (2521, 120, 50), (241, 120, 90)]

st = time()
unsatisfied = []
rrr = 1000000000
rr =  2000000
for n in range(rrr):
    if n%rr == 0:
        print(str(n/rrr*100)+"% done")
    good = False
    for t in range(len(sol)):
        if (n-sol[t][2])/sol[t][1] == int((n-sol[t][2])/sol[t][1]):
            good = True
            #print('%i-%i can be divided by %i'%(n, answers[t][2] , answers[t][1]))
            break
    if not good:
        #print('%i doesnt satisfy condition 2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'%n)
        unsatisfied.append(n)
print(unsatisfied)
print('Condition 2 unsatisfied for %i numbers'%len(unsatisfied))
print('Took %f seconds'%(time()-st))