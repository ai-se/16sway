from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from models import *
from sa import *
from ga import *
from de import *

@setting
def OPTIMIZE(): return o(
  init = lambda m:  1000,
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
      i.how   = how
      i.name  = how.__name__
      i.pop0  = {}
      i.pop   = {}
      i.pop0Log = Num()
      i.popLog  = Num()
      i.naiveLog = Num()
      
def igd(models=[Fonseca,ZDT1],hows=[ga,de]):
  for model in models:
    rseed(the.OPTIMIZE.igdSeed)
    seeds = [r() for _ in xrange(the.OPTIMIZE.repeats)]  
    the.OPTIMIZE.msg(model.__name__)
    results = igd1(model,seeds,
                    the.OPTIMIZE.msg,
                    [HOW(one) for one in hows])
    print("")
    for k,v in results.items():
        print(k,v)
      
def igd1(model,seeds,msg, hows) :  
  ref, all = [], [] 
  for how in hows: 
    msg(how.name)
    for seed in seeds:
        say(1)
        a,z = control(model,how.how,seed=seed)
        how.pop0[seed]  = a
        how.pop[ seed]  = z
        all         += a + z  
        ref          = optimal(model,ref + z)  
  space = Space(all,get=objectives)
  for how in hows: 
     say(2)
     for seed in seeds:
        say(3)
        a  = how.pop0[seed]
        z  = how.pop[ seed]
        naive = optimal(model,a)
        for d in distances(a,    ref, space): how.pop0Log  + d
        for d in distances(z,    ref, space): how.popLog   + d
        for d in distances(naive,ref, space): how.naiveLog + d
  return {how.name : igdNormalize(how) for how in hows}  
  
def optimal(model,pop):
  return tournament(model(), pop, 
                    Space(pop,get=objectives),  
                    how=the.OPTIMIZE.how)                                             
                    
def distances(all,ref,allSpace):
  return [allSpace.closest(one,ref)[1] 
          for one in all]

def igdNormalize(how):
  pop0s  = how.pop0Log.also().range
  pops   = how.popLog.also().range
  naives = how.naiveLog.also().range
  norm   = lambda x,y: int(100 * (x-y)/(x+0.00001)) 
  norms  = lambda lst: [norm(toBe, asIs) for toBe,asIs in zip(lst,pop0s)]
  return { "baseline - naive" : norms(naives),
            "baseline - %s" % how.name : norms(pops) }
   
igd()