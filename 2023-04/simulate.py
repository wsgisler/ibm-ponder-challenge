def print_grid(grid):
    for r in grid:
        print(''.join([str(i) for i in r]))
    print('\n')

def simulate(g, seq, print_log = True):
    n = len(g)
    
    print_grid(g)
    
    for i,choice in enumerate(seq):
        if print_log: print(choice)
        r = n-choice[1]
        c = choice[0]-1
        if g[r][c] != 0:
            print('Warning: cell is not equal to 0')
        for r2 in range(n):
            g[r2][c] = 1-g[r2][c]
        for c2 in range(n):
            if c2 != c:
                g[r][c2] = 1-g[r][c2]
        if print_log or i+1 == len(seq): print_grid(g)
    
ig = [[0,0,1,1],
[1,1,0,1],
[0,1,1,0],
[0,0,0,1]]

ig2 = [[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1],
[1,1,0,1,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,1,0,0,1,1],
[0,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1,1,1,0],
[0,0,0,1,1,0,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,1,0,0],
[1,0,1,1,0,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,1,0,1,0],
[1,1,1,0,0,0,1,0,0,1,0,1,1,1,0,1,0,0,1,0,1,0,0,0],
[1,1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
[1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0],
[0,0,0,1,1,0,0,1,0,0,1,0,1,1,0,1,1,0,1,0,1,0,0,1],
[0,1,1,1,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,0,0,0,0],
[0,1,1,0,0,0,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,1,0,0],
[1,0,0,0,1,1,1,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,1,1],
[0,0,0,1,1,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,1,1,1,0],
[0,1,1,0,0,1,0,1,0,0,0,1,0,0,1,1,1,1,1,1,0,1,0,1],
[1,1,0,0,0,1,0,0,0,0,1,0,1,1,1,0,0,0,1,0,0,0,0,0],
[0,0,0,0,0,0,1,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1],
[1,1,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,1,1,1,0,1,1,0],
[1,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,0,1,1,0,1,0],
[1,1,0,1,0,0,0,0,0,0,1,1,1,0,0,1,0,0,1,1,0,0,1,0],
[1,0,1,0,0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,1,0,0,0,0],
[1,1,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,0,1],
[1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,0,0,0,1,0,1,0,1],
[0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,1,1,1,0,0,0,0,0],
[1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1]]

ig3 = [[1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,0,1,1,0,0,1,0,0,0],
[0,1,0,1,0,0,0,0,1,1,0,0,0,1,1,1,0,1,0,1,0,1,1,1,1,0,0,1,1,0],
[0,0,0,1,1,0,0,1,1,0,1,0,0,1,1,1,1,1,1,0,0,0,1,0,1,0,0,0,1,0],
[1,1,1,1,0,1,1,1,0,1,1,0,0,1,1,1,0,1,1,1,0,1,0,0,1,1,0,0,0,1],
[0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,0,1,0],
[1,0,1,1,1,1,0,0,1,1,1,0,1,1,0,0,1,0,1,1,1,1,0,1,0,0,1,1,1,1],
[0,0,1,1,1,0,0,0,0,1,0,1,1,0,1,0,0,1,1,0,1,0,0,0,0,0,1,1,0,1],
[1,1,1,0,0,1,1,1,0,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0],
[1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,1,0,0],
[1,1,1,0,0,1,1,1,0,1,0,0,1,1,1,1,1,0,0,0,1,1,1,0,1,1,1,0,1,1],
[1,1,1,0,1,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,1,1,0,0],
[0,1,0,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,0,1,0,0,0,0,1,0,0,1],
[0,1,0,1,0,0,1,1,1,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0],
[0,1,0,0,0,1,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,0,1],
[1,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,0,0,1,0,1,1,0,0,1,1,0,1,1,0],
[1,0,1,0,0,0,1,1,0,1,1,0,0,1,0,1,1,1,1,1,1,0,1,1,0,0,1,0,0,1],
[1,1,1,0,1,1,0,0,0,1,0,0,1,0,1,1,1,1,1,0,1,0,0,1,1,0,0,0,1,0],
[1,0,1,0,0,1,1,0,0,0,1,1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
[1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,0,1,1,1,1,1,0,0,1,0],
[0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1],
[1,1,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1,0,0,1,1,0,1,1,0],
[0,1,1,1,0,0,1,1,0,0,0,1,1,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0],
[1,1,1,1,1,0,1,0,0,1,0,1,0,1,0,0,0,0,1,0,0,0,1,1,0,1,1,0,1,0],
[1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,1,1,1,1],
[1,1,1,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,0,1,0,0],
[1,0,1,0,1,1,0,0,0,0,1,1,0,0,1,1,1,0,1,0,1,0,1,1,0,0,0,0,1,1],
[0,0,1,1,0,1,0,1,1,1,0,1,0,0,0,0,0,1,1,0,0,1,0,1,1,0,1,0,0,1],
[0,1,0,0,1,0,1,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,0,1,0,1,0,0,0,1],
[0,1,0,1,1,1,1,0,1,0,0,1,1,1,0,1,0,0,0,1,0,1,1,0,0,1,0,0,1,0],
[1,1,0,0,0,0,0,1,1,0,1,0,1,1,1,1,1,0,1,0,0,1,1,0,0,0,0,0,1,0]]

# simulate(ig, [(2, 4), (2, 3), (1, 1), (4, 4)], print_log = False)
# simulate(ig, [(1, 1), (2, 4), (2, 3), (4, 4)])
# simulate(ig, [(4,4),(1, 1), (2, 4), (2, 3)], print_log = False)

# simulate(ig2, [(1, 14), (5, 5), (13, 22), (18, 4), (21, 24), (7, 6), (19, 14), (6, 9), (12, 10), (4, 13), (11, 18), (16, 2), (13, 19), (15, 12), (13, 2), (7, 18), (8, 22), (17, 23), (24, 23), (22, 23), (18, 19), (24, 16), (2, 7), (4, 7), (20, 2), (22, 14), (1, 7), (16, 23), (15, 24), (24, 22), (14, 17), (5, 2), (24, 3), (19, 17), (14, 5), (10, 17), (22, 2), (10, 18), (16, 6), (8, 2), (17, 4), (15, 6), (8, 19), (14, 14), (22, 21), (23, 6), (2, 14), (19, 9), (11, 22), (19, 3), (21, 18), (15, 3), (16, 17), (8, 18), (13, 17), (4, 1), (23, 22), (1, 17), (21, 6), (12, 5), (1, 12), (12, 3), (9, 1), (18, 22), (13, 7), (13, 3), (1, 15), (6, 21), (14, 13), (3, 17), (18, 5), (20, 17), (3, 22), (19, 10), (21, 15), (7, 10), (14, 2), (2, 5), (22, 7), (21, 16), (19, 21), (19, 6), (16, 8), (19, 15), (11, 8), (23, 4), (13, 24), (20, 20), (12, 24), (18, 21), (3, 1), (10, 11), (24, 11), (3, 7), (5, 11), (14, 11), (24, 14), (1, 23), (16, 1), (13, 16), (15, 5), (18, 24), (12, 14), (4, 12), (7, 5), (20, 6), (9, 24), (14, 1), (12, 17), (1, 4), (3, 14), (12, 21), (6, 14), (3, 16), (14, 23), (23, 5), (8, 4), (6, 8), (12, 18), (11, 23), (5, 23), (19, 7), (3, 23), (1, 22), (11, 20), (4, 6), (22, 19), (13, 23), (15, 23), (16, 20), (1, 8), (2, 20), (23, 12), (1, 20), (10, 20), (16, 22), (7, 7), (6, 1), (5, 7), (9, 12), (17, 14), (2, 16), (21, 19), (17, 19), (7, 13), (15, 2), (9, 20), (6, 11), (20, 19), (2, 18), (23, 11), (23, 2), (17, 15), (14, 21), (19, 24), (9, 3), (12, 7), (9, 22), (1, 9), (15, 18), (5, 19), (8, 21), (3, 4), (5, 4), (24, 13), (20, 16), (4, 2), (24, 12), (10, 3), (24, 4), (18, 16), (11, 13), (11, 3), (1, 5), (9, 6), (11, 21), (19, 1), (3, 2), (11, 16), (18, 23), (1, 21), (16, 21), (1, 24), (23, 24), (21, 1), (3, 15), (11, 9), (22, 16), (15, 21), (15, 4), (10, 4), (22, 22), (4, 4), (23, 19), (5, 20), (22, 20), (24, 15), (4, 17), (20, 1), (4, 8), (11, 2), (22, 18), (20, 13), (2, 22), (2, 15), (18, 3), (2, 13), (6, 20), (19, 5), (9, 10), (5, 17), (1, 3), (7, 19), (21, 7), (12, 19), (14, 10), (22, 5), (24, 1), (1, 1), (12, 22), (1, 13), (11, 24), (13, 18), (5, 12), (15, 7), (6, 3), (14, 15), (10, 13), (24, 6), (18, 14), (6, 13), (12, 11), (7, 12), (3, 13), (4, 19), (11, 5), (2, 17), (4, 22), (17, 12), (19, 23), (10, 16), (7, 24), (10, 7), (20, 14), (10, 8), (4, 15), (1, 19), (18, 15), (18, 13), (4, 5), (20, 4), (17, 13), (4, 11), (23, 3), (20, 24), (12, 9), (8, 12), (10, 9), (5, 8), (18, 17), (2, 2), (22, 12), (17, 17), (2, 6), (5, 1), (15, 11), (2, 10), (6, 6), (22, 17), (12, 12), (5, 21), (7, 1), (17, 3), (11, 4), (23, 16), (21, 10), (24, 21), (24, 10), (4, 21), (21, 20)])

simulate(ig3, [(28, 11), (3, 3), (3, 23), (9, 10), (21, 29), (6, 20), (30, 3), (13, 7), (6, 2), (30, 25), (22, 13), (22, 17), (22, 8), (12, 1), (12, 19), (6, 9), (11, 22), (1, 8), (28, 24), (2, 23), (20, 5), (11, 24), (30, 17), (12, 3), (7, 30), (30, 2), (6, 3), (3, 17), (25, 24), (6, 18), (3, 11), (14, 29), (11, 18), (22, 22), (29, 1), (8, 19), (24, 19), (15, 19), (15, 7), (7, 12), (8, 25), (15, 24), (10, 26), (10, 21), (15, 20), (20, 26), (10, 17), (29, 25), (12, 25), (12, 13), (18, 13), (24, 6), (29, 12), (23, 14), (30, 26), (11, 20), (6, 27), (5, 7), (22, 21), (30, 4), (20, 8), (22, 5), (26, 5), (18, 5), (13, 10), (29, 11), (24, 7), (26, 13), (4, 9), (15, 27), (5, 4), (8, 3), (14, 2), (21, 8), (23, 29), (28, 21), (8, 14), (24, 2), (7, 20), (20, 25), (9, 3), (23, 30), (22, 24), (7, 26), (1, 30), (10, 12), (10, 25), (3, 18), (2, 2), (14, 7), (12, 8), (27, 9), (23, 9), (22, 4), (28, 23), (12, 28), (20, 7), (9, 17), (30, 21), (17, 16), (11, 28), (5, 21), (24, 12), (30, 23), (26, 21), (24, 25), (15, 18), (23, 8), (17, 15), (6, 28), (3, 13), (11, 29), (30, 11), (10, 14), (7, 29), (1, 9), (11, 17), (16, 3), (9, 16), (11, 7), (5, 8), (30, 30), (27, 19), (8, 15), (11, 6), (28, 12), (1, 3), (19, 19), (23, 4), (3, 8), (22, 12), (25, 21), (19, 30), (27, 1), (10, 23), (11, 2), (11, 8), (26, 12), (29, 7), (2, 8), (16, 22), (17, 11), (24, 14), (19, 24), (27, 8), (24, 3), (14, 27), (13, 18), (18, 2), (29, 27), (21, 21), (10, 4), (2, 25), (21, 10), (12, 11), (16, 6), (8, 12), (5, 2), (3, 15), (9, 21), (9, 2), (8, 20), (24, 4), (22, 30), (17, 19), (2, 22), (22, 10), (11, 23), (10, 22), (14, 22), (19, 22), (10, 19), (14, 18), (23, 2), (13, 30), (14, 15), (21, 19), (4, 22), (28, 3), (28, 14), (2, 28), (1, 11), (29, 22), (13, 4), (5, 24), (2, 19), (25, 6), (7, 6), (13, 26), (29, 16), (8, 23), (18, 18), (16, 5), (17, 26), (6, 1), (16, 29), (17, 20), (6, 30), (29, 14), (19, 20), (7, 21), (5, 17), (23, 16), (21, 25), (5, 26), (23, 3), (18, 3), (7, 24), (23, 25), (25, 5), (1, 27), (3, 28), (16, 4), (13, 3), (10, 6), (1, 23), (28, 28), (22, 1), (2, 30), (28, 22), (7, 18), (27, 28), (3, 5), (18, 14), (19, 23), (17, 5), (17, 9), (2, 27), (25, 19), (17, 4), (6, 5), (23, 7), (30, 22), (5, 19), (11, 1), (7, 10), (27, 11), (6, 11), (18, 10), (25, 30), (4, 30), (20, 12), (21, 2), (12, 21), (12, 24), (24, 24), (25, 15), (9, 26), (23, 20), (25, 10), (22, 3), (22, 25), (24, 17), (21, 16), (6, 19), (29, 18), (1, 18), (12, 2), (29, 21), (30, 8), (2, 29), (16, 19), (26, 10), (26, 15), (21, 14), (23, 10), (20, 24), (29, 13), (29, 28), (24, 20), (9, 11), (15, 23), (26, 19), (18, 11), (16, 15), (20, 6), (22, 16), (27, 30), (27, 12), (26, 22), (18, 8), (19, 5), (25, 20), (4, 18), (4, 7), (1, 28), (1, 5), (27, 3), (28, 18), (18, 7), (14, 4), (25, 14), (19, 11), (21, 11), (13, 2), (9, 9), (27, 6), (28, 4), (15, 25), (27, 24), (27, 10), (4, 5), (5, 5), (11, 10), (11, 26), (13, 16), (23, 23), (16, 2), (13, 28), (13, 20), (4, 16), (23, 5), (13, 22), (19, 15), (21, 27), (6, 6), (6, 10), (3, 27), (26, 3), (15, 29), (15, 4), (27, 16), (7, 9), (29, 19), (30, 29), (4, 28), (3, 24), (14, 8), (29, 15), (13, 23), (12, 14), (29, 10), (24, 27), (3, 1), (13, 11), (22, 15), (16, 13), (24, 13), (25, 2), (2, 4), (19, 8), (26, 26), (26, 16), (26, 24), (9, 20), (5, 9), (4, 13), (1, 22), (29, 23), (25, 8), (28, 1), (8, 27), (14, 6), (11, 12), (1, 15), (14, 13), (17, 22), (17, 23), (25, 12), (4, 25), (14, 9), (12, 20), (11, 30), (7, 22), (4, 23), (16, 11), (7, 5), (10, 30), (16, 27), (14, 14), (26, 11), (4, 12), (27, 14), (27, 15), (18, 28), (7, 3), (10, 7), (10, 5), (12, 5), (26, 29), (10, 13), (25, 16), (25, 4), (30, 7), (4, 15), (18, 4), (26, 30), (10, 2), (6, 23), (15, 5), (6, 7), (25, 28), (19, 27), (29, 9), (18, 9), (16, 18), (16, 25), (16, 9), (19, 12), (21, 30), (23, 18), (12, 17), (16, 30), (23, 15), (17, 17), (26, 18), (29, 24), (18, 6), (5, 6), (1, 13), (1, 4), (11, 25), (21, 13), (29, 30), (13, 24), (9, 14), (9, 29), (9, 12), (4, 4), (16, 7), (19, 21), (28, 29), (5, 1), (1, 17), (5, 18), (6, 13), (5, 11), (17, 18), (21, 6)])