from time import time

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

def calculate_score(circle, primes):
    sc = {(i,j): min(abs(ij-ii), 7-ij+ii, 7-ii+ij) for ii,i in enumerate(circle) for ij,j in enumerate(circle)}
    counter = 0
    score = 0
    for p in primes:
        temps = 0
        for i in range(4):
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
    
#circle = [4, 7, 3, 6, 2, 0, 1]

primes = read_distinct_primes('primes.txt')

start_time = time()
minscore = 10000000
mincircle = None
maxscore = 0
maxcircle = None
for i1 in [0,1,2,3]:
    qq = {i for i in range(i1)}
    for i2 in {0,1,2,3,4,5,6,7,8,9}-{i1}-qq:
        for i3 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2}-qq:
            for i4 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2,i3}-qq:
                for i5 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2,i3,i4}-qq:
                    for i6 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2,i3,i4,i5}-qq:
                        for i7 in {0,1,2,3,4,5,6,7,8,9}-{i1,i2,i3,i4,i5,i6}-qq:
                            circle = [i1,i2,i3,i4,i5,i6,i7]
                            counter, score = calculate_score(circle, primes)
                            if score < minscore:
                                minscore = score
                                mincircle = circle
                                print('New min circle: '+str(circle)+' ; score: '+str(score))
                            if score > maxscore:
                                maxscore = score
                                maxcircle = circle
                                print('New max circle: '+str(circle)+' ; score: '+str(score))
           
print()     
print('Min circle:')                
print(mincircle)
print('Max circle:')                
print(mincircle)
print()
print('Time used (seconds): '+str(time()-start_time))