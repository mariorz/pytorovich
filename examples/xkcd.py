
"""
------------------------
Knapsack Problem from
http://xkcd.com/287/
------------------------
"""

from pytorovich import LpProblem


prob = LpProblem("Linear Programming Test Problem")

items = ( ('MIXED FRUIT',   2.15),
          ('FRENCH FRIES',  2.75),
          ('SIDE SALAD',    3.35),
          ('HOT WINGS',     3.55),
          ('MOZZ STICKS',   4.20),
          ('SAMPLER PLATE', 5.80),
          ('BARBEQUE',      6.55) )

exactcost = 15.05

f = [prob.variable(item[0],0,None,int) * 
     item[1] for item in items]

prob.objective = [sum(f)]
prob.constraints = [sum(f) == exactcost]
prob.solve()

for key, val in prob.variables.iteritems():
   print "%s: %s" % (key, val.result)


