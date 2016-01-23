from __future__ import print_function, division
import   sys
sys.dont_write_bytecode = True 

from models import * 

@settings
def SA(): 
  def e(m,x,space): 
      return mean(space.norms(m.eval(x)))
  return o(
    era=50,
    kmax=1000, 
    aggr=normmean,
    energy = e,
    cooling=2,
       retries=100,
       p=0.33,
       verbose=False)
    
def saControl():
  eras= {}
  era = b4 = None  
  for k in xrange(the.SA.kmax):
     t   = ((k+1)/the,SA.kmax)**the.SA.cooling
     now = int(k/the.SA.era)  
     if now-1 in eras:
        b4 = eras[now-1]
     if not now in eras:
        era = eras[now]= o(lt=0,stagger=0,better=0,e=[],evals=0)
        if b4:
            era.eb    = b4.eb
            era.sb    = b4.sb
            era.evals = b4.evals 
        saReportEra(era) 
     era.evals += 1
     yield t,era 
  saReportEra(era)
   
def saReportEra(era): 
    if the.SA.verbose:
        print("%4d::" %era.evals,r4(era.eb)," ",
              o(lt=era.lt,stagger=era.stagger,better=era.better),
            end="")
        print(("  * %s" % r3s(era.sb.objs)) if era.better > 0 else "")
    
def sa(m,_, logDecs,logObjs): 
  sb = s = m.decide()
  eb = e = the.SA.energy(m,s,logObjs.space) 
  logDecs += s
  logObjs += e
  for t,era in saControl(): 
    sn  = mutate(s, get   = decisions, 
                 lower    = logDecs.space.lower, 
                 upper    = logDecs.space.upper, 
                 ok       = m.ok,
                 evaluate = m.eval) 
    logDecs + sn
    logObjs + sn
    en  = the.energy(m,sn) 
    if en < eb:
      eb = en
      era.better += 1
      era.sb, era.eb = sn,en
    if en < e:
      s,e = sn,en
      era.lt += 1
    elif exp((e - en)/t) < r():
      s,e = sn,en
      era.stagger += 1
    era.e += [e]
  return [sb]