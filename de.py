from __future__ import print_function, division
import   sys
sys.dont_write_bytecode = True 

from optimize import * 
from mutate import *

@setting
def DE(): 
   def size(m): return len(m.objs)*10
   return o(
    cr=0.3,
    f =0.75,
    repeats=10,
    select="bdom",
    size = size,
    verbose=True)
    
def de(m,frontier,logDecs,logObjs): 
  for r in xrange(the.DE.repeats):
    for n,parent in enumerate(frontier):
      child = smear(frontier,
                    get     = decisions, 
                    lower   = logDecs.space.lower, 
                    upper   = logDecs.space.upper, 
                    ok      = m.ok,
                    evaluate= m.eval)
      logDecs += child                
      logObjs += child
      if m.select(child,parent,
                     how=the.DE.select,
                     space=logObjs.space):
          frontier[n] = child

  return frontier

def _de(): 
  for model in [Viennet4,ZDT1,Fonseca,DTLZ7_2_3]: #, Viennet4]:
    print(model.__name__) 
    for what in [de,sa]:
      print(what.__name__)
      control(model,what,seed=1)   
  
main(__name__,_de)   
