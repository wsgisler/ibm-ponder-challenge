# I had fun writing a local search solver for this challenge
# Basically, we start with 4 random experiments and determine a score for this experiment set
# The score determines how far we are from a unique solution
# In each iteration we exchange one experiment and we always try to make an exchange that lowers the score
# If the score couldn't be lowered for a while, we will randomize the current solution a bit and will try again

from itertools import combinations
import random

def outcome(experiments,fakeCoins):
	out = []
	for e in experiments:
		w1 = 0
		w2 = 0
		for c in e[0]:
			if c in fakeCoins:
				w1 -= 1
		for c in e[1]:
			if c in fakeCoins:
				w2 -= 1
		if w1 == w2:
			out += [0]
		elif w1 < w2:
			out += [2]
		else:
			out += [1]
	return out

def unique(experiments): #if this is 0 we have reached the goal
	outs = set()
	for c1 in 'abcdefghijk':
		for c2 in {c3 for c3 in 'abcdefghijk' if c3>c1}:
				out = outcome(experiments,c1+c2)
				# print out
				outs.add(str(out[0])+str(out[1])+str(out[2])+str(out[3]))
	return 55-len(outs)

def allExperiments(expSize):
	exps = []
	for c1 in combinations({'a','b','c','d','e','f','g','h','i','j','k'},expSize):
		for c2 in combinations({'a','b','c','d','e','f','g','h','i','j','k'}-set(c1),expSize):
			out = []
			for f1 in 'abcdefghijk':
				for f2 in {c3 for c3 in 'abcdefghijk' if c3>f1}:
					out += outcome((c1,c2),f1+f2)
			name = ''
			for s in c1:
				name += s
			name += '-'
			for s in c2:
				name += s
			#print (name,c1,c2,out)
			exps += [(name,c1,c2,out)]
	return exps


experimentsPool = allExperiments(4)+allExperiments(3)+allExperiments(2)+allExperiments(5)
startSol = [('abcd','efgh'),('abef','cdgh'),('aceg','bdfh'),('ijka','bcde')]
best = unique(startSol)
noImprove = False
while(best > 0):
	noImprove = True
	for e in experimentsPool:
		newSol = [(e[1],e[2]),startSol[1],startSol[2],startSol[3]]
		newScore = unique(newSol)
		if newScore < best:
			best = newScore
			startSol = newSol
			print best
			print startSol
			noImprove = False
		newSol = [startSol[0],(e[1],e[2]),startSol[2],startSol[3]]
		newScore = unique(newSol)
		if newScore < best:
			best = newScore
			startSol = newSol
			print best
			print startSol
			noImprove = False
		newSol = [startSol[0],startSol[1],(e[1],e[2]),startSol[3]]
		newScore = unique(newSol)
		if newScore < best:
			best = newScore
			startSol = newSol
			print best
			print startSol
			noImprove = False
		newSol = [startSol[0],startSol[1],startSol[2],(e[1],e[2])]
		newScore = unique(newSol)
		if newScore < best:
			best = newScore
			startSol = newSol
			print best
			print startSol
			noImprove = False
	if noImprove:
		e = random.choice(experimentsPool)
		e2 = random.choice(experimentsPool)
		startSol = [startSol[0],startSol[1],(e2[1],e2[2]),(e[1],e[2])]
		best = unique(startSol)
print startSol

# Just test a solution that is unique
# print unique([('acbei','dgfhk'),('bgk','efh'),('cbh','eik'),('agf','cdi')])
