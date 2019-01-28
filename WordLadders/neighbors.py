#! /usr/bin/python3

import sys

fin = open("dictall.txt", 'r')
dict = fin.read().split('\n')
input = open(sys.argv[1], 'r').read().strip().split('\n')
wlen = len(input[1])
mwords = [x for x in dict if len(x) == wlen]
out = open(sys.argv[2], 'w')
d = {}
# for word in mwords:
#     nb = []
#     counter = 0
#     for pos in range(len(word)):
#         for c in "abcdefghijklmnopqrstuvwxyz":
#             if c != word[pos]:
#                 nword = word[:pos] + c + word[pos:]
#                 if nword in mwords:
#                     nb.append[nword]
#                     counter += 1
#                 out.write(str(word) + "," + str(counter) +"\n")
#     d[word] = nb
#     #out.write(d)
#     #out.write(str(word) + "," + str(counter) +"\n")

for word in input:
    dlist = []
    counter = 0
    for term in mwords:
        word = len(word)
        term = len(term)
        if word == term: #if the words are equal length
            diff = 0
            for i in range(len(word)):
                if word[i] != term[i]: #check for # of diff characters
                    diff += 1
            if diff == 1:
                #print(word, term)
                counter += 1
                dlist.append(term)
        if word == wlen:
            d[word] = dlist #creates dictionary
#out.write(str(d)) #writes out dictionary
    out.write(str(word) + "," + str(counter) +"\n") #output
