from random import random

def board_string(board):
    result = ''
    for row in board:
        for col in row:
            result += str(col)
    return result
    
def next_board(board, rule_born, rule_stay_alive):
    new_board = [[0 for i in range(len(board))] for j in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board)):
            surrounding_alive = 0
            if i >= 1:
                surrounding_alive += board[i-1][j]
            if i < len(board)-1:
                surrounding_alive += board[i+1][j]
            if j >= 1:
                surrounding_alive += board[i][j-1]
            if j < len(board)-1:
                surrounding_alive += board[i][j+1]
            if board[i][j] == 0:
                new_board[i][j] = 1 if rule_born[surrounding_alive] == 1 else 0
            else:
                new_board[i][j] = 1 if rule_stay_alive[surrounding_alive] == 1 else 0
    return new_board

def silent_iterate(board, generations, rule_born, rule_stay_alive, target_cycle_length):
    past_boards = dict()
    past_boards[board_string(board)] = 0
    found = False
    for gen in range(1,generations+1):
        board = next_board(board, rule_born, rule_stay_alive)
        bs = board_string(board)
        if bs in past_boards:
            found = True
            if target_cycle_length == gen-past_boards[bs]:
                print('Cycle of length %i found after %i generations'%(gen-past_boards[bs], past_boards[bs]))
            return (gen-past_boards[bs], past_boards[bs])
            break
        else:
            past_boards[bs] = gen
    if not found:
        return (0,0)
        
# generate all possible rules:
def test_all_rules_on_start_board(start_board, target_cycle_length):
    for i in range(1024):
        rules = bin(i)[2:]
        while len(rules) < 10:
            rules = '0'+rules
        rule_born = [int(rules[0]), int(rules[1]), int(rules[2]), int(rules[3]), int(rules[4])]
        rule_alive = [int(rules[5]), int(rules[6]), int(rules[7]), int(rules[8]), int(rules[9])]
        result = silent_iterate(start_board, 200000, rule_born, rule_alive, target_cycle_length)
        if result[0] == target_cycle_length:
            print('Did it.')
            print(rule_born)
            print(rule_alive)
            print(start_board)
            return result
    return (0,0)

from time import time
running = True
start_time = time()
while running:
    sb = [[0]*11 for i in range(11)]
    randomfactor = random()
    for i in range(11):
        for j in range(11):
            if random() > randomfactor:
                sb[i][j] = 1
    result = test_all_rules_on_start_board(sb, 72)
    if result[0] == 72 and result[1] > 100000:
        running = False
        print('Time used: '+str(time()-start_time))