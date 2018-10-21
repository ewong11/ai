#! /usr/bin/python3

import sys

fin = open("dictall.txt", 'r')
dict = fin.read().split('\n')
input = open(sys.argv[1], 'r').read().strip().split('\n')
wlen = 4
mwords = [x for x in dict if len(x) == wlen]
#sc = input.read().split('\n')
input = open(sys.argv[1], 'r').read().strip().split('\n')
#wlen = 4
#mwords = set([x for x in input if len(x) == wlen])
#sc = input.read().split('\n')
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
    #print(word)
    dlist = []
    counter = 0
    for term in mwords:
        a = len(word)
        b = len(term)
        if b == a:
            diff = 0
            for i in range(len(word)):
                if word[i] != term[i]: #check for # of diff characters
                    diff += 1
            if diff == 1:
                #print(word, term)
                counter += 1
                dlist.append(term)
        if a == 4:
            d[word] = dlist
#out.write(str(d))
    out.write(str(word) + "," + str(counter) +"\n")
