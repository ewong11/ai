#! /usr/bin/python3

import random, sys

UsingDebuggingArgs = False
DebuggingArgs = {'action':'move','outputfile':'simple.txt','result_prefix':'ANSWER:','ply':'1','play':'o','cputime':'1','board':'-ooooo--xxxxxox---ooxoxo---ooxxo---ooox-------------------------',}


Author = 'Max'
Title = 'It Better Work...'

Blank = '-'
Board = '';
Player = '';

Directions = [
    [0,1], #E
    [1,1], #NE
    [1,0], #N
    [1,-1], #NW
    [0,-1], #W
    [-1,-1], #SW
    [-1,0], #S
    [-1,1]] #SE

Edges = [1,2,3,4,5,6,15,23,31,39,47,55,8,16,24,32,40,48,57,58,59,60,61,62]
Corners = [0,7,56,63]

# ----------------------------- main -----------------------------------
def main():
    global Board, Player

    # get the arguments from either the command-line or the debugging ones above
    if UsingDebuggingArgs:
        args = DebuggingArgs
    else:
        args = {}
        for arg in sys.argv:
            if '=' in arg:
                key,value = arg.split('=')
                args[key] = value

    if args['action'] == 'id':
        Report(args,'title='+Title+'\nauthor='+Author+'\n')
        return

    if args['action'] == 'move':
        # choose a random valid move
        # create a list of the possible moves
        Board = args['board']
        Player = args['play']
        MaxPly = int(args['ply'])

        if MaxPly == 1:
            move = bestMove(Board,Player)
            print (GetPossibilities(Board,Player))
            print (bestMove(Board,Player))
            #print (move)
            Report(args,'move='+str(move)+'\nply=1\n')
        elif MaxPly == 2:
            move = maxDifference(Board, Player)
            Report(args,'move='+str(move)+'\nply=2\n')
        else:
            poss_list = GetPossibilities(Board,Player)
            #print(poss_list)
            if len(poss_list) > 0:
                a_random_valid_pos = random.choice(poss_list)
                Report(args,'move='+str(a_random_valid_pos)+'\nply=0\n')
            else:
                Report(args,'move=-1\nply=0\n')
            return

# ------------------------------------- Report ---------------------------------
def Report(the_args, the_result):
    filename = the_args['outputfile']
    prefix = the_args['result_prefix']
    f=open(filename,'a')
    f.write(prefix+'\n'+the_result)
    f.close()
    print ('Done')

# ------------------------------ RowCol2Pos ----------------------------------
def RowCol2Pos(row,col):
    return row * 8 + col

# ------------------------------ Pos2RowCol ------------------------------------
def Pos2RowCol(pos):
    return (pos//8,pos%8)

# ---------------------------------- IsValidPos ---------------------------------
def IsValidPos(row,col):
    if row < 0 or row >= 8 or col < 0 or col >= 8:
        return False
    return True

# --------------------------------- GetPlayedRay ---------------------------------
def GetPlayedRay(aboard,pos,adir):
    '''return the sequence of played positions starting from pos in direction adir.  Stop at bank or edge'''
    ray_list = []
    row,col = Pos2RowCol(pos)
    row_delta,col_delta = adir
    for i in range(1,8):
        row2 = row + i*row_delta
        col2 = col + i*col_delta
        if not IsValidPos(row2,col2):
            break
        pos2 = RowCol2Pos(row2,col2)
        if aboard[pos2] != Blank:
            ray_list.append(pos2)
        else:
            break
    #print(ray_list)
    return ray_list

# ----------------------------------- Other ---------------------------------------
def Other(this,others):
    if this == others[0]:
        return others[1]
    return others[0]

# ------------------------------------ GetPossibilities ----------------------------
def GetPossibilities(aboard,player):
    poss_list = []
    opponent = Other(player,['x','o'])
    for pos in range(64):
        found = False
        if aboard[pos] == Blank:
            for adir in Directions:
                ray = GetPlayedRay(aboard,pos,adir)
                if len(ray) > 0 and aboard[ray[0]] == opponent:
                    for i in range(1,len(ray)):
                        if aboard[ray[i]] == player:
                            poss_list.append(pos)
                            #print('player',player,'pos',pos,'ray',ray)
                            found = True
                            break
                    if found:
                        break
    return poss_list

def TilesFlipped(aboard,pos,player):
    FlippedList = []
    opponent = Other(player,['x','o'])
    for dir in Directions:
        #print ("Direction: " + str(dir))
        if len(GetPlayedRay(aboard,pos,dir)) != 0:
            playedPos = GetPlayedRay(aboard,pos,dir)
            #print ("playedPos: " + str(playedPos))
            index = 0
            tempList = []
            while index < len(playedPos) and aboard[playedPos[index]] == opponent:
                if index == len(playedPos) - 1:
                    tempList = []
                else:
                    tempList.append(playedPos[index])
                index += 1
                #print ("tempList: " + str(tempList))
            FlippedList += tempList
    return FlippedList

def MostTilesFlipped(aboard,player):
    possibleMoves = GetPossibilities(aboard,player)
    if len(possibleMoves) > 0:
        lenList = []
        for move in possibleMoves:
            total = len(TilesFlipped(aboard,move,player))
            if move in Edges:
                total += 2
            elif move in Corners:
                total += 5
            lenList.append(total)
        mostFlipped = max(lenList)
        return mostFlipped
    else:
        return 0

def bestMove(aboard,player):
    possibleMoves = GetPossibilities(aboard,player)
    lenList = []
    for move in possibleMoves:
        total = len(TilesFlipped(aboard,move,player))
        if move in Edges:
            total += 2
        elif move in Corners:
            total += 5
        lenList.append(total)
    mostFlipped = max(lenList)
    return possibleMoves[lenList.index(mostFlipped)]

def newBoard(curBoard,pos,player):
    FlippedList = TilesFlipped(curBoard,pos,player)
    newBoard = curBoard[:pos] + player + curBoard[pos + 1:]
    for tile in FlippedList:
        newBoard = newBoard[:tile] + player + newBoard[tile+1:]
    return newBoard
    #eat up some apples eat the melons now theres nothing on your plaaate uhhuhuhuhuhuh

def maxDifference(aboard,player):
    possiblePlayerMoves = GetPossibilities(aboard,player)
    opponent = Other(player,['x','o'])
    differences = []
    for move in possiblePlayerMoves:
        nb = newBoard(aboard,move,player)
        mostOppFlip = MostTilesFlipped(nb,opponent)
        differences.append(len(TilesFlipped(aboard,move,player)) - mostOppFlip)
    return possiblePlayerMoves[differences.index(max(differences))]

main()
