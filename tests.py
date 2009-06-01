
from glpkwrap import GoalProblem
import unittest


class AlgebraTest(unittest.TestCase):
    
  
    def test_sum_var_int(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 + 6
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f.constant, 6)

    def test_sum_int_var(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        f = 2 + x1
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f.constant, 2)


    def test_sum_exp_int(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 + 6
        g = f + 3
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g.constant, 9)


    def test_sum_int_exp(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        g = x1 + 4
        f = 2 + g
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f.constant, 6)

    def test_sum_var_exp(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + 6
        g = x2 + f 
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g[x2.name], 1)
        self.assertEqual(g.constant, 6)

    def test_sum_exp_var(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + 6
        g = f + x2 
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g[x2.name], 1)
        self.assertEqual(g.constant, 6)

    def test_sum_var_var(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + x2
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f[x2.name], 1)


    def test_sum_exp_exp(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        g = x1 + 4
        h = x2 + 3
        f = g + h
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f[x2.name], 1)
        self.assertEqual(f.constant, 7)


    def test_sub_var_int(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 - 3
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f.constant, -3)

    
    def test_sub_int_var(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        f = 8 - x1
        self.assertEqual(f[x1.name], -1)
        self.assertEqual(f.constant, 8)

    def test_sub_exp_int(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 + 6
        g = f - 3
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g.constant, 3)

    
    def test_sub_int_exp(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        g = x1 + 4
        f = 2 - g
        self.assertEqual(f[x1.name], -1)
        self.assertEqual(f.constant, -2)


    def test_sub_var_exp(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + 6
        g = x2 - f 
        self.assertEqual(g[x1.name], -1)
        self.assertEqual(g[x2.name], 1)
        self.assertEqual(g.constant, -6)

    def test_sub_exp_var(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + 6
        g = f - x2 
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g[x2.name], -1)
        self.assertEqual(g.constant, 6)
        
   
    def test_sub_var_var(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 - x2
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f[x2.name], -1)



    def test_sub_exp_exp(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        g = x1 + 4
        h = x2 + 3
        f = g - h
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f[x2.name], -1)
        self.assertEqual(f.constant, 1)
  

    def test_mult_var_int(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 * 2
        self.assertEqual(f[x1.name], 2)
        self.assertEqual(f.constant, 0)
        

    def test_mult_int_var(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        f = 2 * x1
        self.assertEqual(f[x1.name], 2)
        self.assertEqual(f.constant, 0)

    def test_mult_exp_int(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        g = x1 + 2
        f = g * 7
        self.assertEqual(f[x1.name], 7)
        self.assertEqual(f.constant, 14)
        

    def test_mult_int_exp(self):
        prob = GoalProblem('unit test')
        x1 = prob.variable("x1",0)
        g = x1 + 4
        f = 2 * g
        self.assertEqual(f[x1.name], 2)
        self.assertEqual(f.constant, 8)




class ProbCasesTest(unittest.TestCase):
    
  
    def test_paint_case(self):
        
        """
        Status: Optimal
        LatexPaint = 4.0
        EmanelPaint = 0.0
        p1 = 0.0
        n1 = 0.0
        p2 = 0.0
        n2 = 600.0
        p3 = 0.0
        n3 = 7.0
        """
        prob = GoalProblem("The Paint Company Problem")
        x1 = prob.variable("LatexPaint",0)
        x2 = prob.variable("EmanelPaint",0)
        n1 = prob.variable("n1",0)
        n2 = prob.variable("n2",0)
        n3 = prob.variable("n3",0)
        p1 = prob.variable("p1",0)
        p2 = prob.variable("p2",0)
        p3 = prob.variable("p3",0)
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
        results = {}
        for c in prob.lp.cols:
            results[c.name] = c.primal
        latex = results['LatexPaint']
        emanel = results['EmanelPaint']
        self.assertEqual(latex, 4)
        self.assertEqual(emanel,0)


    def test_pyglpk_example_case(self):
        """
        http://www.cs.cornell.edu/~tomf/pyglpk/ex_ref.html
        
        RESULTS:
        Z = 733.333; x0 = 33.3333; x1 = 66.6667; x2 = 0
        """

        prob = GoalProblem("Goal Programming Test Problem")
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
        prob.objective(f1)
        prob.objective(f2)
        prob.objective(f3)
        prob.objective(f4)
        prob.priority(p2+p3+p4)
        prob.priority(n1)
        prob.solve()
        self.assertEqual(x0, 33.3333)
        self.assertEqual(x1,66.6667)
        self.assertEqual(x2,0)


    def test_ignizio_example_case(self):
        """
        OPTIMAL SOLUTION FOUND
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
        f1 = x1 + x2 + n1 - p1 == 10
        f2 = x1 + n2 - p2 == 4
        f3 = 5*x1 + 3*x2 + n3 - p3 == 56
        o1 = prob.objective(f1)
        o2 = prob.objective(f2)
        o3 = prob.objective(f3)
        g1 = 2*p1 + 3*p2
        g2 = n3
        P1 = prob.priority(g1)
        P2 = prob.priority(g2)
        prob.solve()
        self.assertEqual(x1,4.0)
        self.assertEqual(x2,6.0)


if __name__ == '__main__':
    unittest.main()   




