def OrdinaryComparison(a,b):
  if a < b: return -1
  if a == b: return 0
  return 1
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
    self.q[a] = self.q[b]
    self.q[b] = temp
    
  def push(self,data):
    self.q.append(data)
    i = len(self.q)-1

    while i > 1 and self.cmpfunc(data, self.q[i//2]) == -1:
        self.swap(i, i//2)
        i = i//2
   
  def pop(self):
    if len(self.q) == 1:
      return None
    retVal = self.q[1]
    i = 1
    self.swap(1, -1)
    self.q.pop(-1)
    child = None  

    while self.findChild(i) != -1:
      if self.cmpfunc(self.q[i], self.q[self.findChild(i)]) == 1:
          temp = self.findChild(i)
          self.swap(i, self.findChild(i))
          i = temp
    return retVal
  
  def findChild(self, index):
    i = index
    if 2 * i >= len(self.q): #no child
      return -1
    elif 2 * i + 1 > len(self.q):
      return 2 * index
    else:
      if self.cmpfunc(self.q[2*i], self.q[2*i+1]) == -1:
        return 2*i
      else:
        return 2*i + 1

  
  def peek(self):
    if len(self.q) == 1:
      return None
    return self.q[1]
  
  def tolist(self):
    retlist = []
    for i in range(len(self.q)):
      if self.q[i] != None:
        retlist.append(self.q[i])
        self.q[i] = None
    return retlist
  
  def toString(self):
    print(self.q)

def my_cmp(a,b):
   if len(a) < len(b): return -1
   if len(a) == len(b): return 0
   return 1
  
Fred = Pqueue()
Fred.push(3)
Fred.push(2)
Fred.push(1)
Fred.push(5)
Fred.push(17)
Fred.pop()
Fred.push(1)
print(Fred.peek())
print(Fred.tolist())

