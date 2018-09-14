"""
IBM Ponder July 2018
Walter Sebastian Gisler
Finally a solution that doesn't require a MIP. 
This is clearly all about representing the data in the right way. And, I think it can be done in an even more efficient manner.
Problem description: https://www.research.ibm.com/haifa/ponderthis/challenges/July2018.html
"""

s = range(700)
combs = {}
identifierCounter = {}
identifier2Comb = {}
obscureIdent = set()
for s1 in s:
	for s2 in [ss for ss in s if ss>s1]:
		for s3 in [ss for ss in s if ss>s2]:
			combs[(s1,s2,s3)] = (s1*s2*s3,s1+s2+s3)
			if (s1*s2*s3,s1+s2+s3) in identifierCounter:
				identifierCounter[(s1*s2*s3,s1+s2+s3)] += 1
				identifier2Comb[(s1*s2*s3,s1+s2+s3)] += [(s1,s2,s3)]
				obscureIdent.add((s1,s2,s3))
			else:
				identifierCounter[(s1*s2*s3,s1+s2+s3)] = 1
				identifier2Comb[(s1*s2*s3,s1+s2+s3)] = [(s1,s2,s3)]
print len(obscureIdent)
				
				
for ident in obscureIdent:
	if (ident[0]+1,ident[1]+1,ident[2]+1) in obscureIdent and (ident[0]+2,ident[1]+2,ident[2]+2) in obscureIdent and (ident[0]+3,ident[1]+3,ident[2]+3) in obscureIdent  and (ident[0]+4,ident[1]+4,ident[2]+4) in obscureIdent  and (ident[0]+5,ident[1]+3,ident[2]+5) in obscureIdent:
		print ident
		print identifier2Comb[(ident[0]*ident[1]*ident[2],ident[0]+ident[1]+ident[2])]
		print identifier2Comb[((ident[0]+1)*(ident[1]+1)*(ident[2]+1),ident[0]+ident[1]+ident[2]+3)]
		print identifier2Comb[((ident[0]+2)*(ident[1]+2)*(ident[2]+2),ident[0]+ident[1]+ident[2]+6)]
		print identifier2Comb[((ident[0]+3)*(ident[1]+3)*(ident[2]+3),ident[0]+ident[1]+ident[2]+9)]
		print identifier2Comb[((ident[0]+4)*(ident[1]+4)*(ident[2]+4),ident[0]+ident[1]+ident[2]+12)]
		print identifier2Comb[((ident[0]+5)*(ident[1]+5)*(ident[2]+5),ident[0]+ident[1]+ident[2]+15)]
		print ""
