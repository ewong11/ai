#! /usr/bin/python3

import random, sys

UsingDebuggingArgs = False
DebuggingArgs = {'action':'move','outputfile':'simple.txt','result_prefix':'ANSWER:','ply':'2','play':'x','cputime':'1','board':'---o-xxo----x-x--oxxooxo--xxoxooxxxoxo-o-xox--------------------',}


Author = 'Eric'
Title = 'Please Work'

Blank = '-'
Board = '';
Player = '';

Directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
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
            print(findBest(Board, Player, 'best'))
            move = findBest(Board, Player, 'best')
            Report(args,'move='+str(move)+'\nply=1\n')
        elif MaxPly == 2:
            print(second(Board,Player))
            move = second(Board, Player)
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
#find best (ply=1)
def findBest(aboard, player, type):
    #find first ply
    to_check = GetPossibilities(aboard,player)
    #print(to_check)
    bestMove = 0 #tracks position of 'bestMove'
    bestMoveCount = 0 #tracks highest # of pieces captured (by bestMove)
    opponent = Other(player,['x','o'])
    listBest = []
    for pos in to_check:
        #print("position: " + str(pos))
        count = 0
        allpositions = [] #list of all positions captured
        for direc in Directions: #check all the directions and add up the amount of pieces you'll capture
            state = GetPlayedRay(aboard,pos,direc) #returns the list of values that have been played in direction direc from position
            #print("state: " + str(state))
            tempCount = 0
            for n in state:
                #counts all of the opponents between position and the next 'player' piece in a certain direction
                #this is supposed to count the pieces captured
                #print("n: " + str(n))
                #print(aboard[n])
                if aboard[n] == opponent:
                    tempCount += 1
                    allpositions.append(pos)
                    #print("tempcount: " + str(tempCount))
                    #print("allpos: " + str(pos))
                elif (aboard[n] == player): #if you hit a 'player,' break
                    count += tempCount
                    tempCount = 0
        #print("pos: " + str(pos) + " count: " + str(count))
        #print("pos: " + str(pos) + " count: " + str(count))
        if pos in Edges:
            count += 2
        if pos in Corners:
            count += 5
        if count > bestMoveCount: #replace with new best move, if there is one (based on pieces captured)
            bestMove = pos
            bestMoveCount = count
            listBest = []
            listBest.append(pos)
        elif count == bestMoveCount:
            listBest.append(pos)
    if len(listBest) != 0:
        bestMove = random.choice(listBest)
    if type == 'best':
        #print("best move: " + str(bestMove) )
        return bestMove
    elif type == 'count':
        return bestMoveCount
    elif type == 'positions':
        return allpositions

def whatToFlip(aboard, player, pos):
    flipList = []
    opponent = Other(player, ['x','o'])
    for d in Directions:
        played = GetPlayedRay(aboard, pos, d)
        i = 0
        tempList = []
        while i < len(played) and aboard[played[i]] == opponent:
            if i == len(played) - 1:
                tempList = []
            else:
                tempList.append(played[i])
            i += 1
        flipList += tempList
    return flipList


def second(aboard, player):
    opponent = Other(player,['x','o'])
    check = GetPossibilities(aboard,player) #checks all our possibilities
    bestCount = None
    bestMove = None
    bestDiff = None
    listBest = []
    for pos in check: #for each of our possible moves
        #print(copy[pos])
        #print(player)
        copy = list(aboard)
        #create a copy of board with move inserted
        #print("aboard: "+ str(aboard))
        #print('copy' + str(copy))
        #print(copy[0])
        #uses copy (stimulates a turn) and use that board for opponent
        changedPositions = whatToFlip(copy, player, pos)
        copy[pos] = player
        for p in changedPositions:
            copy[p] = player
        opponentCount = findBest(copy, opponent, 'count') #will find the move with the highest # of pieces captured by opponent
                                          #this will check each of the opponents possible move
        diff = len(changedPositions) - opponentCount
        # print("opponent count: " + str(count) + "pos: " + str(pos)) #test
        # if bestCount == None:
        #     bestCount = count
        #     bestMove = pos
        # elif count < bestCount: #if that 'max' move by opponent is less than her prev max, replace
        #     print("count: " + str(count) + " current: " + str(bestCount))
        #     bestCount = count #update bestCount
        #     bestMove = pos #change our best move to the one that gives our opponent the least advantage
        #     listBest = []
        # elif count == bestCount:
        #     listBest.append(pos)
        # if pos in Edges:
        #     diff += 2
        # if pos in Corners:
        #     diff += 5
        if bestDiff == None:
            bestDiff = diff
            bestMove = pos
            listBest.append(pos)
        elif diff > bestDiff:
            bestDiff = diff
            bestMove = pos
            listBest = []
            listBest.append(pos)
        elif bestDiff == diff:
            listBest.append(pos)
    if len(listBest) != 0:
        bestMove = random.choice(listBest)
    #if bestMove == None:
    #    bestMove = random.choice(check)
    print("bestMove: " + str(bestMove))
    return bestMove

main()
