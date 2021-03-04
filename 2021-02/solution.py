from docplex.mp.model import Model
from random import randint, random

def number_trusted_neighbors(trusted_neighbors, cell):
    n = len(trusted_neighbors)-1
    tn = 0 # unvaccinated trusted neighbors
    c, r = cell
    if r < n and trusted_neighbors[c][r][0] == '1':
        tn += 1
    if c < n and trusted_neighbors[c][r][1] == '1':
        tn += 1
    if r > 1 and trusted_neighbors[c][r][2] == '1':
        tn += 1
    if c > 1 and trusted_neighbors[c][r][3] == '1':
        tn += 1
    return tn

def next_state(vaccinated, trusted_neighbors):
    new_vaccinated = vaccinated.copy()
    n = len(trusted_neighbors)-1
    for c in range(1,n+1):
        for r in range(1,n+1):
            utn = 0 # unvaccinated trusted neighbors
            if r < n and trusted_neighbors[c][r][0] == '1' and ((c,r+1) not in vaccinated):
                utn += 1
            if c < n and trusted_neighbors[c][r][1] == '1' and ((c+1,r) not in vaccinated):
                utn += 1
            if r > 1 and trusted_neighbors[c][r][2] == '1' and ((c,r-1) not in vaccinated):
                utn += 1
            if c > 1 and trusted_neighbors[c][r][3] == '1' and ((c-1,r) not in vaccinated):
                utn += 1
            if utn == 0: # all trusted neighbors are vaccinated
                new_vaccinated.add((c,r))
    return new_vaccinated
     
def read_hexgrid(hexgrid):
    """
    Reads a hexgrid and returns a 2d array where the first index represents the column (seen from the bottom left corner, starting with 1)
    and the second index represents the row (seen from the bottom, starting with 1). For a n*n hexgrid, this returns a (n+1)*(n+1) grid. The 0 indexes are empty (None)
    """
    h2b = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101', '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'a':'1010', 'b':'1011', 'c':'1100', 'd':'1101', 'e':'1110', 'f':'1111'}
    n = len(hexgrid)
    grid = [[None for i in range(n+1)] for j in range(n+1)]
    for r in range(n):
        for c in range(n):
            grid[c+1][r+1] = h2b[hexgrid[n-r-1][c]]
    return grid
    
def mip_solver(trusted_neighbors, max_timesteps):
    m = Model()
    timesteps = list(range(max_timesteps))
    n = len(trusted_neighbors)-1
    x = {(c,r): m.binary_var() for c in range(1,n+1) for r in range(1,n+1)} # who needs to be vaccinated initially
    vaccinated = {(c,r,t): m.binary_var() for c in range(1,n+1) for r in range(1,n+1) for t in timesteps} # who is vaccinated after t timesteps
    for c in range(1,n+1):
        for r in range(1,n+1):
            vaccinated[(c,r,-1)] = x[(c,r)] # Just a stupid trick to make it easier to access x. Theoretically we could have done without x completely, but this doesn't add many lines but makes it more readable
    # Describe the vaccination dynamics
    for t in timesteps:
        for c in range(1,n+1):
            for r in range(1,n+1):
                tn = number_trusted_neighbors(trusted_neighbors, (c,r))
                if tn == 0:
                    m.add(vaccinated[(c,r,t)] == 1) # if a cell has no trusted neighbors, it will self vaccinate
                else:
                    vn = 0 # vaccinated neighbors
                    if r < n and trusted_neighbors[c][r][0] == '1':
                        vn += vaccinated[(c,r+1,t-1)]
                    if c < n and trusted_neighbors[c][r][1] == '1':
                        vn += vaccinated[(c+1,r,t-1)]
                    if r > 1 and trusted_neighbors[c][r][2] == '1':
                        vn += vaccinated[(c,r-1,t-1)]
                    if c > 1 and trusted_neighbors[c][r][3] == '1':
                        vn += vaccinated[(c-1,r,t-1)]
                    m.add(vaccinated[(c,r,t)] <= vn/tn + vaccinated[(c,r,t-1)]) # if none of the neighbors is vaccinated, then we don't vaccinate
                    m.add(vaccinated[(c,r,t)] >= 1+vn-tn) # this forces the cell to be vaccinated if all trusted neighbors are vaccinated
                    m.add(vaccinated[(c,r,t)] >= vaccinated[(c,r,t-1)]) # if the cell is vaccinated in the previous step it will also be vaccinated now
    # Make sure that at the end, everyone is vaccinated
    for c in range(1,n+1):
        for r in range(1,n+1):
            m.add(vaccinated[(c,r,timesteps[-1])] == 1)
    # Minimize the number of cells that have to be vaccinated initially
    m.minimize(m.sum(x[(c,r)] for c in range(1,n+1) for r in range(1,n+1)))
    m.solve(log_output = True)
    result = set()
    # for t in timesteps:
#         state = set()
#         for c in range(1,n+1):
#             for r in range(1,n+1):
#                 if vaccinated[(c,r,t)].solution_value > 0.5:
#                     state.add((c,r))
#         print(t)
#         print_state(state,n)
    
    for c in range(1,n+1):
        for r in range(1,n+1):
            if x[(c,r)].solution_value > 0.5:
                result.add((c,r))
    return result
    
def print_state(vaccinated, n):
    for r in range(n,0,-1):
        line = ''
        for c in range(1,n+1):
            line += '1' if (c,r) in vaccinated else '0'
        print(line)
    
def main_example():
    grid = read_hexgrid(['381','79c','26c'])
    print(grid)

    solution = mip_solver(grid, 5)
    print(solution)

    # Simulate a situation
    s = {(2,2)}#set() #{(1,2)} # convincing (1,2) to self-vaccinate will start a chain reaction
    for i in range(10): # 10 timesteps
        print()
        print_state(s, 3)
        s = next_state(s, grid)
        
def main_real():
    grid = read_hexgrid(['0a8301b11b01', '1bda41b24d78', '37c09e8d5998',
                         '60473283d3b8', '13279043d9bc', '371bf4c021c1',
                         '1d122e800ee1', '5bc967265d88', '5f1998f5915d',
                         '628dff094034', '39effbe6ecc8', '2c440c20e0a0'])
    print(grid)
    
    timesteps = 8
    
    solution = mip_solver(grid, timesteps)
    print(solution)

    # Simulate a situation
    s = solution
    for i in range(timesteps+1): # 10 timesteps
        print()
        print_state(s, 12)
        s = next_state(s, grid)
        
def bonus_question():
    for i in range(100):
        dec2hex = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'a', 11:'b', 12:'c', 13:'d', 14:'e', 15:'f'}
        hg = [[dec2hex[randint(0,15)] for j in range(12)] for i in range(12)]
        grid = read_hexgrid(hg)
        
        timesteps = 50
    
        solution = len(mip_solver(grid, timesteps))
        print(solution)
        if solution == 42:
            for line in hg:
                print(''.join(line))
            break
            
def verify_bq():
    hg = ['72bef53c26ef','3d24d23fbeb9','5b127d34b430',
          'c367056a0c5a','00ecc2c9e8da','33bf9c3a4cb2',
          '52739b1ed49b','3628653bf1a9','45582428cfef',
          'a4dc9e06334d','6b911c600c49','817756a990c2']
    grid = read_hexgrid(hg)
    print(grid)
    
    timesteps = 160
    
    solution = mip_solver(grid, timesteps)
    print(solution)

    # Simulate a situation
    s = solution
    for i in range(timesteps+1): # 10 timesteps
        print()
        print_state(s, 12)
        s = next_state(s, grid)
        
def verify_bq_2():
    hg = ['72bef53c26ef','3d24d23fbeb9','5b127d34b430',
          'c367056a0c5a','00ecc2c9e8da','33bf9c3a4cb2',
          '52739b1ed49b','3628653bf1a9','45582428cfef',
          'a4dc9e06334d','6b911c600c49','817756a990c2']
    grid = read_hexgrid(hg)
    
    timesteps = 40
    
    solution = {(c,r) for c in range(1,13) for r in range(1,13) if random() > 0.1}

    # Simulate a situation
    s = solution
    for i in range(timesteps+1): # 10 timesteps
        print()
        print_state(s, 12)
        s = next_state(s, grid)
    print(len(solution))
            
#main_real()
#bonus_question()
#verify_bq()
verify_bq_2()