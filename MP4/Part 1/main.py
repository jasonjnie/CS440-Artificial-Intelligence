import math
import random
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import os
import time

# Magic Numbers
# The world model
GRID_X = 12
GRID_Y = 12
PADDLE_Y = 12
VELO_X_NUM = [-1,1]
VELO_Y_NUM = [-1,0,1]
PADDLE_HEIGHT = 0.2


# Learning parameters
"""
C = 1.0
GAMMA = 0.9
DISCOUNT = 0.3
EXPLOR = 1000
GAME_NUM = 100000
TEST_GAME_NUM = 1000
R_P = 10
testing
9.028
"""
"""
9.028
C = 40
GAMMA = 0.9
EXPLOR = 4000
GAME_NUM = 300000
TEST_GAME_NUM = 1000
R_P = 30
"""
C = 40
GAMMA = 0.9
EXPLOR = 2000
GAME_NUM = 500000
TEST_GAME_NUM = 1000
R_P = 30
"""
testing
10.412
"""

# STATE = [ball_x, ball_y, vel_x, vel_y, paddle_y, paddle_op_y]
# Actions of the agent
ACTIONS = [-0.04,0,0.04,None]
ACTIONS_OP = [-0.02,0,0.02,None]
INIT_STATE = [0.5, 0.5, 0.03, 0.01, 0.5 - (PADDLE_HEIGHT/2), 0.5 - (PADDLE_HEIGHT/2)]
INIT_ACTION = 0
PIXEL_LEVEL = 40

glo_reward = 0
reward_total = 0
agent_wins = 0

def ani(state):
    if state == -1:
        return
    else:
        bx = state[0]
        by = state[1]
        vx = state[2]
        vy = state[3]
        paddle_y = state[4]
        paddle_op_y = state[5]

        if bx > 1:
            return -1
        if bx == 1:
            discrete_bx = PIXEL_LEVEL - 1
        else:
            discrete_bx = math.floor(PIXEL_LEVEL*bx) 

        if by == 1:
            discrete_by = PIXEL_LEVEL - 1
        else:
            discrete_by = math.floor(PIXEL_LEVEL*by)

        if vx < 0:
            discrete_vx = -1
        else:
            discrete_vx = 1

        if abs(vy) < 0.015:
            discrete_vy = 0
        elif vy < 0:
            discrete_vy = -1
        else:
            discrete_vy = 1

        if paddle_y == 1:
            discrete_paddle_y = PIXEL_LEVEL - 1
        else:
            discrete_paddle_y = math.floor(PIXEL_LEVEL*paddle_y)
        
        paddle_height = math.floor(PIXEL_LEVEL*PADDLE_HEIGHT)

        if paddle_op_y == 1:
            discrete_paddle_op_y = PIXEL_LEVEL - 1
        else:
            discrete_paddle_op_y = math.floor(PIXEL_LEVEL*paddle_op_y)
        
        paddle_op_height = math.floor(PIXEL_LEVEL*PADDLE_HEIGHT)

        for y in range(0,PIXEL_LEVEL):
            line = ""
            for x in range(0,PIXEL_LEVEL):
                if discrete_bx == x and discrete_by == y:
                   line += "*"
                elif x == (PIXEL_LEVEL - 1) and discrete_paddle_y <= y and y <= (discrete_paddle_y+paddle_height):
                    line +="@"
                elif x == 0 and discrete_paddle_op_y <= y and y <= (discrete_paddle_op_y+paddle_op_height):
                    line +="@"                   
                else:
                    line += ' '
            print(line)
        print("\n")


Q = {}
N_sa = {}
def init():
    for bx in range(0,GRID_X):
        for by in range(0,GRID_Y):
            for vx in range(0,len(VELO_X_NUM)):
                for vy in range(0,len(VELO_Y_NUM)):
                    for paddle_y in range(0,PADDLE_Y):
                        for paddle_op_y in range(0,PADDLE_Y):
                            for action in range(-1,len(ACTIONS)-1):  
                                Q[(bx,by,vx,vy,paddle_y,paddle_op_y,action)] = 0
                                N_sa[(bx,by,vx,vy,paddle_y,paddle_op_y,action)] = 0
    # Final states
    Q[-1] = 0
    N_sa[-1] = 0

def get_reward(state):                                              
    bx = state[0]
    by = state[1]
    vx = state[2]
    vy = state[3]
    paddle_y = state[4]
    paddle_op_y = state[5]
    if bx > 1:
        return -1
    return glo_reward;

'''
def get_points(state):                                              
    bx = state[0]
    by = state[1]
    vx = state[2]
    vy = state[3]
    paddle_y = state[4]
    """
    if bx < 1 and (bx+vx) >= 1 and (by+vy) >= paddle_y and (by+vy) <= (paddle_y + PADDLE_HEIGHT):
        return 1
    return 0
    """
    return glo_reward;
'''

def discrete_state(state):
    bx = state[0]
    by = state[1]
    vx = state[2]
    vy = state[3]
    paddle_y = state[4]
    paddle_op_y = state[5]

    if bx > 1:
        return -1

    if bx < 0:
        return -1

    if bx == 1:
        discrete_bx = GRID_X - 1
    else:
        discrete_bx = math.floor(GRID_X*bx)

    if by == 1:
        discrete_by = GRID_Y - 1
    else:
        discrete_by = math.floor(GRID_Y*by)

    if vx < 0:
        discrete_vx = 0
    else:
        discrete_vx = 1

    if abs(vy) < 0.015:
        discrete_vy = 1
    elif vy < 0:
        discrete_vy = 0
    else:
        discrete_vy = 2

    if paddle_y == 1 - PADDLE_HEIGHT:
        discrete_paddle_y = PADDLE_Y - 1
    else:
        discrete_paddle_y = math.floor(PADDLE_Y*paddle_y/(1-PADDLE_HEIGHT))

    if paddle_op_y == 1 - PADDLE_HEIGHT:
        discrete_paddle_op_y = PADDLE_Y - 1
    else:
        discrete_paddle_op_y = math.floor(PADDLE_Y*paddle_op_y/(1-PADDLE_HEIGHT))       

    return (discrete_bx,discrete_by,discrete_vx,discrete_vy,discrete_paddle_y,discrete_paddle_op_y)


def get_action_id(action):                                              
    if action==None:
        return 2
    else:
        return action/0.04     # 1,0,-1


# This state is discreted
def state_action_tuple(state,action):
    if state == -1:
        return -1
    else:
        return (state[0],state[1],state[2],state[3],state[4],state[5],get_action_id(action))


def exploration(Q,N_sa):
    if N_sa < EXPLOR:
        return R_P
    else:
        return Q


def get_next_action(discrete_state):

    possible_utility = []
    for next_action in ACTIONS[0:3]:
        possible_utility.append([Q[state_action_tuple(discrete_state,next_action)],next_action])

    pair = max(possible_utility, key=lambda x: x[0])

    return pair[1]   # return one action w/ largest utility

"""
def get_next_action(discrete_state):
    possible_utility = []
    for next_action in ACTIONS[0:3]:
        possible_utility.append([Q[state_action_tuple(discrete_state,next_action)],next_action])

    pair = max(possible_utility, key=lambda x: x[0])
    maxVal = pair[0]
    actions_aval = []
    for item in possible_utility:
        if maxVal == item[0]:
            actions_aval.append(item[1])
    random.shuffle(actions_aval)
    return actions_aval[0]
"""


def get_next_action_explor(discrete_state):
    possible_utility = []
    for next_action in ACTIONS[0:3]:
        possible_utility.append([exploration(Q[state_action_tuple(discrete_state,next_action)],N_sa[state_action_tuple(discrete_state,next_action)]),next_action])

    pair = max(possible_utility, key=lambda x: x[0])
    maxVal = pair[0]
    actions_aval = []
    for item in possible_utility:
        if maxVal == item[0]:                                              
            actions_aval.append(item[1])    # in case multiple actions have same utilities
    random.shuffle(actions_aval)
    return actions_aval[0]      # return one action with largest utility


def get_op_action(paddle_op_y,by):
    # ACTIONS_OP = [-0.02,0,0.02,None]
    if (paddle_op_y+PADDLE_HEIGHT/2) < by:
        action_op = ACTIONS_OP[2]
    elif (paddle_op_y+PADDLE_HEIGHT/2) == by:
        action_op = ACTIONS_OP[1]
    elif (paddle_op_y+PADDLE_HEIGHT/2) > by:
        action_op = ACTIONS_OP[0]
    return action_op


def get_next_state(state,action):
    global glo_reward
    global reward_total
    bx = state[0]
    by = state[1]
    vx = state[2]
    vy = state[3]
    paddle_y = state[4]
    paddle_op_y = state[5]

    old_bx = bx
    bx = bx + vx
    by = by + vy

    paddle_y = paddle_y + action
    new_bx = bx
    new_by = by
    new_vy = vy
    new_vx = vx
    new_paddle_y = paddle_y

    action_op = get_op_action(paddle_op_y,new_by)
    new_paddle_op_y = paddle_op_y + action_op      

    if new_paddle_y < 0:
        new_paddle_y = 0
    elif new_paddle_y > (1-PADDLE_HEIGHT):
        new_paddle_y = 1-PADDLE_HEIGHT

    if new_paddle_op_y < 0:
        new_paddle_op_y = 0
    elif new_paddle_op_y > (1-PADDLE_HEIGHT):
        new_paddle_op_y = 1-PADDLE_HEIGHT       

    if by < 0:              # hitting upper bound
        new_by = -by
        new_vy = -vy

    if by > 1:              # hitting lower bound
        new_by = 2 - by
        new_vy = -vy

    if bx > 1 and old_bx < 1 and by >= paddle_y and by <= (paddle_y + PADDLE_HEIGHT):
        U = random.uniform(-0.015,0.015)
        V = random.uniform(-0.03,0.03)
        new_bx = 2 * 1 - bx
        new_vx = -vx + U
        new_vy = vy + V
        glo_reward = 1                      # ball hitting agent's paddel, reward ++
        reward_total += 1

    if bx < 0 and old_bx > 0 and by >= paddle_op_y and by <= (paddle_op_y + PADDLE_HEIGHT):
        U = random.uniform(-0.015,0.015)    # ball hitting opponent's paddle
        V = random.uniform(-0.03,0.03)
        new_bx = -bx
        new_vx = -vx + U
        new_vy = vy + V 

    if (bx < 0 and old_bx > 0) and (by < paddle_op_y or by > (paddle_op_y + PADDLE_HEIGHT)):
        glo_reward = 1                       # opponent missed the ball

    if new_vx > -0.03 and new_vx <= 0:
        new_vx = -0.03
    elif new_vx < 0.03 and new_vx > 0:
        new_vx = 0.03
    elif new_vx > 1:
        new_vx = 0.9
    elif new_vx < -1:
        new_vx = -0.9

    return [new_bx,new_by,new_vx,new_vy,new_paddle_y,new_paddle_op_y]


def is_terminal(state):
    if state == None:
        return False
    bx = state[0]
    if bx > 1:
        return 2    # opponent wins
    elif bx < 0:
        return 1    # agent wins
    return False


# Q_learning 
def Q_learning(state,pre_state,action,reward):
    global glo_reward
    reward_signal = get_reward(state)
    if reward_signal == 1:
        glo_reward = 0
    if (is_terminal(pre_state)==1) or (is_terminal(pre_state)==2) :
        Q[state_action_tuple(discrete_state(pre_state),None)] = reward_signal

    if pre_state == None:
        return (state,action,reward)
    discrete_pre_state = discrete_state(pre_state)
    discrete_cur_state = discrete_state(state)
    N_sa[state_action_tuple(discrete_pre_state,action)] += 1

    possible_utility = []
    for next_action in ACTIONS[0:3]:
        possible_utility.append(Q[state_action_tuple(discrete_cur_state,next_action)])

    if (is_terminal(pre_state)==1) or (is_terminal(pre_state)==2) :
        max_q = 0
    else:
        max_q = max(possible_utility)

    alpha = C/(C+N_sa[state_action_tuple(discrete_pre_state,action)]);
    pre_q = Q[state_action_tuple(discrete_pre_state,action)];
    Q[state_action_tuple(discrete_pre_state,action)] = pre_q + alpha*(reward+GAMMA*max_q-pre_q)   # ppt L28 P23

    return (state,get_next_action_explor(discrete_cur_state),reward_signal)


def training():
    init()
    global reward_total
    global agent_wins
    train_game = 0
    while train_game < GAME_NUM:
        print('Training:',train_game)
        next_pair = Q_learning(INIT_STATE,None,INIT_ACTION,0)
        while True:
            cur_state = next_pair[0]
            cur_action = next_pair[1]
            cur_reward = next_pair[2]
            next_state = get_next_state(cur_state,cur_action)
            next_pair = Q_learning(next_state,cur_state,cur_action,cur_reward)

            if next_pair == None:
                train_game += 1
                break
            if (is_terminal(cur_state)==1) or (is_terminal(cur_state)==2):
                train_game += 1
                break

    print("testing")
    reward_total = 0
    test_game = 0
    while test_game < TEST_GAME_NUM:
        print('Testing:',test_game)
        next_pair = (INIT_STATE,INIT_ACTION)
        while True:
            cur_state = next_pair[0]
            cur_action = next_pair[1]
            next_state = get_next_state(cur_state,cur_action)
            next_action =  get_next_action(discrete_state(next_state));
            next_pair = (next_state,next_action)
            if is_terminal(next_state) == 1:       # agent wins
                test_game += 1
                agent_wins += 1
                break
            elif is_terminal(next_state) == 2:     # opponent wins
                test_game += 1
                break
    print('Average Bounce =',reward_total/test_game)

    print('Agent Wins:',agent_wins/TEST_GAME_NUM*100,'%')


"""
def testing():
    global reward_total
    reward_total = 0
    test_game = 0
    while test_game < TEST_GAME_NUM:
        next_pair = Q_learning(INIT_STATE,None,INIT_ACTION,0)
        while True:
            
            cur_state = next_pair[0]

            print(test_game,reward_total)
            ani(cur_state)
            time.sleep(0.1)
            os.system('clear') 

            #points += get_points(cur_state)
            cur_action = next_pair[1]
            cur_reward = next_pair[2]
            next_state = get_next_state(cur_state,cur_action)
            next_pair = Q_learning(next_state,cur_state,cur_action,cur_reward)
            if next_pair == None:
                test_game += 1
                break
    print(reward_total/test_game)
"""
def testing():
    global reward_total
    reward_total = 0
    test_game = 0
    while test_game < TEST_GAME_NUM:
        next_pair = (INIT_STATE,INIT_ACTION)
        while True:
            cur_state = next_pair[0]
            cur_action = next_pair[1]
            next_state = get_next_state(cur_state,cur_action)
            next_action =  get_next_action(discrete_state(next_state));
            next_pair = (next_state,next_action)
            if is_terminal(next_state):
                test_game += 1
                break
    print(reward_total/test_game)
"""
for GAMMA in [0.7,0.8,0.9]:
    for C in [30,40,50,60,70,80,90]:
        print(GAMMA,C)
        training()
"""
training()
#print("testing")
#testing()
