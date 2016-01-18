# sway
from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from grid  import * 
from models import *
from mutate import *
 
@settings
def GRIDDING(): return o(
    enough=10,
    bigger=1.1,
    budget=100
)
    
def gridding1(m,get,grid,items, verbose):
    def shortShow(cell,*_):
        p = 100*len(cell)/items
        if p>= 1: return str(int(round(p,0)))
        if p> 0: return "."
        return " "
    #----------------
    logs = m.logs() 
    for _ in xrange(items):
      grid += get()
    bigBins = [(binx,biny, grid.middle(binx,biny)) 
                for binx,biny,cell in grid.theCells()
                if len(cell) > the.GRIDDING.enough]
    for _,_,one in bigBins:
        one = m.eval(one) 
        logs + one.objs  
    if verbose:
      print(len(bigBins))
      printm(grid.allCells( shortShow))
    return grid, [(binx,biny) 
                  for binx,biny,one in bigBins 
                  if anyImprovement(one,logs)]
  
def anyImprovement(one,logs):
  for obj,log in zip(one.objs,logs.logs):
    obj *= the.GRIDDING.bigger
    if obj < log.mu:
      return True   
     
def gridding(items   = 1000,
             f       = BASIC_5_2,
             seed    = None,
             verbose = True):
  if seed: rseed(seed) 
  getter = lambda : m.decide()
  budget = the.GRIDDING.budget
  while budget > 0:
    m       = f() 
    grid,bins  = gridding1(m, getter, MakeGrid(Space([],decisions)),
                             items, verbose)
    print(grid)
    budget -= len(bins)
    print(decisions(grid.anys(bins)))
    getter     = lambda : smear3(grid.anys(bins),
                               grid.anys(bins),
                              grid.anys(bins),decisions)
 
    
gridding()