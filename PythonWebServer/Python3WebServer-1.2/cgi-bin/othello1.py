#! /usr/bin/python3

import random, sys

UsingDebuggingArgs = True
DebuggingArgs = {'action':'move','outputfile':'simple.txt','result_prefix':'ANSWER:','ply':'2','play':'x','cputime':'1','board':'--------------------ox-----xo-----------------------------------',}


Author = ''
Title = ''

Blank = '-'
Board = '';
Player = '';

Directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]

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
            #print(findBest(Board, Player))
            move = findBest(Board, Player)
            Report(args,'move='+str(move)+'\nply=1\n')
        elif MaxPly == 2:
            #print(second(Board,Player))
            move = find2ply(Board, Player)
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

def findBest(aboard, player, type):
    to_check = GetPossibilities(aboard,player)
    bestMove = 0 #tracks position of 'bestMove'
    bestMoveCount = 0 #tracks highest # of pieces captured (by bestMove)
    allpositions = [] #list of all positions captured
    opponent = Other(player,['x','o'])
    for pos in to_check:
        count = 0
        for direc in Directions: #check all the directions and add up the amount of pieces you'll capture
            state = GetPlayedRay(aboard,pos,direc) #returns the list of values that have been played in direction direc from position
            sub = 0
            for i in state:
                if aboard[i] == opponent:
                    sub += 1
                elif aboard[i] != player:
                    count += sub
        #print("pos: " + str(pos) + " count: " + str(count))
        if count > bestMoveCount: #replace with new best move, if there is one (based on pieces captured)
            bestMove = pos
            bestMoveCount = count
    return bestMove

def flips(aboard,pos, player):
	opponent = Other(player,['x','o'])
	ray = []
    lastOpponent_i = 0
	turnovers = []
	for idir < len(Directions):
		ray = GetPlayedRay(aboard,pos,Directions[idir]);
		if (ray.length == 0): continue
		if (aboard[ray[0]] != opponent): continue
		lastOpponent_i = -1;
		for (var i = 1; i < ray.length; ++i) {
			c = aboard[ray[i]]
			if (c == player):
				lastOpponent_i = i-1;
				break
		if (lastOpponent_i== -1):
			continue
		for (var i = 0; i <= lastOpponent_i; ++i):
			turnovers.push(ray[i])
	return turnovers



def find2ply(aboard, player):
    opponent = Other(player,['x','o'])
    check = GetPossibilities(aboard,player) #checks all our possibilities
    bestMove = None
    listBest = []
    f = []
    finalDiff = 0
    for pos in check: #for each of our possible moves
        copy = list(aboard)
        f = flips(copy, pos, player)
        for flip in usergain:
            copy[flip] = player
            copy[pos] = player
        usergain = len(f)

        oppBest = findBest(copy, opponent)
        oppFlipped = len(flips(copy, oppBest, opponent))
        diff = usergain - oppFlipped

        if diff > finalDiff:
            finalDiff = diff
            bestMove = pos
    return bestMove


main()
