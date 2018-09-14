# Maybe not the most efficient, but an unusual and fun solution that uses a MIP to verify whether a solution is unique
# We can speed this up significantly if we exclude solutions that use experiments with only one balloon (which is a good assumption)

import sys
from pulp import *
from itertools import combinations

def goodExperimentSet(testSet):
	p = LpProblem("ibmPonder",LpMaximize)
	
	colors = ['a','b','c','d','e','f','g','h','i']
	colorSet = [[colors[c-1] for c in test] for test in testSet]

	weight = LpVariable.dicts("weight",colors,1,9,LpInteger)
	heavier = LpVariable.dicts("heavier",(colors,colors),0,1,LpInteger)
	for t in colorSet:
		p += lpSum([weight[c] for c in t]) <= 9
	
	for c1 in colors:
		for c2 in colors:
			if c1 == c2:
				heavier[c1][c2] == 0
			else:
				p += heavier[c1][c2]*9-8 <= weight[c1]-weight[c2]
				p += heavier[c1][c2]+heavier[c2][c1] == 1

	#Add a constraint that forbids "a" to be 1 - MIP will become infeasible if the solution is unique with regard to 1
	p += weight['a'] >= 2
	
	p.solve(CPLEX(msg = 0))
	status = 0
	if p.status <= 0:
			status = 1
	return status == 1
	
def main():
	good = 0
	done = 0
	weights = 9;
	experiments = []
	colors = ['a','b','c','d','e','f','g','h','i']
	colexp = [] 

	for i in range(2**weights):
		number = "{0:{fill}9b}".format(i, fill='0')
		weight = sum([int(number[i])*(i+1) for i in range(9)])
		if weight <= 9.5 and number != "000000000":
			experiments += [[i+1 for i in range(9) if number[i] == "1"]]
			colexp += [[colors[i] for i in range(9) if number[i] == "1"]]

	testSets = combinations(experiments,4)
	f = open("results.txt","w")
	for ts in testSets:
		print done
		print good
		print ts
		ge = goodExperimentSet(ts)
		if ge:
			for e in ts:
				f.write(str(e)+"\n")
			f.write("-----------------------\n")
			f.flush()
			good+=1
		done+=1
		
main()
