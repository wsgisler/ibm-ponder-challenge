import sys
from pulp import *

def hamming(s1,s2):
	return sum(c1 != c2 for c1, c2 in zip(s1, s2))

p = LpProblem("ibmPonder",LpMaximize)

num_toggles = 6;
settings = []
neighbors = []
answers = ['A','E','I','O','U']

for i in range(2**num_toggles):
	number = "{0:{fill}6b}".format(i, fill='0')
	settings += [number]
	neighbors += [list()]

for s1 in range(len(settings)):
	for s2 in range(len(settings)):
		# print settings[s1]
		# print settings[s2]
		# print hamming(settings[s1],settings[s2])
		if hamming(settings[s1],settings[s2]) == 1:
			neighbors[s1] += [s2]
			
x = LpVariable.dicts('settingscode',(range(len(settings)),answers),0,1,LpInteger)
for s1 in range(len(settings)):
	p += lpSum([x[s1][a] for a in answers]) == 1
	for a in answers:
		p += x[s1][a]+lpSum([x[s2][a] for s2 in neighbors[s1]]) >= 1

for s in range(32):
	for a in answers:
		p += x[s][a] == x[64-s-1][a]

p.solve(CPLEX())

for i in range(len(settings)):
	for a in answers:
		if value(x[i][a]) > 0.9:
			print a

"""
# Additional output to verify solution, not needed

for i in range(len(settings)):
	s = ""
	for n in neighbors[i]:
		s += settings[n]+","
	print s

for a in answers:
	count = 0
	print a
	for i in range(len(settings)):
		if value(x[i][a]) > 0.9:
			count+=1
	print count
"""
