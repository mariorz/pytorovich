
from glpkwrap import LinearProblem
import unittest



class AlgebraTest(unittest.TestCase):
    
  
    def test_sum_var_int(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 + 6
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f.constant, 6)

    def test_sum_int_var(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        f = 2 + x1
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f.constant, 2)


    def test_sum_exp_int(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 + 6
        g = f + 3
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g.constant, 9)


    def test_sum_int_exp(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        g = x1 + 4
        f = 2 + g
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f.constant, 6)

    def test_sum_var_exp(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + 6
        g = x2 + f 
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g[x2.name], 1)
        self.assertEqual(g.constant, 6)

    def test_sum_exp_var(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + 6
        g = f + x2 
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g[x2.name], 1)
        self.assertEqual(g.constant, 6)

    def test_sum_var_var(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + x2
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f[x2.name], 1)


    def test_sum_exp_exp(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        g = x1 + 4
        h = x2 + 3
        f = g + h
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f[x2.name], 1)
        self.assertEqual(f.constant, 7)


    def test_sub_var_int(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 - 3
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f.constant, -3)

    
    def test_sub_int_var(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        f = 8 - x1
        self.assertEqual(f[x1.name], -1)
        self.assertEqual(f.constant, 8)

    def test_sub_exp_int(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 + 6
        g = f - 3
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g.constant, 3)

    
    def test_sub_int_exp(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        g = x1 + 4
        f = 2 - g
        self.assertEqual(f[x1.name], -1)
        self.assertEqual(f.constant, -2)


    def test_sub_var_exp(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + 6
        g = x2 - f 
        self.assertEqual(g[x1.name], -1)
        self.assertEqual(g[x2.name], 1)
        self.assertEqual(g.constant, -6)

    def test_sub_exp_var(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 + 6
        g = f - x2 
        self.assertEqual(g[x1.name], 1)
        self.assertEqual(g[x2.name], -1)
        self.assertEqual(g.constant, 6)
        
   
    def test_sub_var_var(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        f = x1 - x2
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f[x2.name], -1)



    def test_sub_exp_exp(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        g = x1 + 4
        h = x2 + 3
        f = g - h
        self.assertEqual(f[x1.name], 1)
        self.assertEqual(f[x2.name], -1)
        self.assertEqual(f.constant, 1)
  

    def test_mult_var_int(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        f = x1 * 2
        self.assertEqual(f[x1.name], 2)
        self.assertEqual(f.constant, 0)
        

    def test_mult_int_var(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        f = 2 * x1
        self.assertEqual(f[x1.name], 2)
        self.assertEqual(f.constant, 0)

    def test_mult_exp_int(self):
        prob = LinearProblem('unit test')
        x1 = prob.variable("x1",0)
        g = x1 + 2
        f = g * 7
        self.assertEqual(f[x1.name], 7)
        self.assertEqual(f.constant, 14)
        

    def test_mult_int_exp(self):
        prob = LinearProblem('unit test')
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
        prob = LinearProblem("The Paint Company Problem")
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
        prob.constraints = f1
        prob.constraints.append(f2)
        prob.constraints.append(f3)
        prob.objective = [p1, n2, n3]
        prob.solve()
        self.assertEqual(x1.result, 4)
        self.assertEqual(x2.result,0)


    def test_pyglpk_StdExample_case(self):
        """
        http://www.cs.cornell.edu/~tomf/pyglpk/ex_ref.html
        
        RESULTS:
        x0 = 33.3333; x1 = 66.6667; x2 = 0
        """

        prob = LinearProblem("Linear Programming Test Problem", 'max')
        x0 = prob.variable("x0",0)
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        prob.constraints = [
            x0 + x1 + x2 <= 100,
            10*x0 + 4*x1 + 5*x2 <= 600,
            2*x0 + 2*x1 + 6*x2 <= 300
            ]
        prob.objective = [10*x0 + 6*x1 + 4*x2]
        prob.solve()
        
        self.assertEqual(round(x0.result, 3), 33.333)
        self.assertEqual(round(x1.result, 3), 66.667)
        


    def test_pyglpk_GoalExample_case(self):
        """
        http://www.cs.cornell.edu/~tomf/pyglpk/ex_ref.html
        
        RESULTS:
        x0 = 33.3333; x1 = 66.6667; x2 = 0
        """

        prob = LinearProblem("Linear Programming Test Problem")
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
        
        self.assertEqual(round(x0.result, 3), 33.333)
        self.assertEqual(round(x1.result, 3), 66.667)


    def test_ignizio_example_case(self):
        """
        OPTIMAL SOLUTION FOUND
        Status: Optimal
        x1 = 4.0
        x2 = 6.0
        objective function:  18.0

        """
        prob = LinearProblem("Linear Programming Test Problem")
        x1 = prob.variable("x1",0)
        x2 = prob.variable("x2",0)
        n1 = prob.variable("n1",0)
        n2 = prob.variable("n2",0)
        n3 = prob.variable("n3",0)
        p1 = prob.variable("p1",0)
        p2 = prob.variable("p2",0)
        p3 = prob.variable("p3",0)
        f1 = x1 + x2 + n1 - p1 == 10, "some name"
        f2 = x1 + n2 - p2 == 4
        f3 = 5*x1 + 3*x2 + n3 - p3 == 56
        prob.constraints = [f1, f2, f3]
        prob.objective = [2*p1 + 3*p2,n3]
        prob.solve()
        self.assertEqual(x1.result, 4.0)
        self.assertEqual(x2.result, 6.0)



    def test_stdform_example_case(self):
        """
        Status: Optimal
        ChickenPercent = 33.3333
        BeefPercent = 66.6667
        Total Cost of Ingredients per can =  0.9666665
        """
        prob = LinearProblem()
        x1 = prob.variable("x1", 0)
        x2 = prob.variable("x2", 0)
        prob.objective = 0.013*x1 + 0.008*x2
        prob.constraints = [
            x1 + x2 == 100, 
            0.10*x1 + 0.20*x2  >= 8,
            0.080*x1 + 0.100*x2 >= 6,
            0.001*x1 + 0.005*x2 <= 2,
            0.002*x1 + 0.005*x2 <= 0.4
            ]
        prob.solve()
        
        self.assertEqual(round(x1.result, 3), 33.333)

        self.assertEqual(round(x2.result, 3), 66.667)

    
    
    def test_ignizio2_case(self):
        """
        pass
        """
        prob = LinearProblem()
        x1 = prob.variable("x1", 0)
        x2 = prob.variable("x2", 0)
        
        p1 = prob.variable("p1", 0)
        p2 = prob.variable("p2", 0)
        p3 = prob.variable("p3", 0)
        p4 = prob.variable("p4", 0)
        
        n1 = prob.variable("n1", 0)
        n2 = prob.variable("n2", 0)
        n3 = prob.variable("n3", 0)
        n4 = prob.variable("n4", 0)
              
        prob.constraints = [
            8*x1 + 12*x2 + n1 - p1 == 1000,
            x1 + 2*x2 + n2 - p2 == 40,
            x1 + n3 - p3 == 30,
            x2 + n4 - p4 == 15
            ]
        prob.objective = [(p3+p4), n1, p2, (1.5*n4 + n3)]
        prob.solve()
        self.assertEqual(x1.result, 30)
        self.assertEqual(x2.result, 15)
       
        

    def test_birdsong_case(self):
        """
        pass
        """
        prob = LinearProblem()
        x1 = prob.variable("x1", 0)
        x2 = prob.variable("x2", 0)
        x3 = prob.variable("x3", 0)
        x4 = prob.variable("x4", 0)
        
        p1 = prob.variable("p1", 0)
        p2 = prob.variable("p2", 0)
        p3 = prob.variable("p3", 0)
        p4 = prob.variable("p4", 0)
        p5 = prob.variable("p4", 0)
        p6 = prob.variable("p6", 0)
        p7 = prob.variable("p7", 0)
       
        n1 = prob.variable("n1", 0)
        n2 = prob.variable("n2", 0)
        n3 = prob.variable("n3", 0)
        n4 = prob.variable("n4", 0)
        n5 = prob.variable("n5", 0)
        n6 = prob.variable("n6", 0)
        n7 = prob.variable("n7", 0)
       
        f1 = x1 + x2 + x3 + x4 + n1 - p1 == 50000, "profit"
        f2 = x1 + n2 - p2 == 20000, "assembly hours"
        f3 = x2 + n3 - p3 == 5000, "demand deluxe"
        f4 = x2 + n4 - p4 == 15000, "demand supreme"
        f5 = x3 + n5 - p5 == 10000, "foobar"
        f6 = x4 + n6 - p6 == 30000, "barfoo"
        f7 = .06*x1 + .05*x2 +.08*x3 + .07*x4 + n7 - p7 == 4000, "dsds"

        prob.constraints = [f1,f2,f3,f4,f5,f6,f7]
        prob.objective = p1
        prob.objective.append(n2 + 2*n3 + 2*p4)
        prob.objective.append(n6)
        prob.objective.append(p5 + n7)
        prob.solve()
        
        self.assertEqual(x1.result, 20000.0)
        self.assertEqual(x2.result, 5000.0)
        self.assertEqual(x3.result, 0.0)
        self.assertEqual(x4.result, 25000.0)

    

    def test_class1_case(self):
        """
        pass
        """
        prob = LinearProblem()
        x1 = prob.variable("x1", 0, 6)
        x2 = prob.variable("x2", 0)
        
        p1 = prob.variable("p1", 0)
        p2 = prob.variable("p2", 0)

        n1 = prob.variable("n1", 0)
        n2 = prob.variable("n2", 0)

        prob.constraints = [
            x1 + 2*x2 <= 10,
            4*x1 + 8*x2 + n1 - p1 == 45,
            8*x1 + 24*x2 + n2 - p2 == 100
            ]
        
        prob.objective = 2*n1 + p2
        prob.solve()
        prob.print_results()


    def test_class2_case(self):
        """
        pass
        """
        prob = LinearProblem()
        x1 = prob.variable("x1", 0, 6)
        x2 = prob.variable("x2", 0)
        
        p1 = prob.variable("p1", 0)
        p2 = prob.variable("p2", 0)
        p3 = prob.variable("p3", 0)
        p4 = prob.variable("p4", 0)

        n1 = prob.variable("n1", 0)
        n2 = prob.variable("n2", 0)
        n3 = prob.variable("n3", 0)
        n4 = prob.variable("n4", 0)

        prob.constraints = [
            7*x1 + 3*x2 + n1 - p1 == 40,
            10*x1 + 5*x2 + n2 - p2 == 60,
            5*x1 + 4*x2 + n3 - p3 == 35,
            100*x1 + 60*x2  <= 600
            ]
        
        prob.objective = 200*n1 + 100*n2 + 50*n3
        prob.solve()
        prob.print_results()
        
if __name__ == '__main__':
    unittest.main()   




