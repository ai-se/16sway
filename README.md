```
 ____                                       
/\  _`\                                     
\ \,\L\_\  __  __  __     __     __  __     
 \/_\__ \ /\ \/\ \/\ \  /'__`\  /\ \/\ \    
   /\ \L\ \ \ \_/ \_/ \/\ \L\.\_\ \ \_\ \   
   \ `\____\ \___x___/'\ \__/.\_\\/`____ \  
    \/_____/\/__//__/   \/__/\/_/ `/___/> \ 
                                     /\___/ 
                                     \/__/  
```

# Definitions

sway:

+ _verb_
     + move or cause to move slowly or rhythmically backward and forward or from side to side.
         "he swayed slightly on his feet".
         synonyms:	swing, shake, oscillate,
         undulate, move to and fro, move back and 
         forth More  
+ _noun_
    + rule; control. "the part of the continent under 
         Russia's sway".
         synonyms:	clout, influence, power, weight, authority, control
         "his opinions have a lot of sway"



# Conventions

## Settings

Magic parameters are stored in functions that start with an UPPER CASE name 
and are decorated by `@setting`. e,g

```
@setting
def CUT(): return o( 
  crowded=4, 
  cohen=0.1,
  fayyad=False
)
```

Once written that way, we say that the above numbers are the _defaults_
for the global dictionary `the.CUT`.

These parameters can be accessed in the natural way:

    the.CUT.cohen    # returns 0.1

The defaults can   be altered as follows:

    CUT(cohen=0.2)
    
These values can be reset to their initial _defaults_ using:

     reset(seed=1)

This call finds **all** sets and sets them back to their _defaults_
(as well as resetting the random number seed to _"1"_). 
    
## Status

Every file tests itself; e.g.  to run scripts in boot.py:

    python boot.py

The following files (that have check marks)
currently are passing their tests:

-  [X] boot.py  
-  [X] lib.py  
-  [X] counts.py  
-  [X] space.py
-  [x] grid.py
-  [x] mutate.py  
-  [ ] model.py 
-  [ ] models.py  # tournament 
-  [ ] control.py 
