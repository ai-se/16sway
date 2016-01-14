# sway
from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from counts import *
from space import *

@setting
def GRID(): return o(
 bins=16, # each grid has bins**2 cells
 tooMuch= 1.05 # regrowth grids when new "c" more than "bigger"
)

class Grid(Some):
  def __init__(i,space=None,init=[],):
    i.n,i.max,i.all, i.grid = 0,2,[], None
    i.space = space or Space()
    map(i.__add__,init)
  def atFull(i,x): 
    i.grid = i.grid or  Grid1(east=i.all[0],
                              west=i.all[1],
                              space=i.space) 
    i.grid + x
    
class Grid1:
  def __init__(i,east,west,inits=[],space=None):
    i.space = space or Space()
    i.reset(east,west,inits)
    i + east
    i + west
  def reset(i,east,west,inits=[]): 
    say("*")
    b4 = inits[:]
    i.east, i.west = east,west
    i.c      = i.dist(east,west)
    i.values = [] 
    i._pos   = {}
    i.cells   = [[[] for _ in range(the.GRID.bins)]
                     for _ in range(the.GRID.bins)] 
    map(i.__add__,inits)
  def dist(i,x,y):
    return i.space.dist(x,y)
  def __add__(i,one):
    a = i.dist(i.east,one)
    b = i.dist(i.west,one)
    c = i.c
    if  0 <  c*the.GRID.tooMuch  < a: 
      i.reset(i.east,one,i.values)
      return i + one
    if 0 < c*the.GRID.tooMuch < b: 
      i.reset(one,i.west,i.values)
      return i + one
    i.values += [one]
    x = div( a**2 + c**2 - b**2  , 2*c)
    if x**2 > a**2:
      x = a 
    y = sqrt(a**2 - x**2)
    binx, biny = i.bin(x), i.bin(y)
    i.cells[ binx ][ biny ] += [one]
    i._pos[id(one)] = o(x=x,y=y,binx=binx,
                        biny=biny,a=a,b=b)
    return x,y
  def bin(i,x):
    x = int(x/((i.c+0.0001)/the.GRID.bins))
    return max(0,min(the.GRID.bins - 1, x))
  def pos(i,x) :
    return i._pos[id(x)]
    
def _grid(items=1000,arity=5):
  reset()
  #GRID(bins=5)
  def show(n):
    q = int(round(100 *  n /len(g.grid.values),0))
    return q if q else " "
  
  g=Grid()
  for _ in xrange(items):
    one = [r3(r()/10) for _ in xrange(arity)]
    g + one
  for _ in xrange(items):
    one = [r() for _ in xrange(arity)]
    g + one 
  m= map(lambda cells:  
            map(lambda cell: show(len(cell)), 
                cells),
         g.grid.cells)
  print("")
  printm(m)
  assert len(g.grid.values) == items *2
    
main(__name__,_grid)