from __future__ import print_function, division
import   sys
sys.dont_write_bytecode = True 

from optimize import * 
from mutate import *

@setting
def SA(): 
  def e(m,x,space): 
    return mean(space.norms(m.eval(x)))
  return o(
    era=256,
    kmax=2000,  
    how="bdom",
    energy = e,
    cooling=5,  
    verbose=True)
    
def saControl():
  eras= {}
  era = b4 = None   
  for k in xrange(the.SA.kmax):
     t   = ((k+1)/the.SA.kmax)**the.SA.cooling
     now = int(k/the.SA.era)  
     if now-1 in eras:
        b4 = eras[now-1]
     if not now in eras:
        era = eras[now]= o(lt=0,stagger=0,better=0,e=[],
                           evals=0,eb=10**32,sb=[])
        if b4:
            era.eb    = b4.eb
            era.sb    = b4.sb
            era.evals = b4.evals 
            saReportEra(b4) 
     era.evals += 1 
     yield t,era 
  saReportEra(era)
  print("")
   
def saReportEra(era): 
    if the.SA.verbose:
        print("\n%6d:: %3f " % (era.evals,r4(era.eb)),
              o(lt=era.lt,stagger=era.stagger,better=era.better),
            end="")
        say(("  * %s" % r3s(era.sb.objs)) if era.better > 0 else "")
    
def sa(m,_, logDecs,logObjs):  
  sb = s = m.decide()
  eb = e = the.SA.energy(m,s,logObjs.space) 
  logDecs += s
  logObjs += s
  frontier = []
  for t,era in saControl():  
    era.e += [e] 
    sn  = mutate(s, get   = decisions, 
                 lower    = logDecs.space.lower, 
                 upper    = logDecs.space.upper, 
                 ok       = m.ok,
                 evaluate = m.eval) 
    
    
    logDecs += sn
    logObjs += sn
    en  = the.SA.energy(m,sn,logObjs.space)   
    if en < eb:
      eb = en
      era.better += 1
      era.sb, era.eb = sn,en
      frontier = [sb]
    elif m.bothAsGood(sn,sb, how=the.SA.how, space=logObjs):
      frontier += [sn]
    if en < e:
      s,e = sn,en
      era.lt += 1 
    elif exp((e - en)/t) < r():
      s,e = sn,en
      era.stagger += 1 
  return  frontier 
   
def _sa(): 
  for source in [Viennet4,ZDT1,Fonseca,DTLZ7_2_3]: #, Viennet4]:
    print(source.__name__)
    control(source,sa,seed=1)  
  
main(__name__,_sa)
