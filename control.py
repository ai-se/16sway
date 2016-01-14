# sway
def optimize(model,how,seed=1,init=10,verbose=False,retries=100,**d):
  rseed(seed)
  init=10*len(model.objs)
  pop0   = [model.eval(model.decide(retries=retries))
             for one in xrange(init)]
  #check1(">",pop0)
  logDecs = Log(pop0, value=decs)
  logObjs = Log(pop0, value=objs)
  pop = how(model,pop0[:],logDecs,logObjs, verbose=verbose,**d)
  #check1("<",pop)
  map(model.eval,pop)
  return pop0,pop
  
def igd(models=[Fonseca,ZDT1],hows=[de],verbose=False,
        repeats=5, seed0=1,init=300,selects=bdoms,select="bdom"):
  class metas:
    def __init__(i,how):
      i.how  = how
      i.name = how.__name__
      i.last  = {}
      i.first = {}
  hows = [metas(how) for how in hows]
  for model in models:
    print("-",model.__name__)
    rseed(seed0)
    every = []
    firsts = []
    lasts = []
    bests = []
    for n in xrange(repeats):
      say("|")
      seed1 = r()
      for meta in hows:
        say(".")
        a,z = optimize(model(),meta.how,seed=seed1,
                       init=init,repeats=repeats,select=select)
        meta.last[seed1]  = z
        meta.first[seed1] = a
        firsts += a
        lasts += z
        every += a
        every += z
        say(1)
        space1 = Space(z[0],value=objs)
        space1.updates(a+z)
        say(2); say(":");
        say(len(bests+z))
        bests = selects(model(),bests+z,space1)
        say(3)
    say("!!")
    space = Space(every[0],value=objs)
    space.updates(every)
    say("\n")
    once=True
    for meta in hows:
       baseline = Num()
       better   = Num()
       eden     = Num()
       for k in meta.last:
         for e in meta.first[k]:
           _,d=space.closest(e,bests)
           eden + d
         for a in selects(model(),meta.first[k],space):
           _,d = space.closest(a,bests)
           baseline + d
         for z in meta.last[k]:
           _,d = space.closest(z,bests)
           better + d
       #print(eden.also().range,",eden,",model.__name__)
       #print(baseline.also().range,",baseline,",model.__name__)
       #print(better  .also().range,",",meta.name, ",",model.__name__)
       comp1= [int(100*(a-z)/(a+0.00001))
               for a,z in zip(eden.also().range,baseline.also().range)]
       comp2= [int(100*(a-z)/(a+0.00001))
               for a,z in zip(eden.also().range,better.also().range)]
       if once:
         print(comp1,"eden - baseline")
         once=False
       print(comp2,"eden - ",meta.name)
         
def ranges(space,best,what):
  return Num([space.closest(one,best)[1] for one in what]).also().range[1:4]
