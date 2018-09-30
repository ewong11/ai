#! /usr/bin/python3

import sys

f = open(sys.argv[1],'r')
sc = f.read().split('\n')
j = open(sys.argv[2],'w')
for i in sc:
    tempList = i.split(',')
    sum = 0
    noNum = True
    for e in tempList:
        noWS = e.strip()
        if noWS.isdigit():
            noNum = False
            sum += int(e)
    if not noNum and sum > 0:
        j.write(str(sum))
        j.write('\n')
