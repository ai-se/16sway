from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from models import *

@setting
def OPTIMIZE(): return o(
  init = lambda m:  10*len(m.objs)
) 

def pop0stats(m,pop):
  logs = Logs([Num() for _ in m.objs])
  for one in pop:
    logs + objectives(one)
  return [log.also().median for log in logs.logs]
  
def control(model,how,seed=1): 
  rseed(seed)
  m       = model()
  n       = the.OPTIMIZE.init(m) 
  pop0    = [m.eval(m.decide()) for one in xrange(n)] 
  print(r3s(pop0stats(m,pop0)))
  logDecs = MakeGrid(Space(pop0,get=decisions))
  logObjs = MakeGrid(Space(pop0,get=objectives))
  for one in pop0:  
    logDecs+= one
    logObjs+= one 
  pop     = how(m,pop0[:],logDecs,logObjs)  
  map(m.eval,pop)  
  return pop0,pop