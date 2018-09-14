# Ok, this is clearly an overkill, I just liked the idea of solving this as a MIP

from pulp import *
from itertools import combinations
import random

t = LpProblem("June",LpMaximize)

xaxis = range(11)
yaxis = range(11)
figureL = ['L1','L2','L3','L4'] #L, L+90deg clockwise, ...
figureJ = ['J1','J2','J3','J4']

figureDef = {'L1':[(0,0),(0,1),(0,2),(1,2)], 
			 'L2':[(0,0),(1,0),(2,0),(0,1)], 
			 'L3':[(0,0),(1,0),(1,1),(1,2)],
			 'L4':[(2,0),(0,1),(1,1),(2,1)],
			 'J1':[(1,0),(1,1),(1,2),(0,2)],
			 'J2':[(0,0),(0,1),(1,1),(2,1)],
			 'J3':[(0,0),(1,0),(0,1),(0,2)],
			 'J4':[(0,0),(1,0),(2,0),(2,1)]}

outsideDef = {'L1':[(0,-1),(-1,0),(1,0),(-1,1),(1,1),(-1,2),(2,2),(0,3),(1,3)], 
			  'L2':[(0,-1),(1,-1),(2,-1),(-1,0),(3,0),(-1,1),(1,1),(2,1),(0,2)], 
			  'L3':[(0,-1),(1,-1),(-1,0),(2,0),(0,1),(2,1),(0,2),(2,2),(1,3)],
			  'L4':[(2,-1),(0,0),(1,0),(3,0),(-1,1),(3,1),(0,2),(1,2),(2,2)],
			  'J1':[(1,-1),(0,0),(2,0),(0,1),(2,1),(-1,2),(2,2),(0,3),(1,3)],
			  'J2':[(0,-1),(-1,0),(1,0),(2,0),(-1,1),(3,1),(0,2),(1,2),(2,2)],
			  'J3':[(1,-1),(2,-1),(0,0),(3,0),(0,1),(2,1),(0,2),(2,2),(1,3)],
			  'J4':[(0,-1),(1,-1),(2,-1),(-1,0),(3,0),(0,1),(1,1),(3,1),(2,2)]}

grid = LpVariable.dicts("x",(xaxis,yaxis),0,1,LpInteger)

topLeftFigureL = LpVariable.dicts("L",(xaxis,yaxis,figureL),0,1,LpInteger)
topLeftFigureJ = LpVariable.dicts("J",(xaxis,yaxis,figureJ),0,1,LpInteger)

#Use exactly 5 Ls
t += lpSum([topLeftFigureL[x][y][f] for x in xaxis for y in yaxis for f in figureL]) == 5

#Use exactly 5 Js
t += lpSum([topLeftFigureJ[x][y][f] for x in xaxis for y in yaxis for f in figureJ]) == 5

#The area of our shape has to be 5x4 = 20
t += lpSum([grid[x][y] for x in xaxis for y in yaxis]) == 20

for x in xaxis[-3:]:
	for y in yaxis:
		t += grid[x][y] == 0
		t += lpSum([topLeftFigureL[x][y][lpf] for lpf in figureL]) == 0
		t += lpSum([topLeftFigureJ[x][y][lpf] for lpf in figureJ]) == 0

for x in xaxis:
	for y in yaxis[-3:]:
		t += grid[x][y] == 0
		t += lpSum([topLeftFigureL[x][y][lpf] for lpf in figureL]) == 0
		t += lpSum([topLeftFigureJ[x][y][lpf] for lpf in figureJ]) == 0


"""#Color grid with FigureL
for x in xaxis[:-3]:
	for y in yaxis[:-3]:
		for fl in figureL:
			for x1,y1 in figureDef[fl]:
				t += topLeftFigureL[x][y][fl] <= grid[x+x1][y+y1]"""
				
#Color grid with FigureJ
for x in xaxis[:-3]:
	for y in yaxis[:-3]:
		for fj in figureJ:
			for x1,y1 in figureDef[fj]:
				t += topLeftFigureJ[x][y][fj] <= grid[x+x1][y+y1]
				
#Don't color the three rows around everything:
for x in xaxis:
	for y in yaxis:
		if  x<=2 or x>=max(xaxis)-2 or y<=2 or y>= max(yaxis)-2:
			t += grid[x][y] == 0
				
#If a grid cell is colored, there needs to be a FigureL somewhere
for x in xaxis[3:]:
	for y in yaxis[3:]:
		t += grid[x][y] <= lpSum([topLeftFigureL[x-x1][y-y1][fl] for fl in figureL for x1,y1 in figureDef[fl]])
		
#If a grid cell is colored, there needs to be a FigureJ somewhere
for x in xaxis[3:]:
	for y in yaxis[3:]:
		t += grid[x][y] <= lpSum([topLeftFigureJ[x-x1][y-y1][fj] for fj in figureJ for x1,y1 in figureDef[fj]])
		
#FigureL has to be one piece (=the figure has to have at least one connection with another figure)
for x in xaxis[3:-3]:
	for y in yaxis[3:-3]:
		for fl in figureL:
			t += topLeftFigureL[x][y][fl] <= lpSum([grid[x+x1][y+y1] for x1,y1 in outsideDef[fl]])
			
#FigureJ has to be one piece (=the figure has to have at least one connection with another figure)
for x in xaxis[3:-3]:
	for y in yaxis[3:-3]:
		for fj in figureJ:
			t += topLeftFigureJ[x][y][fj] <= lpSum([grid[x+x1][y+y1] for x1,y1 in outsideDef[fj]])
					
"""#No overlap FigureL
for x in xaxis[:-3]:
	for y in yaxis[:-3]:
		for fl in figureL:
			for x1,y1 in figureDef[fl]:
				t += 1-topLeftFigureL[x][y][fl] >= lpSum([topLeftFigureL[x+x1][y+y1][fl2] for fl2 in figureL])"""
				
#No overlap FigureJ
"""for x in xaxis[:-3]:
	for y in yaxis[:-3]:
		for fj in figureJ:
			for x1,y1 in figureDef[fj]:
				t += 1-topLeftFigureJ[x][y][fj] >= lpSum([topLeftFigureJ[x+x1][y+y1][fj2] for fj2 in figureJ])"""
				
#No 1-hole:
for x in xaxis[1:-1]:
	for y in yaxis[1:-1]:
		t += 1-grid[x][y]+grid[x-1][y]+grid[x+1][y]+grid[x][y-1]+grid[x][y+1] <= 4
		
#No 2-hole horizontal:
for x in xaxis[1:-2]:
	for y in yaxis[1:-1]:
		t += 1-grid[x][y]+1-grid[x+1][y]+grid[x-1][y]+grid[x+2][y]+grid[x][y-1]+grid[x][y+1]+grid[x+1][y-1]+grid[x+1][y+1] <= 7
		
#No 2-hole vertical:
for x in xaxis[1:-1]:
	for y in yaxis[1:-2]:
		t += 1-grid[x][y]+1-grid[x][y+1]+grid[x-1][y]+grid[x+1][y]+grid[x-1][y+1]+grid[x+1][y+1]+grid[x][y+2]+grid[x][y-1] <= 7

#No 3-hole horizontal:
for x in xaxis[1:-3]:
	for y in yaxis[1:-1]:
		t += 1-grid[x][y]+1-grid[x+1][y]+1-grid[x+2][y]+grid[x-1][y]+grid[x+3][y]+grid[x][y-1]+grid[x][y+1]+grid[x+1][y-1]+grid[x+1][y+1]+grid[x+2][y-1]+grid[x+2][y+1] <= 10
		
#No 3-hole vertical:
for x in xaxis[1:-1]:
	for y in yaxis[1:-3]:
		t += 1-grid[x][y]+1-grid[x][y+1]+1-grid[x][y+2]+grid[x-1][y]+grid[x+1][y]+grid[x-1][y+1]+grid[x+1][y+1]+grid[x-1][y+2]+grid[x+1][y+2]+grid[x][y+3]+grid[x][y-1] <= 10
		
for trynum in range(1000):
	t.solve(CPLEX_PY())

	f = open("Lsolution"+str(trynum)+".html","w")
	f.write('<b>L-Solution</b>')
	f.write("<html><table border=1>")
	lMap = {x:{y:0 for y in yaxis} for x in xaxis}
	counter = 0
	for y in yaxis:
		for x in xaxis:
			xx = ""
			if value(topLeftFigureL[x][y]['L1']) > 0.9:
				counter+=1
				for x1,y1 in figureDef['L1']:
					lMap[x+x1][y+y1] = counter
			if value(topLeftFigureL[x][y]['L2']) > 0.9:
				counter+=1
				for x1,y1 in figureDef['L2']:
					lMap[x+x1][y+y1] = counter
			if value(topLeftFigureL[x][y]['L3']) > 0.9:
				counter+=1
				for x1,y1 in figureDef['L3']:
					lMap[x+x1][y+y1] = counter
			if value(topLeftFigureL[x][y]['L4']) > 0.9:
				counter+=1
				for x1,y1 in figureDef['L4']:
					lMap[x+x1][y+y1] = counter
	for y in yaxis:
		f.write("<tr height='30px'>")
		for x in xaxis:
			xx = ""
			if value(topLeftFigureL[x][y]['L1']) > 0.9:
				xx = 'L1'
			if value(topLeftFigureL[x][y]['L2']) > 0.9:
				xx = 'L2'
			if value(topLeftFigureL[x][y]['L3']) > 0.9:
				xx = 'L3'
			if value(topLeftFigureL[x][y]['L4']) > 0.9:
				xx = 'L4'
			if value(grid[x][y]) > 0.9:
				color = {1:'red',2:'green',3:'blue',4:'pink',5:'orange'}
				xx = str(lMap[x][y])
				f.write("<td width='30px' bgcolor='"+color[lMap[x][y]]+"'>"+xx+"</td>")
			else:
				f.write("<td width='30px'>"+xx+"</td>")
		f.write("</tr>")
	f.write("</table></html>")

	f = open("Jsolution"+str(trynum)+".html","w")
	f.write('<b>J-Solution</b>')
	f.write("<html><table border=1>")
	jMap = {x:{y:0 for y in yaxis} for x in xaxis}
	counter = 0
	for y in yaxis:
		for x in xaxis:
			xx = ""
			if value(topLeftFigureJ[x][y]['J1']) > 0.9:
				counter+=1
				for x1,y1 in figureDef['J1']:
					jMap[x+x1][y+y1] = counter
			if value(topLeftFigureJ[x][y]['J2']) > 0.9:
				counter+=1
				for x1,y1 in figureDef['J2']:
					jMap[x+x1][y+y1] = counter
			if value(topLeftFigureJ[x][y]['J3']) > 0.9:
				counter+=1
				for x1,y1 in figureDef['J3']:
					jMap[x+x1][y+y1] = counter
			if value(topLeftFigureJ[x][y]['J4']) > 0.9:
				counter+=1
				for x1,y1 in figureDef['J4']:
					jMap[x+x1][y+y1] = counter
	for y in yaxis:
		f.write("<tr height='30px'>")
		for x in xaxis:
			xx = ""
			if value(topLeftFigureJ[x][y]['J1']) > 0.9:
				xx = 'J1'
			if value(topLeftFigureJ[x][y]['J2']) > 0.9:
				xx = 'J2'
			if value(topLeftFigureJ[x][y]['J3']) > 0.9:
				xx = 'J3'
			if value(topLeftFigureJ[x][y]['J4']) > 0.9:
				xx = 'J4'
			if value(grid[x][y]) > 0.9:
				color = {1:'red',2:'green',3:'blue',4:'pink',5:'orange'}
				xx = str(jMap[x][y])
				f.write("<td width='30px' bgcolor='"+color[jMap[x][y]]+"'>"+xx+"</td>")
			else:
				f.write("<td width='30px'>"+xx+"</td>")
		f.write("</tr>")
	f.write("</table></html>")
	
	for xa in range(-20,20):
		for ya in range(-20,20):
			t += lpSum([grid[xa+x][ya+y] for x in xaxis for y in yaxis if (value(grid[x][y]) > 0.9 and (xa+x in xaxis and ya+y in yaxis))]) <= 19
	#t += lpSum([1-grid[x][y] for x in xaxis for y in yaxis if value(grid[x][y]) > 0.9]) >= 1
