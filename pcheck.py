#! /usr/bin/python
import sys
def OrdinaryComparison(a,b):
  if a < b: return -1
  if a == b: return 0
  else: return 1
def my_cmp(a,b):
  if len(a) < len(b): return -1
  if len(a) == len(b): return 0
  return 1


class Pqueue():

  def __init__(self, comparator = OrdinaryComparison):
    self.cmpfunc = comparator
    self.q = [None]

  def swap(self, a, b):
    temp = self.q[a]
    tempb = self.q[b]
    self.q[a] = tempb
    self.q[b] = temp


  def push(self,data):
    self.q.append(data)
    i = len(self.q)-1
    while i > 0 and self.cmpfunc(data, self.q[i//2]) == -1:
        self.swap(i, i//2)
        i = i//2

  def pop(self):
    if len(self.q) == 1:
      return None
    retVal = self.q[1]
    i = 1
    #print "before pop: ", len(self.q)
    self.swap(1, len(self.q)-1)
    self.q.pop(len(self.q)-1)
    #print "after pop" , len(self.q)
    while self.findChild(i) != -1 and self.cmpfunc(self.q[i], self.q[self.findChild(i)]) == 1:
          temp = self.findChild(i)
          self.swap(i, self.findChild(i))
          i = temp
    return retVal

  def findChild(self, index):
    if 2 * index >= len(self.q): #no child
      return -1
    elif 2 * index + 1 >= len(self.q):
      return 2 * index
    else:
      if self.cmpfunc(self.q[2*index], self.q[2*index+1]) == -1:
        return 2*index
      else:
        return 2*index + 1


  def peek(self):
    if len(self.q) == 1:
      return None
    return self.q[1]

  def tolist(self):
    retlist = []
    while len(self.q) > 1:
        retlist.append(self.pop())
    return retlist

    #for i in range(len(self.q)):
        #retlist.append(self.q.pop())
    #  if self.q[i] != None:
    #    retlist.append(self.q[i])
    #    self.q[i] = None
    #return retlist

  def toString(self):
    print(self.q)

def my_cmp(a,b):
   if len(a) < len(b): return -1
   if len(a) == len(b): return 0
   return 1

f = open(sys.argv[1],'r')
sc = f.read().split('\n')
j = open(sys.argv[2],'w')
out = Pqueue()
for line in sc:
    c = line.split(',')
    command = c[0]
    if command == "push":
        for num in c[1:]:
            out.push(int(num))
    elif command == "peek":
        j.write(str(out.peek()))
        j.write('\n')
    elif command == "pop":
        j.write(str(out.pop()))
        j.write('\n')
    elif command == "tolist":
        j.write(str(out.tolist()))
        j.write('\n')
