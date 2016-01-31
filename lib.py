# sway
from __future__ import print_function, division
import random,math, numpy,sys
import gnuplotlib,os
sys.dont_write_bytecode = True

from boot import *

#### pretty print stuff 

def r3(x)    : return round(x,3)
def r4(x)    : return round(x,4)
def r5(x)    : return round(x,5)

def r3s(lst) : return map(r3,lst)
def r4s(lst) : return map(r4,lst)
def r5s(lst) : return map(r5,lst)

def say(*lst):
  for x in lst:
    sys.stdout.write(str(x))
  sys.stdout.flush()

def printm(matrix,sep=' | '):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = sep.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)

#### one-liners  

r      = random.random
any    = random.choice
within = random.uniform
rseed  = random.seed
sqrt   = math.sqrt
exp    = math.exp
ee     = math.e
pi     = math.pi
div   = lambda x,y: x/(y+0.00001)

def any2(lst,f=lambda x,y:[x,y]):
  return f(any(lst),any(lst))

def anyMean(lst,n=2):
  return mean([any(lst) for _ in xrange(n)])
  
#### list stuff

def first(lst)  : return lst[0]
def second(lst) : return lst[1]
def last(lst)   : return[-1]
def mean(lst)   : return sum(lst)/len(lst)
def shuffle(lst):
  random.shuffle(lst)
  return lst
  
#### misc stuff

def same(x) : return x
def lt(x,y) : return x < y
def gt(x,y) : return x > y

def _lib():
  reset()
  assert abs(r() - 0.134364244112) < 0.00001
  lst = list('abcd')
  assert first(lst) == 'a'
  assert lt(1,2)
  assert gt(2,1)
  assert same(lst) == lst
  assert r3s([1.1111111,2.2222]) == [1.111,2.222]
  assert div(1,0) > 0
  
def often(d,enough=10**32):
  n, lst = 0, []
  for x in d: 
    n   += d[x]
    lst += [(d[x],x)]
  lst = sorted(lst, reverse=True)
  while enough > 0:
    tmp = random.random()
    for freq,thing in lst:
      tmp -= freq*1.0/n
      if tmp <= 0:
        yield thing
        enough -= 1
        break
  
####################
# ascii graph stuff
# https://github.com/dkogan/gnuplotlib

data = numpy.asarray 
def textplot(*l,**d):
  assert len(l[0]) > 0, "no data found"
  gnuplotlib.plot(*l,unset='grid', 
                    terminal='dumb 80 30',**d)
def pngplot(*l,**d):
  out = os.environ["HOME"] + "/workspace/tmp/sway" + str(int(10000*r())) + ".pdf"
  if os.path.exists(out):
    os.remove(out)
  gnuplotlib.plot(*l,
     unset='grid', 
     output=out,
     terminal = 'pdf solid color font ",10" size 3.5in,3.5in',
     **d)  
  return out
 
def _textplot(): 
  x    = data([r() for _ in xrange(100)])
  textplot(x, x**0.33, 
          xlabel="x= width",title="y= black splots",
          yrange=[0,1.1],
          cmds="set key top left")
          
##################
# start up stuff

def main(name,*lst):
  if name == '__main__':
    ok(*lst)
  
 
main(__name__ ,_lib, _textplot)