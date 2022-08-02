from docplex.cp.model import CpoModel

def solve(n,m,start):
    model = CpoModel()
    x = {(i,j): 0 for i in range(n) for j in range(m)}
    giving = {(i,j): model.binary_var(name = 'giving_'+str(i)+'_'+str(j)) for i in range(n) for j in range(m)}
    receiving = {(i,j): model.binary_var(name = 'receiving_'+str(i)+'_'+str(j)) for i in range(n) for j in range(m)}

    # start configuration
    bigm = sum(start)
    for i in range(n):
        x[(i,0)] = start[i]
    
    # calculate x values for following iterations
    for j in range(1,m):
        given = model.sum(x[(ii,j-1)]*receiving[(ii,j)] for ii in range(n))
        for i in range(n):
            x[(i,j)] = x[(i,j-1)] + x[(i,j-1)]*receiving[(i,j)] - given*giving[(i,j)]
            model.add(x[(i,j)] >= 0)

    # At each iteration, one cell gives and one cell receives
    for j in range(1,m):
        model.add(model.sum(giving[(i,j)] for i in range(n)) == 1)
        model.add(model.sum(receiving[(i,j)] for i in range(n)) == 1)
        for i in range(n):
            model.add(giving[(i,j)] + receiving[(i,j)] <= 1)
            
    
    model.minimize(model.min(x[(nn,m-1)] for nn in range(n)))

    sol = model.solve(log_output = True, TimeLimit = 2000, Workers = 4)
    
    # Prepare solution values
    xx = {(i,j): 0 for i in range(n) for j in range(m)}
    bigm = sum(start)
    for i in range(n):
        xx[(i,0)] = start[i]
    for j in range(1,m):
        given = sum(sol[receiving[(ii,j)]]*xx[(ii,j-1)] for ii in range(n))
        for i in range(n):
            if sol[receiving[(i,j)]] == 1:
                xx[(i,j)] = xx[(i,j-1)]*2
            elif sol[giving[(i,j)]] == 1:
                xx[(i,j)] = xx[(i,j-1)]-given
            else:
                xx[(i,j)] = xx[(i,j-1)]
            #xx[(i,j)] = xx[(i,j-1)] + xx[(i,j-1)]*sol[receiving[(i,j)]] - sum(xx[(ii,j-1)]*sol[receiving[(ii,j-1)]] for ii in range(n))*sol[giving[(i,j)]]

    solution_string = ''
    for j in range(m):
        print(', '.join([str(int(xx[(i,j)])) for i in range(n)]))
        solution_string += '('+(', '.join(sorted([str(int(xx[(i,j)])) for i in range(n)])))+'), '

    print(solution_string)
   
    return min([int(xx[(i,j)]) for i in range(n)]) == 0

start = (855661, 1395050, 1402703, 1575981, 2956165, 4346904, 5516627, 5693538, 6096226, 7359806)
n = len(start)
last_working = (0,0)
for m in [13]:
    print('Trying m: '+str(m))
    solve(n,m,start)