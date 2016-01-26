from __future__ import print_function, division
import   sys
sys.dont_write_bytecode = True 

from optimize import * 
from mutate import *

@setting
def GA(): return o(
    repeats=10,
    popSize = 256,
    select="bdom", 
    enough = 0.75,
    verbose=True)
   
def ga(m,pop,logDecs,logObjs): 
  more = True
  repeats = the.GA.repeats
  while more and repeats > 0 :
    repeats -= 1
    while  len(pop) < the.GA.popSize:
      mum,dad =  any(pop), any(pop) 
      child   =  crossOverMutate(
                        (mum,dad), 
                        get   = decisions, 
                        lower = logDecs.space.lower, 
                        upper = logDecs.space.upper, 
                        ok    = m.ok,
                        evaluate = m.eval) 
      logDecs += child                
      logObjs += child
      pop     += [child] 
    pop = tournament(m,pop,logObjs.space,how=the.GA.select)
    print(len(pop))
    more = len(pop) < the.GA.popSize*the.GA.enough
  return pop

def _ga(): 
  for model in [Viennet4,ZDT1,Fonseca,DTLZ7_2_3]: #, Viennet4]:
    print(model.__name__) 
    for what in [ga]:
      print(what.__name__)
      control(model,what,seed=1)   
  
main(__name__,_ga)   
