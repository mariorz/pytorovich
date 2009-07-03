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


prob = LpProblem("Standard Example", 'max')
x0 = prob.variable("x0")
x1 = prob.variable("x1")
x2 = prob.variable("x2")

prob.constraints = [
   x0 + x1 + x2 <= 100,
   10*x0 + 4*x1 + 5*x2 <= 600,
   2*x0 + 2*x1 + 6*x2 <= 300
]

prob.objective = [10*x0 + 6*x1 + 4*x2]

prob.solve()

for key, val in prob.variables.iteritems():
   print "%s: %s" % (key, val.result)
