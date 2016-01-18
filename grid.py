# sway
from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from counts import *
from space import *

@setting
def GRID(): return o(
 bins=16, # each grid has bins**2 cells 
)

class MakeGrid:
  def __init__(i,space=None):
    i.east, i.west, i.space=None, None, space
  def __iadd__(i,one): 
    if   not i.east:  i.east = one  
    elif not i.west:  i.west = one 
    else:
      return Grid(i.east,i.west,space=i.space) 
    return i
    
class Grid:
  def __init__(i,east,west,inits=[],space=None): 
    i.space = space or Space()
    i.tooMuch = 1 + 1/the.GRID.bins
    i.reset(east,west,inits,"0")
    i += east
    i += west
  def reset(i,east,west,inits=[],comment="*"): 
    say(comment)
    b4 = inits[:]
    i.east, i.west = east,west
    i.c      = i.dist(east,west)
    i.values = [] 
    i._pos   = {}
    i.cells   = [[[] for _ in range(the.GRID.bins)]
                     for _ in range(the.GRID.bins)] 
    map(i.__iadd__,inits)
  def dist(i,x,y):
    return i.space.dist(x,y)
  def __iadd__(i,one): 
    a = i.dist(i.east,one)
    b = i.dist(i.west,one)
    c = i.c
    if  0 <  c*i.tooMuch < a: 
      i.reset(i.east,one,i.values)
      i += one
      return i
    if 0 < c*i.tooMuch < b: 
      i.reset(one,i.west,i.values)
      i += one
      return i
    i.values += [one]
    x = div( a**2 + c**2 - b**2  , 2*c)
    if x**2 > a**2:
      x = a 
    y = sqrt(a**2 - x**2)
    binx, biny = i.bin(x), i.bin(y)
    i.cells[ binx ][ biny ] += [one]
    i._pos[id(one)] = o(x=x,y=y,binx=binx,of=one,
                        biny=biny,a=a,b=b)
    return i
  def theCells(i):
    for binx,row in enumerate(i.cells):
      for biny,cell in enumerate(row):
        yield binx,biny,cell
  def allCells(i,f=lambda c,x,y: (len(c),x,y)):
     return [ [f(cell,binx,biny) 
              for biny,cell in enumerate(row)]
              for binx,row  in enumerate(i.cells)]
  def anys(i,lst):
    return i.any(*any(lst))
  def any(i,binx,biny):
    return any(i.cells[binx][biny])
  def middle(i,binx,biny):
    cell  = i.cells[binx][biny]
    all   = map(i.pos,cell)
    xmu   = mean([z.x for z in all])
    ymu   = mean([z.y for z in all])
    out,d = None,10**32
    for z in all:
      tmp = ((z.x - xmu)**2 + (z.y - ymu)**2)**0.5
      if tmp < d:
        out,d = z.of,tmp
    return out
  def bin(i,x):
    x = int(x/((i.c+0.0001)/the.GRID.bins))
    return max(0,min(the.GRID.bins - 1, x))
  def pos(i,x) :
    return i._pos[id(x)]
    
def _grid(items=1000,arity=5):
  reset()
  GRID(bins=16)
  def show(n):
    n = 100 *  n /len(g.values)
    q = int(round(n,0))
    if n >= 1: return q
    if n >  0: return "."
    return " "
    
  g=MakeGrid()
  for _ in xrange(items):
    one = [r3(r()/10) for _ in xrange(arity)]
    g += one
  for _ in xrange(items):
    one = [r() for _ in xrange(arity)]
    g += one 
  m= map(lambda cells:  
            map(lambda cell: show(len(cell)), 
                cells),
         g.cells)
  print("")
  printm(m)
  assert len(g.values) == items *2-1
  return g
 
  
    
#main(__name__,_grid)