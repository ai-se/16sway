from __future__ import print_function, division
import   sys
sys.dont_write_bytecode = True 

from optimize import * 

@settings
def SA(): 
  def e(m,x,space): 
      return mean(space.norms(m.eval(x)))
  return o(
    era=50,
    kmax=500,  
    how="bdom",
    energy = e,
    cooling=2,  
    verbose=True)
    
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
  print(10)
  sb = s = m.decide()
  eb = e = the.SA.energy(m,s,logObjs.space) 
  logDecs += s
  logObjs += e
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
    en  = the.energy(m,sn) 
    if bothAsGood(sn,sb, how=the.SA.how, space=logObjs):
       frontier += [sn]
    if en < eb:
      eb = en
      era.better += 1
      era.sb, era.eb = sn,en
      frontier = [sb]
    if en < e:
      s,e = sn,en
      era.lt += 1 
    elif exp((e - en)/t) < r():
      s,e = sn,en
      era.stagger += 1 
  return frontier
   

print(control(ZDT1,sa))

