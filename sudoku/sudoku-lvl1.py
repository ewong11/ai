#! /usr/bin/python

import sys

# Opening the read and write files
boardFile = open(sys.argv[1],'r')
inputLines = boardFile.read().split('\n')
solvedOutput = open(sys.argv[2],'w')
boardName = sys.argv[3]

#keeps track of backtracks
backtrack = 0

#instantiates a stack for later use
stack = []

# List of "cliques" for every row, column, and cell
Cliques = [
# Rows
[0,1,2,3,4,5,6,7,8],
[9,10,11,12,13,14,15,16,17],
[18,19,20,21,22,23,24,25,26],
[27,28,29,30,31,32,33,34,35],
[36,37,38,39,40,41,42,43,44],
[45,46,47,48,49,50,51,52,53],
[54,55,56,57,58,59,60,61,62],
[63,64,65,66,67,68,69,70,71],
[72,73,74,75,76,77,78,79,80],
# Columns
[0,9,18,27,36,45,54,63,72],
[1,10,19,28,37,46,55,64,73],
[2,11,20,29,38,47,56,65,74],
[3,12,21,30,39,48,57,66,75],
[4,13,22,31,40,49,58,67,76],
[5,14,23,32,41,50,59,68,77],
[6,15,24,33,42,51,60,69,78],
[7,16,25,34,43,52,61,70,79],
[8,17,26,35,44,53,62,71,80],
# Cells
[0,1,2,9,10,11,18,19,20],
[3,4,5,12,13,14,21,22,23],
[6,7,8,15,16,17,24,25,26],
[27,28,29,36,37,38,45,46,47],
[30,31,32,39,40,41,48,49,50],
[33,34,35,42,43,44,51,52,53],
[54,55,56,63,64,65,72,73,74],
[57,58,59,66,67,68,75,76,77],
[60,61,62,69,70,71,78,79,80]]

# Creating a dictionary of the "neighbors" of each position in the board
neighborDict = {}
for pos in range(81):
    neighborList = []
    for clique in Cliques:
        if pos in clique:
            for i in clique:
                # Puts every UNIQUE clique neighbor into the list (no duplicates allowed)
                if i != pos and i not in neighborList:
                    neighborList.append(i)
    neighborDict[pos] = neighborList

# Finding the puzzle in the input file and putting into a list
puzzleStr = ""
index = 0
while inputLines[index] != boardName:
    index += 1
# When the name of the puzzle is found:
for i in range(index + 1,index + 10):
    # Take the next 9 lines in the file and concatenate into one string
    puzzleStr += inputLines[i]
    # Adding a comma when at the end of the line (except for the 9th line)
    if (i - index) != 10:
        puzzleStr += ','
# Once all of the lines are in a string, make a list of each pos by splitting on commas
puzzleList = puzzleStr.split(',')
stack.append([[], list(puzzleList)])

# Function: neighborValues(pos,state)
# Parameters:
#   pos - Position on the sudoku board
#   state - state of the board currently being used
# Returns the values (from 1 to 9) already used by the neighbors of pos at certain state
# Returns as a set to remove duplicates and speed up time to check for presence of value
def neighborValues(pos):
    valueList = []
    positions = neighborDict[pos]
    for neighbor in positions:
        valueList.append(puzzleList[neighbor]) #adds value of each position to its corresponding postion
    valueSet = set(valueList)
    if '_' in valueSet:
        valueSet.remove('_')     # Remove the '_' because it's not a numerical value of one of the neighbors
    return valueSet

#-----------------------------------------------------------SMARTNESS--------------------------------------------------------------------#
# LOOKS FOR FORCES AFTER EACH GUESS
# FINDS BEST INDEX TO GUESS, BASED ON LENGTH OF ITS NEIGHBORS

#looks through entire board for forces and puts number there
def force():
    global puzzleList #state of puzzle

    i = 0
    while i < 81:
        neighbors = neighborValues(i)
        if puzzleList[i] == '_':
            if len(neighbors) == 8:
                for n in range(1,10):
                    stri = str(n)
                    if stri not in neighbors:
                        puzzleList[i] = stri
                        break
                i = 0
            else:
                i += 1
        else:
            i += 1
def force2():
    global puzzleList #state of puzzle
    i = 0
    while i < 81:
        if puzzleList[i] == '_':
            neighbors = neighborValues(i)
            if len(neighbors) == 8:
                for n in range(1,10):
                    stri = str(n)
                    if stri not in neighbors:
                        puzzleList[i] = stri
                        break
                i = 0
            else:
                i += 1
        else:
            i += 1

#finds the empty space with the longest number of neighbors
#that position has the least number of places to choose
def betterGuess():
    #global puzzleList
    neighborLen = 0
    i = 0
    retGuess = 0
    while i < 81:
        if puzzleList[i] == '_':
            if len(neighborValues(i)) > neighborLen:
                retGuess = i
                neighborLen = len(neighborValues(i))
        i += 1
    return retGuess

def solve(index):
    global puzzleList
    global backtrack
    global stack

    neighbors = neighborValues(index)
    #from naive solver
    if len(neighbors) + len(stack[len(stack) - 1][0]) < 9:
        for i in range(1,10):
            stri = str(i)
            if stri not in neighbors and stri not in stack[len(stack) - 1][0]:
                stack[len(stack) - 1][0].append(stri)
                puzzleList[index] = stri
                stack.append([[],list(puzzleList)]) # Add the new guess to the top of the stack
                break
    # A CONTRADICTION was found after all guesses are tried
    else:
        # Pop contradction, restore old state
        stack.pop()
        backtrack += 1
        puzzleList = stack[len(stack) - 1][1]

def smart():
    # keep guessing until no more empty space
    while '_' in puzzleList:
        force2()
        nextBlank = betterGuess()
        solve(nextBlank)
    print (backtrack)

    # Changing the name in output file to say "solved" instead of "unsolved"
    nameList = boardName.split(',')
    nameList[2] = "solved"
    solvedOutput.write(','.join(nameList) + '\n')
    # Writing out the solution as a 9x9 box instead of one long line
    for i in range(9):
        solvedOutput.write(','.join(puzzleList[i*9:i*9+9]) + '\n')

smart()
