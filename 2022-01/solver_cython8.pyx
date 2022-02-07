from time import time

cdef float start_time
cdef int minscore, maxscore, i1, i3, i4, i5, i6, i7, i8, score, counter
cdef list mincircle, maxcircle

def read_distinct_primes(path):
    primes = []
    with open(path, 'r') as f:
        for l in f.readlines():
            distinct = True
            for i in range(10):
                if l.count(str(i)) > 1:
                    distinct = False
                    break
            if distinct:
                primes.append(l)
    return primes

cdef calculate_score(circle, primes):
    cdef sc, move
    cdef int counter, score, temps, ii, i, ij, j
    cdef str p
    sc = {(i,j): min(abs(ij-ii), 8-ij+ii, 8-ii+ij) for ii,i in enumerate(circle) for ij,j in enumerate(circle)}
    counter = 0
    score = 0
    for p in primes:
        temps = 0
        for i in range(5):
            move = (int(p[i]), int(p[i+1]))
            if move in sc:
                temps += sc[move]
            else:
                temps = -1
                break
        if temps > 0:
            score += temps
            counter += 1
    return counter, score
    

primes = read_distinct_primes('primes6.txt')

start_time = time()
minscore = 10000000
mincircle = []
maxscore = 0
maxcircle = []
for i1 in [0,1,2]:
    qq = {i for i in range(i1)}
    for i2 in {0,1,2,3,4,5,6,7,8,9}-{i1}-qq:
        for i3 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2}-qq:
            for i4 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2,i3}-qq:
                for i5 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2,i3,i4}-qq:
                    for i6 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2,i3,i4,i5}-qq:
                        for i7 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2,i3,i4,i5,i6}-qq:
                            for i8 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2,i3,i4,i5,i6,i7}-qq:
                                circle = [i1,i2,i3,i4,i5,i6,i7,i8]
                                counter, score = calculate_score(circle, primes)
                                if score < minscore:
                                    minscore = score
                                    mincircle = circle
                                    print('New min circle: '+str(circle)+' ; score: '+str(score) +' ('+str(counter)+')')
                                if score > maxscore:
                                    maxscore = score
                                    maxcircle = circle
                                    print('New max circle: '+str(circle)+' ; score: '+str(score) +' ('+str(counter)+')')
           
print()     
print('Min circle:')                
print(mincircle)
print('Max circle:')                
print(maxcircle)
print()
print('Time used (seconds): '+str(time()-start_time))