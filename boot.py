# sway
from __future__ import print_function, division
import zipfile,re,traceback,random,sys
sys.dont_write_bytecode = True 
 

##################################################
# test engine

class ok:
  tries = fails = 0  #  tracks the record so far
  def score(i):
    t,f= ok.tries, ok.fails
    return "# TRIES= %s FAIL= %s %%PASS = %s%%"  % (
      t,f,int(round(t*100/(t+f+0.001))))
  def __init__(i,*tests):
    map(i.test,tests)
    print(i.score())
  def test(i,f):
    print("### ",f.__name__)
    ok.tries += 1
    try: f()
    except Exception,e:
      ok.fails += 1
      i.report(f,e)
  def report(i,test,e):
    _, _, tb = sys.exc_info()
    f, line, fun, what = traceback.extract_tb(tb)[-1]
    print('{}: line {}, in {} ==> {} {}'.format(
        f, line, fun, what,e))

def _ok():
  def oa():
    assert 1==1
    assert 2==1
    assert 5==1 # never reached
  def ob(): # called, even though a() has errors
    assert 10==10
  def oc():
    assert 3==3
    assert 3==1
  ok(oa,ob,oc)

class o:
  def __init__(i,**d)   : i.add(**d)
  def __setitem__(i,k,v): i.__dict__[k] = v
  def __getitem__(i,k)  : print(k); return i.__dict__[k]
  def __repr__(i)       : return 'o'+str(i.__dict__)
  def add(i,**d)        : return i.__dict__.update(d)
  def items(i)          : return i.__dict__.items()

def _o():
  def oa(): 
    x=o(name='tim',age=55)
    x['name'] = 'tom'
    assert x.name == 'tom'
    x.name = 'tony'
    assert x.name == 'tony'
    assert str(x) == "o{'age': 55, 'name': 'tony'}" 
  ok(oa)

####################################################
# option controls

class settings:
  funs = o()
  all  = o()
  def __init__(i,f):
    what = f.__name__   
    def g(**d):
      tmp = f()
      tmp.add(**d)
      settings.all[what] = tmp
      return tmp
    settings.funs[what] = g
    settings.all[what]  = g()
  @staticmethod
  def reset(seed=1):
    for k,v in settings.funs.items():
      settings.all[k] = v() 
    random.seed(seed)
def setting(f):
  settings(f)
  return settings.funs[f.__name__]

the=settings.all
reset=settings.reset

__name__ == '__main__' and ok(_ok,_o)
