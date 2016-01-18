from __future__ import print_function, division
import  sys
sys.dont_write_bytecode = True 

from models import *

def _div(items=512):
  models= [ZDT1] #,Fonseca,Kursawe]
  models=[Kursawe]
  for f in models:
    reset()
    GRID(bins=16)
    COUNTS(qs=[0.25,0.5,0.75])
    print(f.__name__)
    m=f()
    rows, _,all,gridDecs,gridObjs= _gridding(m,items)
    print("\n")
    mat = [  [ _show(cell,items) for cell in  row]  
               for row  in  rows]
    mat1 = [[r]+x for r,x in enumerate(mat[:])]
    
    mat1 = [[" "] + [i for i in xrange(len(row))]]+ mat1
    printm(mat1,sep=",")           
    cells = []
    for r,row in enumerate(rows):
        for c,cell in enumerate(row):
          cells += [(r,c,cell)]
    print("")
    s=0
    anys=10
    overalls =  _divParts(m,all) 
    for i in xrange(len(m.objs)):
      print("")
      overall = [overalls[i].also().median]
      top=overall[s] 
      print(i,"all :",r3s(overall),r3(top),sep=",")
      reports = []
      for x,y,cell in cells:
        if len(cell) > anys :
          parts= _divParts(m,cell)
          #part = [parts[i].also().median] 
           
          mid = gridDecs.middles(x,y) ;part = [ mid[0].objs[i] ]
          #part=sorted([one.of.objs[s]  for one in mid])
          if part[s]  < overall[s]:
            deltas = [int(div(100* (theres - here), theres))
                      for here,theres in zip(part,overall)]
            top1 = r3(part[s])
            reports += [[i,x,y,"part:",r3s(part),"deltas:",deltas,"len=",len(cell),r3(top1/top)]]
      for report in sorted(reports,key=lambda z: -1*z[4][0]):
        print(*report)

def _divParts(m,lst):
  nums = [Num() for _ in m.objs]
  for one in lst:
    for num,obj in zip(nums,one.objs):
        num+ obj 
  return nums
 
def _rahul(items=512):
  models= [BASIC,BASIC,
           BASIC_10_2,BASIC_10_2,
           BASIC_20_2,BASIC_20_2,
           BASIC_40_2,BASIC_40_2,
           BIASED,BIASED,
           BIASED_10_2,BIASED_10_2,
           BIASED_20_2,BIASED_20_2,
           BIASED_40_2,BIASED_40_2
           ] #ZDT1,Fonseca,Kursawe]
  for f in models:
    reset()
    GRID(bins=16)
    print(f.__name__)
    rows,_= _gridding(f(),items)
    print("\n")
    printm([ [ _show(cell,items) for cell in row]  
            for row  in rows])
            
def _gridding(m,items):
    spaceDecs = Space(value=decisions)
    spaceObjs = Space(value=objectives) 
    gridDecs  = Grid(spaceDecs)
    gridObjs  = Grid(spaceObjs)
    all =  [_worker(m,spaceDecs,gridDecs,spaceObjs,gridObjs)  
            for _ in xrange(items)] 
    #xs1,ys1= _frontier(m,all,spaceObjs) 
    #xs2,ys2= _frontier(m,all,spaceObjs,how='cdom') 
    ##print("Bdoms",len(xs1))
    #print("Cdoms",len(xs2))
    
    #textplot(
     #     (data(xs2), data(ys2), {'legend':'cdom'}),
      #    (data(xs1), data(ys1), {'legend':'bdom'}),
       ### cmds="set key bottom left") 
    return gridDecs.cells, gridObj.cells,all,gridDecs,gridObjs

def _worker(m,spaceDecs,gridDecs,spaceObjs,gridObjs):
    x = m.decide()
    spaceDecs + x
    gridDecs += x
    x= m.eval(x)
    spaceObjs + x 
    gridObjs += x
    return x
    
def _show(cell,items,r=None,c=None):
    n = len(cell) 
    p =   int(100*n /items) 
    if p >=  1: return n 
    if n > 0 : return "_"
    return " "
  
def _frontier(m,all,spaceObjs,how="bdom"):
    some = tournament(m,all,spaceObjs,how=how) 
    xs,ys= [],[]
    for one in sorted(some,key=lambda z:z.objs):
        xs += [one.objs[0]]
        ys += [one.objs[1]]
    return xs,ys
  