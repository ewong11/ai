# -*- coding: utf-8 -*-
"""TicTacToe-HW3.ipynb

### TicTac Toe Homework 3###

We're closing in on a real competitor, with new properties of the BoardNode that will guide us to true bliss and the best next move.

Again, I'm using layout and board sometimes synonymously.
"""

import random

''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# Best future states according to the player viewing this board
ST_X = 1  # X wins
ST_O = 2  # O wins
ST_D = 3  # Draw

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {}   # This is primarily for debugging: key = layout, value = BoardNode

class BoardNode:

    def __init__(self, layout):
        self.layout = layout
        self.mover = 'x' if layout.count('x') == layout.count('o') else 'o'

        self.state = BoardNode.this_state(layout) # if final board, then ST_X, ST_O or ST_D, else None
        if self.state is None:
            self.best_final_state = None           # best achievable future state: ST_X, ST_O or ST_D
            self.best_move = None                  # 0-9 to achieve best state
            self.num_moves_to_final_state = None   # number of moves to best state
        else:
            self.best_final_state = self.state
            self.best_move = -1
            self.num_moves_to_final_state = 0

        self.children = set()

    def print_me(self):
        print('layout:',self.layout)
        print('mover:',self.mover)
        print('state:',BoardNode.str_state(self.state))
        print('best_final_state:',BoardNode.str_state(self.best_final_state))
        print('best_move:',self.best_move,BoardNode.str_move(self.best_move))
        print('num_moves_to_final_state:',self.num_moves_to_final_state)

    def print_layout(self):
        print('%s\n%s\n%s' % (' '.join(self.layout[0:3]),' '.join(self.layout[3:6]),' '.join(self.layout[6:9])))

    # =================== class methods  =======================
    def str_state(state):
        # human description of a state
        return 'None' if state is None else ['x-wins','o-wins','draw'][state-1]

    def str_move(move):
        # human description of a move
        moves = ('top-left','top-center','top-right',\
                 'middle-left','middle-center','middle-right',\
                 'bottom-left','bottom-center','bottom-right')
        return 'done' if move == -1 else moves[move]

    def this_state(layout):
        # classifies this layout as None if not final, otherwise ST_X or ST_O or ST_D
        for awin in Wins:
            if layout[awin[0]] != '_' and layout[awin[0]] == layout[awin[1]] == layout[awin[2]]:
                return ST_X if layout[awin[0]] == 'x' else ST_O
        if layout.count('_') == 0:
            return ST_D
        return None

def CreateAllBoards(layout):
    # Populate AllBoards with finally calculated BoardNodes

    if layout in AllBoards:
        return

    anode = BoardNode(layout)
    # if this is an end board, then all of its properties have already be calculated by __init__()
    if anode.state is not None:
        AllBoards[layout] = anode
        return

    # expand children if this is not a final state
    move = 'x' if layout.count('x') == layout.count('o') else 'o'
    for pos in range(9):
        if layout[pos] == '_':
            new_layout = layout[:pos] + move + layout[pos+1:]
            if new_layout not in AllBoards:
                CreateAllBoards(new_layout)
            anode.children.add(new_layout)

    # ==============================================================================
    # Your excellent code here to calculate the BoardNode properties below for this node
    #   best_move
    #   best_final_state
    #   num_moves_to_final_state
    # ===============================================================================

    #list of wins, draws, and losses possible
    winState = []
    loseState = []
    drawState = []


    if (anode.mover == "x") :
        WIN = 1
        LOSS = 2
    else:
        WIN = 2
        LOSS = 1

    if (len(winState) > 0):
        anode.best_final_state = WIN
        bestLayout = winState[0]
        for a in winState:
            if (AllBoards[a].num_moves_to_final_state < AllBoards[bestLayout].num_moves_to_final_state):
                bestLayout = a

    elif (len(draws) > 0):
        anode.best_final_state = 3 #draw
        bestLayout = draws.pop()

    else:
        anode.best_final_state = LOSS
        bestLayout = loseState[0]
        for b in loseState:
            if (AllBoards[b].num_moves_to_final_state > AllBoards[bestLayout].num_moves_to_final_state):
                bestLayout = b

    anode.num_moves_to_final_state = AllBoards[bestLayout].num_moves_to_final_state + 1

    if anode.mover == "x":
        for i in anode.children:
            child = AllBoards[i]
            if (child.best_final_state == 1):
                winState.append(i)
            elif (child.best_final_state == 2):
                loseState.append(i)
            else:
                drawState.append(i)
    if anode.mover == "o":
        for i in anode.children:
            child = AllBoards[i]
            if (child.best_final_state == 2):
                winState.append(i)
            elif (child.best_final_state == 1):
                loseState.append(i)
            else:
                drawState.append(i)

    for i in range(9):
        if (anode.layout[i] != bestLayout[i]):
            anode.best_move = i
            break

    AllBoards[layout] = anode

#  Test me here...
AllBoards = {}
print('x should win this one in 3 moves')
b='x_o_o___x'
CreateAllBoards(b)
AllBoards[b].print_me()
AllBoards[b].print_layout()

AllBoards = {}
b='x__xoxo__'
print('\no should win this one in 1 move')
CreateAllBoards(b)
AllBoards[b].print_me()
AllBoards[b].print_layout()

AllBoards = {}
b='_________'
print('\nthis should be a draw in 9 moves')
CreateAllBoards(b)
AllBoards[b].print_me()
AllBoards[b].print_layout()
