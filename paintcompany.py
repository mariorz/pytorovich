

from glpkwrap import *
"""
tatus: Optimal
LatexPaint = 4.0
n1 = 0.0
p2 = 0.0
p1 = 0.0
n2 = 600.0
n3 = 7.0
EmanelPaint = 0.0
p3 = 0.0

"""


prob = GoalProblem("The Paint Company Problem")


#using spaces in the name causes much faiL
x1 = prob.variable("LatexPaint",0)
x2 = prob.variable("EmanelPaint",0)

n1 = prob.variable("n1",0)
n2 = prob.variable("n2",0)
n3 = prob.variable("n3",0)

p1 = prob.variable("p1",0)
p2 = prob.variable("p2",0)
p3 = prob.variable("p3",0)

Priorities = [p1,n2,n3]



#prob += 1000*p1 + 100*n2 + 10*n3, "min function"
#f1 = 10*x1 + 15*x2 + n1 - p1 == 40, "man hours"
#f2 = 100*x1 + 100*x2 + n2 - p2 == 1000, "profit"
#f3 = x2 + n3 - p3 == 7, "order for friend"

f1 = 10*x1 + 15*x2 + n1 - p1 == 40
f2 = 100*x1 + 100*x2 + n2 - p2 == 1000
f3 = x2 + n3 - p3 == 7

o1 = prob.objective(f1)
o2 = prob.objective(f2)
o3 = prob.objective(f3)


P1 = prob.priority(p1)
P2 = prob.priority(n2)
P2 = prob.priority(n3)



prob.solve()
prob.display()








