from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from models import *

@setting
def OPTIMIZE(): return o(
  init = lambda m:  10*len(m.objs)
) 

def control(model,how,seed=1):
  print(1)
  rseed(seed)
  m = model()
  n       = the.OPTIMIZE.init(m) 
  pop0    = [m.eval(m.decide()) for one in xrange(n)] 
  logDecs = MakeGrid(Space(pop0,get=decisions))
  logObjs = MakeGrid(Space(pop0,get=objectives))
  for one in pop0: 
    print(one)
    logDecs+= one
    logObjs+= one
  print(10)
  pop     = how(m,pop0[:],logDecs,logObjs) 
  map(m.eval,pop)
  print(30)
  return pop0,pop