"""
------------------------
Example problem:
http://www.cs.cornell.edu/~tomf/pyglpk/ex_ref.html
------------------------


maximize Z = 10x0 + 6x1 + 4x2

subject to: 	

p = x0 + x1 + x2
q = 10x0 + 4x1 + 5x2
r = 2x0 + 2x1 + 6x2

and bounds of variables:	

-inf < p <= 100   0 <= x0 < inf
-inf < q <= 600   0 <= x1 < inf
-inf < r <= 300   0 <= x2 < inf


"""

from pytorovich import LpProblem

prob = LpProblem("Goal Exammple")
x0 = prob.variable("x0",0)
x1 = prob.variable("x1",0)
x2 = prob.variable("x2",0)
n1 = prob.variable("n1",0)
n2 = prob.variable("n2",0)
n3 = prob.variable("n3",0)
n4 = prob.variable("n4",0)
p1 = prob.variable("p1",0)
p2 = prob.variable("p2",0)
p3 = prob.variable("p3",0)
p4 = prob.variable("p4",0)

f1 = 10*x0 + 6*x1 + 4*x2 + n1 - p1 == 1000
f2 = x0 + x1 + x2 + n2 - p2 == 100
f3 = 10*x0 + 4*x1 + 5*x2 + n3 - p3 == 600
f4 = 2*x0 + 2*x1 + 6*x2 + n4 - p4 == 300

prob.constraints = [f1, f2, f3, f4]
prob.objective = [p2+p3+p4, n1]

prob.solve()

for key, val in prob.variables.iteritems():
   print "%s: %s" % (key, val.result)


