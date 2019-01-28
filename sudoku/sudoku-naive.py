#! /usr/bin/python

import sys

# Opening the read and write files
boardFile = open(sys.argv[1],'r')
inputLines = boardFile.read().split('\n')
solvedOutput = open(sys.argv[2],'w')
boardName = sys.argv[3]

# Counter to check how many backtracks are necesary to solve the puzzle
# AKA to see how bad the naive solver method is
backtrack = 0

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

# Naive Solver uses a stack, guessing, and backtracking to incrementally fill in the board until solved
def naiveSolver():
    stack = []
    # Add the original state to the stack
    stack.append([[],puzzleList])

    # Function: guess(index)
    # Parameters:
    # index - Index at which a guess is being made
    # Makes a guess for possible value at index
    def guess(index):
        global puzzleList
        global backtrack

        # Get the values of the neighbors at index
        neighVal = neighborValues(index)
        newState = list(puzzleList)

        # FORCED STATE
        # If 8 out of 9 values were used, then the the value at index is FORCED to be the remaining number
        if len(neighVal) == 8:
            # newState[index] = 45 - sum(neighVal)
            for n in range(1,10):
                stri = str(n)
                if stri not in neighVal:
                    newState[index] = stri
                    puzzleList = newState # Update the current puzzle state
                    break

        # GUESSING STATE
        # If the neighbors have used less than 8 values and the remaining values haven't been guessed yet, then another guess needs to be made
        elif len(stack[len(stack) - 1][0]) + len(neighVal) != 9:
            for i in range(1,10):
                stri = str(i)
                # Find the value that is not used by the neighbors and has not been guessed yet
                if stri not in neighVal and stri not in stack[len(stack) - 1][0]:
                    stack[len(stack) - 1][0].append(stri)
                    newState[index] = stri
                    puzzleList = newState # Update the current state
                    stack.append([[],puzzleList]) # Add the new guess to the top of the stack
                    break

        # A CONTRADICTION was found after all guesses
        else:
            # Pop the contradction off of the stack
            # Induces backtracking by restoring the last state before guessing
            stack.pop()
            backtrack += 1
            puzzleList = stack[len(stack) - 1][1]

    # keep guessing until no more empty space
    while '_' in puzzleList:
        # Find the position of the next empty space (where there is an '_')
        nextBlank = puzzleList.index('_')
        #print (nextBlank)
        guess(nextBlank)
    print (backtrack)

    # Changing the name in output file to say "solved" instead of "unsolved"
    nameList = boardName.split(',')
    nameList[2] = "solved"
    solvedOutput.write(','.join(nameList) + '\n')
    # Writing out the solution as a 9x9 box instead of one long line
    for i in range(9):
        solvedOutput.write(','.join(puzzleList[i*9:i*9+9]) + '\n')

naiveSolver()
