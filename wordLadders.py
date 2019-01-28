#! /usr/bin/python3

import sys, heapq

fin = open("dictall.txt", 'r')
dict = fin.read().split('\n')


input = open(sys.argv[1], 'r').read().strip().split('\n')
wlen = len(input[0])
mwords = [x for x in dict if len(x) == wlen]
out = open(sys.argv[2], 'w')
d = {}

for word in mwords:
    nb = []
    counter = 0
    for pos in range(len(word)):
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c != word[pos]:
                nword = word[:pos] + c + word[pos+1:]
                if nword in mwords:
                    nb.append[nword]
    d[word] = nb

unexplored = {}
frontier = []
#frontier1 = PQueue()
explored = {}
    #out.write(d)
    #out.write(str(word) + "," + str(counter) +"\n")
