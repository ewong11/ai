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


class Node():
    def __init__(self, data):
        self.data=data
        self.parent=None
        self.Lchild = None
        self.Rchild = None
        self.prev_last = None
    #def setLChild(self, data):
    #    self.LChild = data
    #def setRChild(self, data):
    #    self.RChild = data
    #def setParent(self, data):
    #    self.parent = data
    def value(self):
        return self.data
    def __str__(self):
        return str(self.data)

class minHeap():
    def __init__(self):
        self.root = None
        self.size = 0
        self.current = None
        self.last = None
    def swap(self, a, b):
        temp = a
        a.data = b
        b.data = a
    def push(self, data):
        anode = Node(data)
        if size == 0:
            self.root = anode
        else:
            self.last = anode
        size += 1
