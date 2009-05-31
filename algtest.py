
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







if __name__ == '__main__':
    unittest.main()   




