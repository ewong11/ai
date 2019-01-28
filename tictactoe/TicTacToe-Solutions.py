#! usr/bin/python3

import sys

# Counting the total number of possible games and resulting game boards in the Tic-Tac-Toe solution set

# Counter for the total number of possible games of Tic-Tac-Toe
# Games end when one side wins or when the board is filled (after 9 moves)
numOfGames = 0

numOfXWins = 0
numOfOWins = 0
numOfDraws = 0

# Counter for the total number of distinct boards produced by the games
# Different game paths can result in the same exact
boardConfigs = 0
prevConfigs = set()

# State of the board
curBoard = "_________"

# Stack to contain the last state of the board and the moves already explored
stack = []
stack.append([[],curBoard])

# Indices that must be the same symbol in order to win the game
solutions = [[0,1,2],[3,4,5],[6,7,8], #rows
            [0,3,6],[1,4,7],[2,5,8], #columns
            [0,4,8],[2,4,6]] #diagonals

AllBoards = {}
# Method isSovled(board)
# Parameters:
#   board - current state of the Tic-Tac-Toe board as a string
# Returns true if either side wins with the current board (three x's or three o'x in a row)
def isSolved(board):
        for clique in solutions:
            pos0 = clique[0]
            pos1 = clique[1]
            pos2 = clique[2]
            if curBoard[pos0] != '_' and curBoard[pos0] == curBoard[pos1] == curBoard[pos2]:
                return True
        return False

def winner(board):
    if isSolved(board):
        for clique in solutions:
            pos0 = clique[0]
            pos1 = clique[1]
            pos2 = clique[2]
            if curBoard[pos0] != '_' and curBoard[pos0] == curBoard[pos1] == curBoard[pos2]:
                return curBoard[pos0]

def gameOver(board):
    full = True
    for element in curBoard:
        if element == '_':
            full = False
    if full or isSolved(board):
        return True
    return False

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endState = None # if this is a terminal board, endState == 'x' or 'o' for wins, of 'd' for draw, else None
        self.parents = [] # all layouts that can lead to this one, by one move
        self.children = [] # all layouts that can be reached with a single move

    def print_me(self):
        print ('layout:',self.layout, 'endState:',self.endState)
        print ('parents:',self.parents)
        print ('children:',self.children)


def CreateAllBoards(layout,parent):
    global curBoard
    global numOfGames
    global boardConfigs
    global prevConfigs
    global numOfDraws
    global numOfXWins
    global numOfOWins

    newNode = BoardNode(layout)

    if curBoard.count('_') % 2 == 0:
        nextMove = 'o'
    else:
        nextMove = 'x'

    if gameOver(curBoard) or curBoard.count('_') == len(stack[len(stack) - 1][0]):
        if gameOver(curBoard):
            numOfGames += 1
            if isSolved(curBoard):
                if winner(curBoard) == 'x':
                    newNode.endState = 'x'
                    numOfXWins += 1
                elif winner(curBoard) == 'o':
                    newNode.endState = 'o'
                    numOfOWins += 1
            else:
                numOfDraws += 1
        newNode.parents = prevConfigs
        if curBoard not in prevConfigs:
            boardConfigs += 1
            prevConfigs.add(curBoard)
        stack.pop()
        # print ("\n\n\n POP \n\n\n")
        if len(stack) > 0:
            curBoard = stack[len(stack) - 1][1]
    else:
        index = 0
        while index < 9:
            if curBoard[index] == '_':
                newBoard = curBoard[0:index] + nextMove + curBoard[index + 1:]
                newNode.children.append(newBoard)
            index += 1
        index = 0
        while index < 9:
            if curBoard[index] == '_' and index not in stack[len(stack) - 1][0]:
                newBoard = curBoard[0:index] + nextMove + curBoard[index + 1:]
                newNode.children.append(newBoard)
                stack[len(stack) - 1][0].append(index)
                stack.append([[],newBoard])
                curBoard = newBoard
                break
            else:
                index += 1
    AllBoards[curBoard] = newNode
    # print (curBoard)
    # print (stack)
    # print ('\n')



def generateGames():
    #while len(stack) != 0:
        #CreateAllBoards()
    while len(stack) != 0:
        CreateAllBoards(len(stack[len(stack) - 1][0]), None)
    #print(len(AllBoards))
    print(numOfGames)
    print(boardConfigs)
    print (numOfDraws)
    print (numOfXWins)
    print (numOfOWins)

generateGames()
sum = 0
for elem in AllBoards:
    sum += len(AllBoards[elem].children)
print sum



# print(gameOver("oxooxxxox"))
# print(gameOver("oxoxoxxoo"))
# print(gameOver("oxooxx_ox"))
