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


Example problem:

http://www.cs.cornell.edu/~tomf/pyglpk/ex_ref.html

maximize Z = 10x0 + 6x1 + 4x2

subject to 	
        p = x0 + x1 + x2
	q = 10x0 + 4x1 + 5x2
	r = 2x0 + 2x1 + 6x2

and bounds of variables	




Standard form:
-----------------

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
prob.print_results()



Goal form:
-----------------

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
prob.print_results()

"""


#TO DO:

# doc
# check case when using inopt for integer solving
# report on candidate solutions when using MIP?


import glpk


__version__ = "0.1"
__date__ = "2009-06-02"
__maintainer__ = "mario romero"
__author__ = "Mario Romero (mario@romero.fm)"
__license__ = "GPL3"




class InputError(Exception):
    """
    Exception raised for errors in the input.
    
    Attributes:
       message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message



class LpProblem(object):
    def __init__(self, name=None, obj_dir='min'):
        self.lpx = glpk.LPX()        
        self.name = self.lpx.name = name
        self.obj_dir = obj_dir
        self.obj_vaule = None
        self._objective = []
        self._obj_matrix = []
        self._constraints = []
        self._const_matrix = []
        self._vars = {}
        self.status = self.lpx.status
   
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
            objective = [objective]
        elif isinstance(objective, LpEquation):
            objective = [objective]
        del self.objective
        for obj in objective:
            if isinstance(obj, LpVariable):
                obj = LpEquation(obj)
            self._objective.append(obj)

    def del_objective(self):
        self._objective = []
        self._obj_matrix = []
        
    
       
    objective = property(get_objective, 
                         set_objective, 
                         del_objective)

    

    def _get_name(self, eq):
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
        


    def _sync_matrices(self):
        for eq in self.constraints:
            if isinstance(eq, LpVariable):
                eq = LpEquation(eq)
            count = len(self.lpx.rows)
            self.lpx.rows.add(1)
            row = self.lpx.rows[count]
            row.name, eq = self._get_name(eq)
            self._set_row_bounds(row, eq.rhseq, -eq.constant)
            for col in self.lpx.cols:
                if col.name in eq:
                    self._const_matrix.append(eq[col.name])
                else:
                    self._const_matrix.append(0.0)

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
            
        self.lpx.matrix = self._const_matrix
        self.lpx.obj[:] = self._obj_matrix[0]


    def _sync_results(self):
        self.status = self.lpx.status
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
        count = len(self.lpx.rows)
        self.lpx.rows.add(1)
        objval = self.lpx.obj.value
        self.lpx.rows[count].bounds = objval, objval
        for n in self._obj_matrix[0]:
            self._const_matrix.append(n)
        del self._obj_matrix[0]
        #del self._objective[0]
    
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

    def solve(self):
        if len(self.objective) == 0:
            raise InputError("No objective set")
        if len(self.constraints) == 0:
            raise InputError("No constraints set")    

        self._sync_direction()
        mat = self._obj_matrix[:]
        obj = self._objective[:]
        
        for pri in self._objective:
            self._sync_matrices()
            self.lpx.simplex()
            for col in self.lpx.cols:
                if col.kind is int:
                    self.lpx.integer(callback=Callback())
                    break
            self.obj_value = self.lpx.obj.value
            self._obj_to_constraint()
            
            
        self._sync_results()
        self._obj_matrix = mat
        self._objective = obj
        

            
    def results_to_string(self):
        sorted_keys = self._vars.keys()
	sorted_keys.sort()
        sorted_keys.reverse()
        string = '\n'.join('%s = %s' % (key, self._vars[key].result) 
                        for key in sorted_keys)
        return string
        
    def constraints_to_string(self):
        string = ""
        for const in self.constraints:
            sorted_keys = const.keys()
            constant = const.constant
            rhseq = const.rhseq
            sorted_keys.sort()
            sorted_keys.reverse()
            string += ' + '.join('%s * %s' % (const[key], key) 
                        for key in sorted_keys)
            if rhseq == 'eq':
                string += ' == '
            elif rhseq == 'ge':
                string += ' >= '
            else:
                string += ' <= '

            string += ' %s' % -constant
            return string
    
    

    def objective_to_string(self):
        string = "[ "
        for obj in self.objective:
            sorted_keys = obj.keys()
            sorted_keys.sort()
            sorted_keys.reverse()
            string += ' + '.join('%s * %s' % (obj[key], key) 
                        for key in sorted_keys)
            string += ", "
        string = string[:-2]    
        string += " ]"
        return string
    
    def __repr__(self):
        string = ""
        string += "Problem Name: %s\n\n" % self.name
        string += "Minimize: %s\n\n" % self.objective_to_string()
        string += "Subject to:\n%s\n\n" % self.constraints_to_string()
        string += "Status: %s\n\n" % self.status
        string += "Results:\n"
        string += self.results_to_string() + "\n\n"
        
        #not print for goal problems?
        string += "Objective Value: %s" % self.obj_value

        return string


class Callback:
    def select(self, tree):
        # some code to select subproblems here...
        pass
    def prepro(self, tree):
        # some code for preprocessing here...
        pass
    def rowgen(self, tree):
        # some code for providing constraints here...
        pass
    def heur(self, tree):
        # some code for providing heuristic solutions here...
        pass
    def cutgen(self, tree):
        # some code for providing constraints here...
        pass
    def branch(self, tree):
        # some code to choose a variable to branch on here...
        pass
    def bingo(self, tree):
        # some code to monitor the situation her
        pass
        

                      

class LpVariable(object):
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




class LpEquation(dict):
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
        




