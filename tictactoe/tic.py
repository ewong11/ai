#! /usr/bin/python

import sys

board = "________"
stack = []

solutions = [[0,1,2],[3,4,5],[6,7,8], #rows
            [0,3,6],[1,4,7],[2,5,8], #columns
            [0,4,8],[2,4,6]] #diagonals

def isSolved(board):
        for clique in solutions:
            pos0 = clique[0]
            pos1 = clique[1]
            pos2 = clique[2]
            if board[pos0] == board[pos1] == board[pos2]:
                return True
        return False
