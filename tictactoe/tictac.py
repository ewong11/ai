Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

NumGames = 0
NumBoards = 0
Boards = set()
AllBoards = {}

def GamesAndBoards(starting_board):
    global NumBoards, Boards, NumGames

    NumGames = 0
    Boards = set()
    TryAllMoves(starting_board)
    NumBoards = len(Boards)

def TryAllMoves(board):
    global NumGames

    Boards.add(board)

    # Is this the final board in a game?
    if IsWin(board) or board.count('_') == 0:
        NumGames += 1
        return

    # Find all children of this board
    move = 'x' if board.count('o') == board.count('x') else 'o'
    for pos in range(9):
        if board[pos] == '_':
            new_board = board[:pos] + move + board[pos+1:]
            TryAllMoves(new_board)

def IsWin(board):
    for awin in Wins:
        if board[awin[0]] == board[awin[1]] and board[awin[1]] == board[awin[2]] and board[awin[0]] != '_':
            return True
    return False

def winner(board):
    if IsWin(board):
        for clique in Wins:
            pos0 = clique[0]
            pos1 = clique[1]
            pos2 = clique[2]
            if board[pos0] != '_' and board[pos0] == board[pos1] == board[pos2]:
                return board[pos0]

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

def CreateAllBoards(layout, parent):
    # recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary
    newNode = BoardNode(layout)
    newNode.parents.append(parent)
    if winner(layout):
        newNode.endState = winner(layout)
    else:
        move = 'x' if layout.count('o') == layout.count('x') else 'o'
        for pos in range(9):
            if layout[pos] == '_':
                new_board = layout[:pos] + move + layout[pos+1:]
                if new_board not in AllBoards:
                    CreateAllBoards(new_board, layout)
                newNode.children.append(new_board)
    AllBoards[layout] = newNode


CreateAllBoards('_________', None)
print len(AllBoards)
sum = 0
for elem in AllBoards:
    sum += len(AllBoards[elem].children)
print sum
#print (NumBoards, NumGames)
