import math

def S(e):
    return -sum([p*math.log(p,2) for p in e if p > 0])

print S([5.0/14,5.0/14.0,4.0/14])
