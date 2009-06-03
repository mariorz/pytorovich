
import glpk

#TODO:
# choose better class names
# deletion of matrix is bad
# append does not work

class LinearProblem(object):
    def __init__(self, name=None, obj_dir='min'):
        
        self.lp = glpk.LPX()        
        self.name = self.lp.name = name
        self.obj_dir = obj_dir
        self._const_matrix = []
        self._obj_matrix = []
        self._constraints = []
        self._objectives = []
        self._vars = []
    
    def get_constraints(self):
        return self._constraints

    def set_constraints(self, constraints):
        self.del_constraints()
        for const in constraints:
            self._add_constraint(const)
        
    def del_constraints(self):
        self._constraints=[]
        del self.lp.rows[:]

    constraints = property(get_constraints, 
                          set_constraints, 
                          del_constraints)

    def get_objectives(self):
        return self._objectives

    def set_objectives(self, objectives):
        if isinstance(objectives, LinearVariable):
            objectives = [objectives]
        self.del_objectives()
        for pri in objectives:
            self._add_objective(pri)

    def del_objectives(self):
        self._objectives=[]
        self._obj_matrix = []
        
    objectives = property(get_objectives, 
                          set_objectives, 
                          del_objectives)


    def _add_constraint(self, eq):
        if isinstance(eq, LinearVariable):
            eq = LinearConstraint(eq)
        
        self._constraints.append(eq)
        count = len(self.lp.rows)
        self.lp.rows.add(1)
        row = self.lp.rows[count]

        try:
            row.name = eq[1]
            eq = eq[0]
        except:
            row.name = None

        if eq.constant is None or eq.constant == 0:
            print "eq: %s, constant;: %s" % (eq, eq.constant)

            
        if eq.rhseq == 'eq':
            row.bounds = -eq.constant, -eq.constant
        elif eq.rhseq == 'le':
            row.bounds = None, -eq.constant
        elif eq.rhseq == 'ge':
            row.bounds = -eq.constant, None
        else:
            print "WTFMFKWTF"
            

        for col in self.lp.cols:
            if col.name in eq:
                self._const_matrix.append(eq[col.name])
            else:
                self._const_matrix.append(0)

    def _add_objective(self, eq):
        if isinstance(eq, LinearVariable):
            eq = LinearEquation(eq)
        
        obj_row = []
        for col in self.lp.cols:
            if col.name in eq:
                obj_row.append(eq[col.name])
            else:
                obj_row.append(0)

        self._objectives.append(eq)
        self._obj_matrix.append(obj_row)

    def _copy_matrices(self):
        self.lp.matrix = self._const_matrix
        self.lp.obj[:] = self._obj_matrix[0]


    def variable(self, name, lower=None, upper=None):
        count = len(self.lp.cols)
        self.lp.cols.add(1)
        col = self.lp.cols[count]
        col.name = name
        col.bounds = lower, upper
        var = LinearVariable(name, lower, upper)
        self._vars.append(var)
        return var

    
    def solve(self):
        if self.obj_dir == 'min':
            self.lp.obj.maximize = False
        else:
            self.lp.obj.maximize = True
        for pri in self._objectives:
            self._copy_matrices()
            self.lp.simplex()
            count = len(self.lp.rows)
            self.lp.rows.add(1)
            objval = self.lp.obj.value
            self.lp.rows[count].bounds = objval, objval
            for n in self._obj_matrix[0]:
                self._const_matrix.append(n)
            #deletion of matrix is fucked up
            del self._obj_matrix[0]
            del self._objectives[0]

        for c in self.lp.cols:
            for var in self._vars:
                if c.name == var.name:
                    var.result = c.primal
    
    def display(self):
        print '; '.join('%s = %g' % (c.name, c.primal) for c in self.lp.cols)
                      

class LinearVariable(object):
    def __init__(self, name, lower=None, upper=None):
        self.name = name
        self.lower = lower
        self.upper = upper
        self.result = None
    
    def __add__(self, other):
        return LinearEquation(self) + other
    
    def __radd__(self, other):
        return LinearEquation(self) + other
    
    def __sub__(self, other):
        return LinearEquation(self) - other
    
    def __rsub__(self, other):
        return other - LinearEquation(self)
    
    def __mul__(self, other):
        return LinearEquation(self) * other
    
    def __rmul__(self, other):
        return LinearEquation(self) * other
    
    def __pos__(self):
        return self
    
    def __neg__(self):
        return LinearEquation(self) * -1
    
    def __eq__(self, other):
        return LinearEquation(self) == other


class LinearEquation(dict):
    def __init__(self, eq=None, rhseq=None):
        if isinstance(eq, LinearEquation):
            self.constant = eq.constant
            self.rhseq = rhseq
            dict.__init__(self, eq)
        elif isinstance(eq, LinearVariable):
            self.constant = 0
            self.rhseq = rhseq
            dict.__init__(self, {eq.name:1})
        else:
            self.constant = 0
            self.rhseq = rhseq
            dict.__init__(self)

    def __add__(self, other):
        eq = LinearEquation(self)
        #if other == 0.0: return eq
        if isinstance(other, int) or isinstance(other, float):
            eq.constant += other
        elif isinstance(other, LinearVariable):
            eq._addterm(other.name, 1)
        elif isinstance(other, LinearEquation):
            eq.constant += other.constant
            for v,x in other.iteritems():
                eq._addterm(v, x)
        return eq


    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        eq = LinearEquation()
        if isinstance(other, int) or isinstance(other, float):
            if other != 0:
                eq.constant = self.constant * other
                for v,x in self.iteritems():
                        eq[v] = x * other
        elif isinstance(other, LinearVariable):
            return self * LinearEquation(other)
        elif isinstance(other, LinearEquation):
            raise TypeError, "Non-constants cannot be multiplied in LP"
        return eq
    
    def __rmul__(self, other):
        return (self * other)
    
    def __eq__(self, other):
        return LinearEquation(self - other, 'eq')

    def __ge__(self, other):
        return LinearEquation(self - other, 'ge')

    def __le__(self, other):
        return LinearEquation(self - other, 'le')
       
    def __pos__(self):
        return self
        
    def __neg__(self):
        eq = LinearEquation(self)
        return eq * -1
    
    def _addterm(self, key, value):
        y = self.get(key, 0)
        if y:
            y += value
            if y: self[key] = y
            else: del self[key]
        else:
            self[key] = value


