"""
-------------------------------------------------------------------
Copyright (C) 2009 Mario Romero, mario@romero.fm
This file is part of Pytorovich.

Pytorovich is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Pytorovich is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Pytorovich.  If not, see <http://www.gnu.org/licenses/>.
-------------------------------------------------------------------



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





Standard form:
------------------------
from pytorovich import LpProblem

prob = LpProblem("Standard Example", 'max')
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

for key, val in prob.variables.iteritems():
   "%s: %s" % (key, val.result)




Goal form:
------------------------

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
   "%s: %s" % (key, val.result)



------------------------
Knapsack Problem
Example from: 
http://xkcd.com/287/
------------------------
from pytorovich import LpProblem

prob = LpProblem("Integer Programming Problem")

items = ( ('MIXED FRUIT',   2.15),
          ('FRENCH FRIES',  2.75),
          ('SIDE SALAD',    3.35),
          ('HOT WINGS',     3.55),
          ('MOZZ STICKS',   4.20),
          ('SAMPLER PLATE', 5.80),
          ('BARBEQUE',      6.55) )

exactcost = 15.05

f = [prob.variable(item[0], 0, None, int) * 
     item[1] for item in items]

prob.objective = sum(f)
prob.constraints = sum(f) == exactcost
prob.solve()

for key, val in prob.variables.iteritems():
   "%s: %s" % (key, val.result)


"""




__version__ = "0.1"
__date__ = "2009-06-29"
__maintainer__ = "Mario Romero"
__author__ = "Mario Romero (mario@romero.fm)"
__license__ = "GPL3"


import glpk


# TO DO

# solve options


class InputError(Exception):
    """
    Exception raised for errors in the input.
    
    Attributes:
       message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message



class LpProblem(object):
    """
    A Linear Programming Problem

    Attributes:
       lpx -- pyglpk problem instance
       name -- problem name
       obj_dir -- objective function optimization direction
             -'min': minimize (default)
             -'max': maximize
       obj_value -- objective function value*
       status -- problem status
             -'opt': optimal   
             -'indef': indefinite
    
    
    Properties:
       variables -- LP Variables in problem instance
       constraints -- Problem constraints
       objective -- Problem objective(s)
    
    Private Attributes:
       _objective -- LP problem objective in dict form 
       _obj_matrix -- LP problem objective (vector form)
       _constraints -- Problem constraints (list of dicts) 
       _vars -- Problem vars declared

   """
    
    def __init__(self, name=None, obj_dir='min'):
        self.lpx = glpk.LPX()        
        self.name = self.lpx.name = name
        self.obj_dir = obj_dir
        self.obj_value = None
        self.status = self.lpx.status
        self._objective = []
        self._obj_matrix = []
        self._constraints = []
        self._vars = {}
        
   
    def get_variables(self):
        return self._vars

    variables = property(get_variables)
    
    
    def get_constraints(self):
        return self._constraints

    def set_constraints(self, constraints):
        if isinstance(constraints, LpVariable):
            constraints = [constraints]
        elif isinstance(constraints, LpEquation):
            constraints = [constraints]

        
        del self.constraints
        for const in constraints:
            self._constraints.append(const)
  
    def del_constraints(self):
        self._constraints = []
        
    
    constraints = property(get_constraints, 
                           set_constraints, 
                           del_constraints)

    def get_objective(self):
        return self._objective

    def set_objective(self, objective):
        if isinstance(objective, LpVariable):
            objective = [LpEquation(objective)]
        elif isinstance(objective, LpEquation):
            objective = [objective]
        del self.objective
        for obj in objective:
            self._objective.append(obj)

    def del_objective(self):
        self._objective = []
        self._obj_matrix = []
        
    
       
    objective = property(get_objective, 
                         set_objective, 
                         del_objective)


    def _get_name(self, eq):
        # if eq has a name set, it will be a touple
        # in which the first value is the actual
        # equation
         try:
            name = eq[1]
            eq = eq[0]
         except:
             name = None
         return name, eq
         
   
    def _set_row_bounds(self, row, rhseq, const):
        if rhseq == 'le':
            row.bounds = None, const
        elif rhseq == 'ge':
            row.bounds = const, None
        else:
            row.bounds = const, const
        


    def _sync_constraints(self, add_one=False):
        for eq in self.constraints:
            if isinstance(eq, LpVariable):
                eq = LpEquation(eq)
            
            rowid = self.lpx.rows.add(1)
            row = self.lpx.rows[rowid]
            row.name, eq = self._get_name(eq)
                     
            self._set_row_bounds(row, eq.rhseq, -eq.constant)
           
            # constraint matrix implementation of glpx object 
            # is spase e.g. [(0,4),(1,2),(3,0)... (n, 10]
            # LpEquation objects are also spase
            sparsemat = [term for term in eq.iteritems()]
            row.matrix = sparsemat
           
            
                    


    def _sync_objectives(self):
        for eq in self.objective:
            if isinstance(eq, LpVariable):
                eq = LpEquation(eq)
            obj_row = []
            for col in self.lpx.cols:
                if col.name in eq:
                    obj_row.append(eq[col.name])
                else:
                    obj_row.append(0.0)

                    
            self._obj_matrix.append(obj_row)
           
        self.lpx.obj[:] = self._obj_matrix[0]
        

        

    def _sync_results(self):
        self.status = self.lpx.status
        self.obj_vaule = self.lpx.obj.value
        for c in self.lpx.cols:
            self._vars[c.name].result = c.primal
    
    def _sync_direction(self):
        if self.obj_dir == 'min':
            self.lpx.obj.maximize = False
        else:
            self.lpx.obj.maximize = True
            
        
    
    def _obj_to_constraint(self):
        """
        Make consraint out of last solved objective
        """

        rowid = self.lpx.rows.add(1)
        objval = self.lpx.obj.value
        row = self.lpx.rows[rowid]
        row.bounds = objval, objval

        objiter = range(len(self._obj_matrix[0]))
        sparsemat = [(i,  self._obj_matrix[0][i]) for i in objiter]
        row.matrix = sparsemat     
        
        # delete the objective that has just been optimized
        # so that _sync_matrices(), copies the next objective
        # to the lpx objective matrix
        del self._obj_matrix[0]



    def variable(self, name, lower=None, upper=None, type=float):
        count = len(self.lpx.cols)
        self.lpx.cols.add(1)
        col = self.lpx.cols[count]
        col.name = name
        col.bounds = lower, upper
        col.kind = type
        var = LpVariable(self.lpx, name, lower, upper, type)
        self._vars[name] = var
        return var

    def solve(self, **kwds):
        if len(self.objective) == 0:
            raise InputError("No objective has been set.")
        if len(self.constraints) == 0:
            raise InputError("No constraints have been set.")    

        self._sync_direction()
        self._sync_objectives()

        cb = None
        if 'callback' in kwds:
            cb = kwds['callback']
        
        for pri in self._objective:
            self._sync_constraints(True)
                            
            method = None
            if 'method' in kwds:
                method = kwds['method']
            
            integer = None
            if 'integer' in kwds:
                integer = kwds['integer']
            
            if method == 'interior':
                self.lpx.interior()
            elif method == 'exact':
                self.lpx.exact()
            else:
                self.lpx.simplex()
            
            # FIX
            # this check fails if columns
            # are floats but the user
            # asks for an integer solution
            for col in self.lpx.cols:
                if col.kind is not float:
                    if integer == 'intopt':
                        self.lpx.intopt()
                    else:
                        self.lpx.integer(callback=cb)
                    break
                                    
            self.obj_value = self.lpx.obj.value
            self._obj_to_constraint()
            
        self._sync_results()
                

            
  

        

                      

class LpVariable(object):
    """
    A Linear Programming Variable

    Attributes:
       name -- variable name
       result -- optimal var value (None if unsolved)
       lp -- enclosing lp problem
    
    Properties:
       type -- variable type*
             -'float'
             -'int'
       lower -- var lower bound
       upper -- var upper bound

    """
    def __init__(self, lp, name, lower=None, upper=None, type='float'):
        self.name = name
        self.result = None
        self._lp = lp
        self._type = type
        self._lower = lower
        self._upper = upper
        
    def get_type(self):
        return self._type

    def set_type(self, type):
        #add check for non av types
        self._type = type
        self._sync_type()

    def del_type(self):
        #float is default type
        self._type = float

    
    type = property(get_type,
                     set_type,
                     del_type)


    
    def get_lower(self):
        return self._lower

    def set_lower(self, val):
        self._lower = val
        self._sync_bounds()

    def del_lower(self):
        self.lower = None

    
    lower = property(get_lower,
                     set_lower,
                     del_lower)

       
    def get_upper(self):
        return self._upper

    def set_upper(self, val):
        self._upper = val
        self._sync_bounds()

    def del_upper(self):
        self.upper = None


   
    upper = property(get_upper,
                     set_upper,
                     del_upper)


    def _sync_bounds(self):
        for col in self._lp.cols:
            if col.name == self.name:
                col.bounds = self.lower, self.upper
                break
    
    def _sync_type(self):
        for col in self._lp.cols:
            if col.name == self.name:
                col.type = self.type
                break

        
    def __add__(self, other):
        return LpEquation(self) + other
    
    def __radd__(self, other):
        return LpEquation(self) + other
    
    def __sub__(self, other):
        return LpEquation(self) - other
    
    def __rsub__(self, other):
        return other - LpEquation(self)
    
    def __mul__(self, other):
        return LpEquation(self) * other
    
    def __rmul__(self, other):
        return LpEquation(self) * other
    
    def __pos__(self):
        return self
    
    def __neg__(self):
        return LpEquation(self) * -1
    
    def __eq__(self, other):
        return LpEquation(self) == other

    def __ge__(self, other):
        return LpEquation(self) >= other

    def __le__(self, other):
        return LpEquation(self) <= other




class LpEquation(dict):
    """
    A Linear Equation

    Attributes:
       constant -- equation constant value
       rhseq -- right hand side equality symbol
             - 'ge': greater or equal (>=)
             - 'le': less or equal (<=)
             - 'eq': equal (==)
    """
    def __init__(self, eq=None, rhseq=None):
        if isinstance(eq, LpEquation):
            self.constant = eq.constant
            self.rhseq = rhseq
            dict.__init__(self, eq)
        elif isinstance(eq, LpVariable):
            self.constant = 0
            self.rhseq = rhseq
            dict.__init__(self, {eq.name:1})
        else:
            self.constant = 0
            self.rhseq = rhseq
            dict.__init__(self)

    def __add__(self, other):
        eq = LpEquation(self)
        if isinstance(other, int) or isinstance(other, float):
            eq.constant += other
        elif isinstance(other, LpVariable):
            eq._addterm(other.name, 1)
        elif isinstance(other, LpEquation):
            eq.constant += other.constant
            for var,val in other.iteritems():
                eq._addterm(var, val)
        return eq


    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        eq = LpEquation()
        if isinstance(other, int) or isinstance(other, float):
            eq.constant = self.constant * other
            for var,val in self.iteritems():
                eq[var] = val * other
        elif isinstance(other, LpVariable):
            return self * LpEquation(other)
        elif isinstance(other, LpEquation):
            raise TypeError, "Non-constants cannot be multiplied"
        return eq
    
    def __rmul__(self, other):
        return (self * other)
    
    def __eq__(self, other):
        return LpEquation(self - other, 'eq')

    def __ge__(self, other):
        return LpEquation(self - other, 'ge')

    def __le__(self, other):
        return LpEquation(self - other, 'le')
       
    def __pos__(self):
        return self
        
    def __neg__(self):
        eq = LpEquation(self)
        return eq * -1
    
    def _addterm(self, key, value):
        y = self.get(key, 0)
        y += value
        self[key] = y
        




