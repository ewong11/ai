#! /usr/bin/python3

import sys
import heapq

fin = open("dictall.txt", 'r')
dict = fin.read().split('\n')

input = open(sys.argv[1], 'r').read().strip().split('\n')
wlen = len(input[0].split(',')[0])
mwords = set([x for x in dict if len(x) == wlen])
out = open(sys.argv[2], 'w')
d = {}

for word in mwords:
    nb = []
    for pos in range(len(word)):
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c != word[pos]:
                nword = word[:pos] + c + word[pos+1:]
                if nword in mwords:
                    nb.append(nword)
    d[word] = nb #creates a dicionary of certain length


class Node():
    def __init__(self, totalcost, word, pathTo):
        self.word = word
        self.cost = totalcost
        self.path = pathTo
    # def getCost(self):
    #     return self.cost
    # def getWord(self):
    #     return self.word
    # def getPath(self):
    #     return self.path
    def toTuple(self):
        return (self.cost, self.word, self.path) #used for compaison - cost is first

class WordLadder():
    def __init__(self,first,target):
        self.ux = set()
        self.fr = []
        #heapq.heapify(self.fr)
        self.x = set()
        self.first = first
        self.target = target
        self.count = 0
        initNode = Node(self.estimate(self.first),self.first,[]) #initialize first node and push into frontier
        heapq.heappush(self.fr,initNode.toTuple())

    #add unexplored list of all words of certain length
    def populate(self):
        for word in mwords:
            #nodeword = Node(word,0,[])
            self.ux.add(word)

    #estimate distance to target node by counting # of different letters
    def estimate(self,word):
        diff = 0
        for a in range(len(self.first)):
            if word[a] != self.target[a]:
                diff += 1
        return diff

    def processFrontier(self):
        currentNode = heapq.heappop(self.fr) #will pop out top node
        curWord = currentNode[1]
        self.x.add(curWord)

        #creates a new path to currentNode
        updatePath = list(currentNode[2])
        updatePath.append(curWord)

        #looks into dictionary to find all neighbors of given word
        neighbors = d[curWord]

        for neighbor in neighbors:
            #checks if neighbor has been explored
            if neighbor not in self.x:
                #if neighbor in self.ux:
                #    self.ux.remove(neighbor)
                newNode = Node(currentNode[0] + self.estimate(curWord) - self.estimate(neighbor) - 1, neighbor, updatePath)
                heapq.heappush(self.fr,newNode.toTuple()) #push onto hoop and make sure most efficient path is on top
        return currentNode

for pair in input:
    term = pair.split(',')
    ladder = WordLadder(term[0], term[1])
    ladder.populate() #populates with nodes of words in mwords
    #print ladder.ux
    while term[1] not in ladder.x:
        if len(ladder.fr) == 0:
            finalPath = list(term)
            break
        nextWord = ladder.processFrontier()
        #print(nextWord)
        finalPath = list(nextWord[2])
        finalPath.append(nextWord[1])

    out.write(str(len(finalPath)))
    out.write(",".join(finalPath))
    out.write("\n")
