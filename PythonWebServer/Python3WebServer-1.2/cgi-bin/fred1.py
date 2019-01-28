#! /usr/bin/python3

import random, sys

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

    def str_move(self, move):
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

    #print(anode.children)


    if anode.state is not None:
        return

    else:
    # Best future states according to the player viewing this board
    #ST_X = 1  # X wins
    #ST_O = 2  # O wins
    #ST_D = 3  # Draw

        wins = []
        losses = []
        draws = []
        for child in anode.children:
            if move == "x":
                if AllBoards[child].best_final_state == 1:
                    wins.append(child)
                elif AllBoards[child].best_final_state == 2:
                    losses.append(child)
                else:
                    draws.append(child)
            elif move == "o":
                if AllBoards[child].best_final_state == 2:
                    wins.append(child)
                elif AllBoards[child].best_final_state == 1:
                    losses.append(child)
                else:
                    draws.append(child)
        # print(wins)
        #print(draws)
        #print(losses)
        if len(wins)>0:
            #print(wins)
            shortest=[wins[0]]
            nextw=[]
            for x in wins:
                #print(AllBoards[x].print_me())
                if AllBoards[x].best_move==-1:
                    nextw.append(x)
                if AllBoards[x].num_moves_to_final_state == AllBoards[shortest[0]].num_moves_to_final_state:
                    shortest.append(x)
                elif AllBoards[x].num_moves_to_final_state < AllBoards[shortest[0]].num_moves_to_final_state:
                    shortest=[wins[0]]
            if len(nextw)>0:
                choice=random.choice(nextw)
            else:
                choice=random.choice(shortest)
            anode.best_final_state=AllBoards[choice].best_final_state
            anode.best_move=choice
            #print("BEST MOVE: " + choice)
            for x in range(len(layout)):
                if choice[x] != layout[x]:
                    #print(x)
                    anode.best_move=x

            anode.num_moves_to_final_state=AllBoards[choice].num_moves_to_final_state+1
        elif len(draws)>0:
            longest=[draws[0]]
            for x in draws:
                if AllBoards[x].num_moves_to_final_state == AllBoards[longest[0]].num_moves_to_final_state:
                    longest.append(x)
                elif AllBoards[x].num_moves_to_final_state > AllBoards[longest[0]].num_moves_to_final_state:
                    longest=[draws[0]]
            choice=random.choice(longest)
            anode.best_final_state=AllBoards[choice].best_final_state
            anode.best_move=choice
            #print("BEST MOVE: " + choice)
            for x in range(len(layout)):
                if choice[x] != layout[x]:
                    #print(x)
                    anode.best_move=x

            anode.num_moves_to_final_state=AllBoards[choice].num_moves_to_final_state+1
        else:
            longest=[losses[0]]
            for x in losses:
                if AllBoards[x].num_moves_to_final_state == AllBoards[longest[0]].num_moves_to_final_state:
                    longest.append(x)
                elif AllBoards[x].num_moves_to_final_state > AllBoards[longest[0]].num_moves_to_final_state:
                    longest=[losses[0]]
            choice=random.choice(longest)
            anode.best_final_state=AllBoards[choice].best_final_state
            anode.best_move=choice
            #print("BEST MOVE: " + choice)
            for x in range(len(layout)):
                if choice[x] != layout[x]:
                    #print(x)
                    anode.best_move=x

            anode.num_moves_to_final_state=AllBoards[choice].num_moves_to_final_state+1

    AllBoards[layout] = anode

def main():
    #AllBoards = {}
    result = ''
    id = 0
    dct = getargs()
    result_prefix = dct['result_prefix']
    result += result_prefix + '\n'
    if 'result_file' in dct:
        try:
            f=open(dct['result_file'],'w')
            f.write(result)
            f.close()
        except:
            print ('Cannot open: %s\n%s\n' % (dct['result_file'],result))
    if 'board' in dct:
        #AllBoards = {}
        b = dct['board']
        CreateAllBoards(b)
        m = int(AllBoards[b].best_move)
        print(m)
        result += "move: " + str(m) + '\n'
        result += "Best move: " + AllBoards[b].str_move(m) + " num moves til end: " + str(AllBoards[b].num_moves_to_final_state) + '\n'
    else:
        id = 1
    if id == 1:
        result += "Author: Eric" + '\n'
        result += "Title: I Tried" + "\n"
    return result


def getargs():
    dct = {}
    for i in range(1,len(sys.argv)):
        sides = sys.argv[i].split('=')
        if len(sides) == 2:
            dct[sides[0]] = sides[1]
    return dct

dct = getargs()
#if 'board' in dct:
#    CreateAllBoards(dct['board'])
print(main())
