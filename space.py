#sway
from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from lib import *

@setting
def SPACE(): return o(
  norm=True
)

# need a way to init from a list

class Space:
  def __init__(i,inits=[],value=same,):
    i.value = value
    i.cache = {}
    i.lower, i.upper = None, None
    map(i.__add__,inits)
  def ready(i,one):
    if not i.lower:
      i.lower = [ 10**32 for _ in i.value(one)]
      i.upper = [-10**32 for _ in i.value(one)]
  def __add__(i,one):
    i.ready(one)
    for n,(lo,up,new) in enumerate(zip(i.lower, i.upper,
                                       i.value(one))):
      if new > up: i.upper[n] = new
      if new < lo: i.lower[n] = new
  def dist(i,xs,ys):
    a, b = id(xs), id(ys)
    if a > b:
      return i.dist(ys,xs)
    k = (a,b)
    if k in i.cache: 
      return i.cache[k]
    else:
      i.cache[k] = d = i.dist1(xs,ys)
      return d
  def dist1(i,xs,ys,d=0,n=0):
    i.ready(xs)
    one = i.value(xs)
    two = i.value(ys)
    for n,(x,y) in enumerate(zip(one,two)):
      x  = i.norm(x,n) 
      y  = i.norm(y,n) 
      d += (x - y)**2
      n += 1
    return sqrt(d) / sqrt(n)
  def norm(i,x,n):
    if x < i.lower[n]: i.lower[n] = x
    if x > i.upper[n]: i.upper[n] = x
    if the.SPACE.norm:
      lo = i.lower[n]
      up = i.upper[n]
      return div( (x- lo) , (up - lo) )
    else:
      return x
  def furthest(i,one,all,better=gt,most=0):
    d, out = most, one
    for two in all:
      if id(two) != id(one):
        tmp = i.dist(one,two)
        if better(tmp,d):
          d,out = tmp,two
    return out,d
  def closest(i,one,all):
    return i.furthest(one,all,better=lt,most=10**32)

def _space(arity=5, items=1000):
  reset() 
  print(1)
  space=Space() 
  one = None
  all = []
  for _ in xrange(items):
    one = [r3(r()) for _ in xrange(arity)]
    space + one
    all += [one]
  print("Lo",space.lower)
  print("up",space.upper)
  assert sum(space.lower) < 0.01*arity
  assert sum(space.upper) > 0.99*arity
  two,d2   = space.closest(one,all)
  three,d3 = space.furthest(one,all)
  print("one",one)
  print("closest",two,d2)
  print("furthest",three,d3)
  assert d2 < d3  
  
main(__name__, _space)
  
