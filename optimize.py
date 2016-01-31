from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from models import *
from sa import *

@setting
def OPTIMIZE(): return o(
  init = lambda m:  10*len(m.objs)
  igdSeed=1,
  msg = lambda x: print(x),
  repeats = 5,
  how = 'bdom'
) 

def popStats(m,pop,filter=same):
  logs = Logs([Num() for _ in m.objs])
  spaceObjs =  Space(pop,get=objectives)
  for one in filter(pop):
    logs + objectives(one)
    spaceObjs + one
  return [log.also().median for log in logs.logs],spaceObjs
  
def control(model,how,seed=1): 
  rseed(seed)
  m       = model()
  n       = the.OPTIMIZE.init(m) 
  pop0    = [m.eval(m.decide()) for one in xrange(n)] 
  #print(r3s(first(popStats(m,pop0))))
  logDecs = MakeGrid(Space(pop0,get=decisions))
  logObjs = MakeGrid(Space(pop0,get=objectives))
  for one in pop0:  
    logDecs+= one
    logObjs+= one 
  pop     = how(m,pop0[:],logDecs,logObjs)  
  map(m.eval,pop)  
  return pop0,pop
  
def dumb(m,pop,logDecs,lobObjs,how='bdom'):
  for _ in xrange(1000): 
     one      = m.eval(m.decide()) 
     lobObjs += one
     pop     += [one]
  return tournament(m,pop,lobObjs.space,how=how)
   
  
class HOW:
  def __init__(i,how):
      i.how  = how
      i.name = how.__name__
      i.last  = {}
      i.first = {}
      
def igd(models=[],hows=[de]):
  for model in models:
    reset(the.OPTIMIE.igdSeed)
    the.OPTIMIZE.msg(model.__name__)
    results = igd1(model, 
                    r(), 
                    the.OPTIMIZE.msg,
                    [HOW(one) for one in hows])
    igdReport(model,results)
    
def igd1(model,seed1,msg, hows)   
  bests  = []
  firsts = []
  all    = []
  for how in hows:
    for n in xrange(the.OPTIMIZE.repeats):
        aa,zz = control(model,how.how,seed=seed1)
        how.first[n] = aa
        how.last[n]  = zz
        firsts += aa
        all    += aa + zz  
        bests   = optimal(model,bests + zz) 
  allSpace = Space(all,get=objectives)
  for how in hows:
      baseline = Num()
      better = Num()
      eden = Num()
      for n in xrange(the.OPTIMIZE.repeats):
        aa,zz = how.first[n], how.last[n]
        for a in aa: 
          eden + allSpace.closest(a,bests)[1] 
        for baseline in optimal(model ,aa):
          baseline + allSpace.closest(baseline,bests)[1] 
                                              
                                              
def optimal(model,pop):
  return tournament(model(), pop, 
                    Space(pop,get=objectives),  
                    how=the.OPTIMIZE.how)                                             