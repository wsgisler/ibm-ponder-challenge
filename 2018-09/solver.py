"""

IBM Ponder September 2018 Challenge
Walter Sebastian Gisler
Maybe an unusual approach, but I like simulations.

It works as follows:

- we randomly generate a high number of different "person selections"
- each "person selection" has 26 people. each persons name in the selection starts with a different letter (a-z)
- in each "person selection" there is a certain likelihood for each person to be a man or a woman
- this likelihood is also determined randomly for each person selections, so we end up with selections 
  with no women, 10% women, 50% women, 100% women and everything in between
- We then read a list of three letter words (with three unique letters) from a dictionary file
- amongst these words, we try to find the smallest subset of words that guarantee that for each "person selection"
  there is at least one word that would form a mono gender team.
- For this selection process, I have used a MIP, which works extremely well

On the choice of num_tests:
- The lower this value is, the higher the chance that we find a wrong solution
- The higher it is, the more difficult it becomes to solve the MIP
- values above 500 have consistently worked for this

"""

from pulp import *
from itertools import combinations
import random

def test_word(sample,word):
    win = True
    let = ''
    for l in word:
        if let != '' and sample[l] != let:
            win = False
        let = sample[l]
    return win    

p = LpProblem('ponder',LpMinimize)
words = list()

with open('words.txt','r') as word_file:
    for line in word_file:
    	wo = {l for l in line.replace('\n','')}
    	if len(wo) == 3:
            words.append(line.replace('\n',''))
        
#generate random choices of w/m assignments to letters
num_tests = 3000
letters = 'abcdefghijklmnopqrstuvwxyz'
rr = [random.random() for test in range(num_tests)] # probability of a 0 for each test set
tests = [{l:0 if random.random() > rr[test] else 1 for l in letters} for test in range(num_tests)]

choice = LpVariable.dicts("chooseWord",words,0,1,LpInteger)

win = [{w:1 if test_word(tests[test],w) else 0 for w in words} for test in range(num_tests)]

#For every test sample, one of the chosen words needs to be a win
for test in range(num_tests):
	p += lpSum([choice[w]*win[test][w] for w in words]) >= 1, 'testSample'+str(test)

p.objective = lpSum([choice[w] for w in words])

p.solve(CPLEX_PY())

for w in words:
    if value(choice[w]) > 0.5:
        print w
