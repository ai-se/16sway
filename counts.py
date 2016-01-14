# sway
from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from lib import *

@setting
def COUNTS(): return o(
  max=256,
  qs = [0.1, 0.3, 0.5, 0.7, 0.9],
  round = r3s
)
class Some:
  def __init__(i, init=[], max=None):
    i.n, i.all, i.max = 0,[],max or the.COUNTS.max
    map(i.__add__,init)
  def __add__(i,x):
    i.n += 1
    now = len(i.all)
    if now > i.max:    return i.afterFull(x)
    if now < i.max:    return i.beforeFull(x)
    return i.atFull(x)
  def beforeFull(i,x):
    i.all += [x]
  def atFull(i,x): 
    return i.afterFull(x)
  def afterFull(i,x):
    now = len(i.all)
    if r() <= now/i.n:
      i.all[ int(r() * now) ]= x

class Log: pass

class Num(Log):
  def __init__(i,inits=[]):
    i.hi = i.lo = None
    i.mu = i.sd = i.m2 = 0  
    i.n = 0
    i.some = Some()
    i._also= None
    map(i.__add__,inits)
  def __add__(i,z):
    i._also = None
    i.n  += 1
    i.some + z
    i.lo  = min(z,i.lo)
    i.hi  = max(z,i.hi)
    delta = z - i.mu;
    i.mu += delta/i.n
    i.m2 += delta*(z - i.mu)
    if i.n > 1:
      i.sd = (i.m2/(i.n - 1))**0.5
  def norm(i,z):
    return div( (z - i.lo), (i.hi - i.lo))
  def also(i):
    if not i._also:
      lst = sorted(i.some.all)
      m   = len(lst) 
      r   = the.COUNTS.round
      i._also = o(some=lst,
                  median=lst[int(m/2)],
                  range=r([lst[int(m*x)] for x in the.COUNTS.qs]))
    return i._also
  
class Logs:
  def __init__(i,logs=[],inits=[]):
    i.logs = logs
    map(i.__add__,inits)
  def __add__(i,x):
    for log in i.logs:
      log + x

def _counts():   
  reset()
  most = 1000
  want = [0.05, 0.25, 0.5, 0.75,0.95]
  COUNTS(max=most,qs=want)
  got1 = Num([r() for _ in xrange(most)]).also().range
  got2 = Num([r() for _ in xrange(most)]).also().range
  print("M P SubSampling ReSampling SubWorseThanReSampling")
  for few in [32,64,128,256,512]: 
    print("")
    COUNTS(max=few,qs=want)
    got0 = Num([r() for _ in xrange(most)]).also().range
    for g0,w,g1,g2 in zip(got0,want,got1,got2):
      subSampling = r3(100*div(g0-w,w))
      reSampling  = r3(100*div(g1-g2,g1))
      subSampling = 0 if abs(subSampling) < 5 else subSampling
      reSampling  = 0 if abs(reSampling)  < 5 else reSampling
      print(few,w,subSampling, reSampling, 
            abs(reSampling) < abs(subSampling))

main(__name__, _counts)
