# sway
from __future__ import print_function, division
import  os,sys
sys.dont_write_bytecode = True 

from grid  import * 
from models import *
from mutate import *
 
@settings
def GRIDDING(): return o(
    enough=10,
    bigger=1.1,
    budget=64
)
    
def gridding1(m,all,grid,items, verbose):
    def shortShow(cell,*_):
        p = 100*len(cell)/items
        if p>= 1: return str(int(round(p,0)))
        if p> 0: return "."
        return " "
    #----------------
    evals =0
    logs = m.logs() 
    for one in all:
      grid += one
    bigBins = [(binx,biny, grid.middle(binx,biny)) 
                for binx,biny,cell in grid.theCells()
                if len(cell) > the.GRIDDING.enough]
    for _,_,one in bigBins:
        evals += 1
        one = m.eval(one) 
        logs + one.objs  
    if verbose:
      print(len(bigBins))
      #printm(grid.allCells( shortShow))
    for num in logs.logs:
        print(num.txt,num.also().range,num.also().iqr)
    return grid, evals, [(binx,biny) 
                  for binx,biny,one in bigBins 
                  if anyImprovement(one,logs)]
  
def anyImprovement(one,logs):
  for obj,log in zip(one.objs,logs.logs):
    obj *= the.GRIDDING.bigger
    if obj < log.mu:
      return True   
     
def gridding(items   = 1000,
             f       = Kursawe,
             seed    = None,
             verbose = True):
  if seed: rseed(seed) 
  budget  = the.GRIDDING.budget
  m       = f() 
  all     = [ m.decide() for _ in xrange(items) ]
  while True:
    space  = Space(get=decisions)
    grid,evals,bins = gridding1(m, all, 
                         MakeGrid(space), items, verbose)
    budget -= evals
    if budget <= 0: return 
    if not bins: return
    of = oftens(bins) 
    for bin in bins:
        print(bin)
        tmp = of[bin]
        print("")
        print(bin,tmp.dists)
        say("B> ")
        for n,x in enumerate(tmp.get):
            say(x)
            if n > 5: 
                print("")
                break
    exit()
    all = [ smear([ grid.anys(bins), 
                    grid.anys(bins),
                     grid.anys(bins)],
                     lower=space.lower,
                     upper=space.upper,
                      get=decisions) 
                for _ in xrange(items) ]
                

def oftens(bins):
    def dist((x1,y1),(x2,y2)):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5
    out={}
    for xy1 in bins:
        dists=  sorted([ (dist(xy1,xy2),xy2) for xy2 in bins])
        most = dists[-1][0]+0.0001
        dists = [(100-int(100*d/most),k) for d,k in dists] 
        neighbors={k:n/most for n,k in dists}
        get = often(neighbors) 
        out[xy1] = o(get=get,  dists=dists)
    return out
   
    
    
   
    
gridding()