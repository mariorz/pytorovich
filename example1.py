
from glpkwrap import *




"""
OPTIMAL SOLUTION FOUND
Time used:   0.0 secs
Memory used: 0.1 Mb (53708 bytes)
lpx_print_sol: writing LP problem solution to `/var/folders/P3/P3SbaQdAGTOsG8yulRnTKk+++TI/-Tmp-/94351-pulp.sol'...
Status: Optimal
x1 = 4.0
x2 = 6.0
objective function:  18.0

"""


prob = GoalProblem("Goal Programming Test Problem")

x1 = prob.variable("x1",0)
x2 = prob.variable("x2",0)

n1 = prob.variable("n1",0)
n2 = prob.variable("n2",0)
n3 = prob.variable("n3",0)

p1 = prob.variable("p1",0)
p2 = prob.variable("p2",0)
p3 = prob.variable("p3",0)


f1 = (x1 + x2 + n1 - p1 == 10, "profits")
f2 = (x1 + n2 - p2 == 4, "hours")
f3 = (5*x1 + 3*x2 + n3 - p3 == 56, "revenue")

o1 = prob.objective(f1)
o2 = prob.objective(f2)
o3 = prob.objective(f3)

g1 = 2*p1 + 3*p2
g2 = n3

P1 = prob.priority(g1)
P2 = prob.priority(g2)

prob.solve()

prob.display()


