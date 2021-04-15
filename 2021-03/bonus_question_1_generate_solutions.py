from docplex.mp.model import Model
    
rows = [0,1,2,3,4]
cols = [0,1,2,3,4]

m = Model('Ponder')

x = {(r,c): m.binary_var() for r in rows for c in cols} # x = explore

solutions = []

# Constraints
for r in rows:
    for c in cols:
        for cc in [-1,0,1]:
            if r-1 in list(rows) and c+cc in list(cols):
                m.add(x[(r,c)] <= x[(r-1,c+cc)])

solution = True
while solution:
    m.minimize(m.sum(x[(r,c)] for r in rows for c in cols))
    solution = m.solve(log_output = True)
    if solution:
        m.add(m.sum(x[(r,c)] for r in rows for c in cols if x[(r,c)].solution_value < 0.5) >= 1) # exclude previous solution
        sol = []
        for r in rows:
            for c in cols:
                if x[(r,c)].solution_value > 0.5:
                    sol.append((r,c))
        solutions.append(sol)
            
print(solutions)
print(len(solutions))