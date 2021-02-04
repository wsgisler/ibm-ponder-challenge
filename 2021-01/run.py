from time import time

def perform_step(grid, p, d): # grid is a NxN array, p is the current position, d is the current direction (direction: 0 = up, 1 = right, 2 = down, 3 = left)
    p0 = p[0]
    p1 = p[1]
    # vaccinate and determine new direction
    if grid[p0][p1] == 0: # vaccinate, then turn 90 degrees clockwise
        grid[p0][p1] = 1
        d += 1
        if d == 4:
            d = 0
    elif grid[p0][p1] == 1: # vaccinate, then turn 90 degrees counter-clockwise
        grid[p0][p1] = 2
        d -= 1
        if d == -1:
            d = 3
    elif grid[p0][p1] == 2: # do nothing, keep direction
        d = d
    elif grid[p0][p1] == 3: # 3 = B; if there is a bot, turn 90 degrees counter-clockwise, but don't change the cells status
        d -= 1
        if d == -1:
            d = 3
    # perform step
    if d == 0:
        if p0 > 0:
            p[0] -= 1
        else:
            p[0] = len(grid)-1
    if d == 1:
        if p1 < len(grid)-1:
            p[1] += 1
        else:
            p[1] = 0
    if d == 2:
        if p0 < len(grid)-1:
            p[0] += 1
        else:
            p[0] = 0
    if d == 3:
        if p1 > 0:
            p[1] -= 1
        else:
            p[1] = len(grid)-1
    return grid, p, d
    
def vaccinated(grid):
    for r in grid:
        for c in r:
            if c not in [2,3]:
                return False
    return True

def simulate(g, maxn = 1000, checkfreq = 100):
    p = [0,0]
    d = 0
    for i in range(maxn):
        if i%checkfreq == 0:
            v = vaccinated(g)
            if v:
                pgrid(g)
                return True
        g,p,d = perform_step(g,p,d)
        #pgrid(g)
    #pgrid(g)
    return False
        
    
def pgrid(g):
    for row in g:
        print(row)
    print()

# initial_grid = []
# for i in range(N):
#     initial_grid.append([0]*N)
# initial_p = [0,0]
# initial_d = 0
# pgrid(initial_grid)

N = 50
counter = 0
st = time()
for x1 in range(N):
    for y1 in range(N):
        for x2 in range(N):
            for y2 in range(N): 
                if x1*N + y1 < x2*N + y2:
                    g = []
                    for i in range(N):
                        g.append([0]*N)
                    g[x1][y2] = 3
                    g[x2][y2] = 3
                    counter += 1
                    if counter%5000 == 0:
                        print(counter)
                        print(time()-st)
                    if simulate(g, 50000, 2000):
                        print((x1,y1))
                        print((x2,y2))
                        raise SystemExit(0)