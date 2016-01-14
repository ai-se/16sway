# sway
from __future__ import print_function, division
from functools import wraps
import  sys
sys.dont_write_bytecode = True 

from lib import *
from space import *

@setting
def MUTATE(): return o(
  p        = 0.33,
  nudge    = 2,
  cr       = 0.7, 
  f        = 0.3,
  retries  = 100,
  restrain = lambda x,lower,upper: bound(x,lower,upper)
)


##################################################
def bounded(lst,lower,upper):
  for x,lo,up in zip(lst,lower,upper):
    if not lo <= x <= up:
      return False
  return True
  
def bound(lst,lower,upper):
  def bound1(x, lo, up):
    if   lo == up: return lo
    elif x  == up: return up
    else:
      return lo + ((x - lo) % (up - lo))
  return [bound1(x,lo,up) for x,lo,up in 
          zip(lst, lower, upper)]

def truncated(lst,lower,upper):
  return [ min(max(x,lo),up) 
           for x,lo,up in zip(lst,lower,upper)]

def _restrain():
  lower  = [3,3,3,3]
  upper  = [7,7,7,7]
  data   = [2,3,7,8] 
  assert [6,3,7,4] == bound( data,lower,upper)
  assert [3,3,7,7] == truncated(data,lower,upper)

##################################################
def mutator(f): 
  WARNING = ": too hard to satisfy %s" % f.__name__
  #@wraps
  def worker(old,get=same,
             lower    = None, 
             upper    = None,
             ok       = None,
             evaluate = None,  
             put     = lambda z : o(objs=None, decs=z),
             retries  = the.MUTATE.retries):
    dec1 = f(old,get,lower, upper) 
    dec2 = the.MUTATE.restrain(dec1,lower,upper) 
    new  = put(dec2)
    if ok: 
      assert retries > 0,WARNING
      if not ok(new):
        return worker(old,get=same,
                      lower    = lower,
                      upper    = upper,
                      ok       = ok,
                      evaluate = evaluate,
                      put     = put,
                      retries  = retries-1)
    return evaluate(new) if evaluate else new
  return worker
  
######################################################  
@mutator
def mutate(old,get,lower,upper):
  p = the.MUTATE.p 
  return [x if p < r() else lo + (up - lo)*r() 
          for x,lo,up 
          in  zip(get(old),lower,upper)]
          
def _some(most = 10 , arity =5):
  reset()
  lower = [0 for _ in xrange(arity)]
  upper = [1 for _ in xrange(arity)]
  all = [[r() for _ in xrange(arity)]
              for _ in xrange(most)] 
  return most,arity,lower,upper, all
  
def _mutator1():
  most,arity,lower,upper, all = _some()
  MUTATE(p=0,retries=20)
  for one in all:
    two = mutate(one, lower=lower,upper=upper,put=same)
    assert one == two
 
def _mutator2():   
  most,arity,lower,upper, all = _some()
  MUTATE(p=0.33,retries=20)
  ok = lambda lst: sum(lst) < 0.75*arity
  for one in all:
    two = mutate(one, lower=lower,upper=upper,put=same, ok=ok)
    assert bounded(one,lower,upper)
    assert bounded(two,lower, upper)
    assert ok(one) or (not(ok(one)) and ok(two))   

######################################################  
@mutator
def interpolate(all,get,*_):
  return [x + r()*(y-x)
          for x,y 
          in  zip(get(any(all)),
                  get(any(all)))]

def _interpolate():
  most,arity,lower,upper, all = _some()
  for _ in all:
    new = interpolate(all, lower=lower,upper=upper,get=same)
    bounded(new.decs, lower, upper)
                   
######################################################  
@mutator
def nudge((here,there),get,*_):
   return [ x + r()*the.MUTATE.nudge*(y - x)
            for x,y
            in  zip(get(here), 
                    get(there)) ]
  
def _nudge():
  most,arity,lower,upper, all = _some()
  for _ in all:
    new = nudge((any(all),any(all)), lower=lower,upper=upper,get=same)
    bounded(new.decs, lower, upper)
    
######################################################  
@mutator
def smear(all,get,*_):
  aa, bb, cc = any(all), any(all), any(all)
  f = the.MUTATE.f
  cr= the.MUTATE.cr
  tmp=  [a + f*(b - c) if r() < cr else a
         for a,b,c
         in  zip(get(aa),
                 get(bb),  
                 get(cc))]
  n = random.randint(0,len(aa)-1)
  tmp[n] = aa[n]
  return tmp

def _smear():
  most,arity,lower,upper, all = _some()
  for _ in all:
    new = smear(all, lower=lower,upper=upper,get=same)
    bounded(new.decs, lower, upper)

######################################################  
    
main(__name__,
      _restrain,_mutator1,_mutator2,_interpolate,_nudge,_smear)

