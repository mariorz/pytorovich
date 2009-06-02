
import glpk


class LinearProblem(object):
    def __init__(self, name, objective='min'):
        self.lp = glpk.LPX()        
        self.lp.name = name
        self.objective = objective
        self._const_matrix = []
        self._pri_matrix = []
        self._constraints = []
        self._periorities = []
    
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

    def get_priorities(self):
        return self._priorities

    def set_priorities(self, priorities):
        self.del_priorities()
        for pri in priorities:
            self._add_priority(pri)

    def del_priorities(self):
        #why not del self._priorities?
        self._priorities=[]
        self._pri_matrix = []
        
    priorities = property(get_priorities, 
                          set_priorities, 
                          del_priorities)


    def _add_constraint(self, eq):
        if isinstance(eq, LinearVariable):
            eq = LinearEquation(eq)
        
        self._constraints.append(eq)
        count = len(self.lp.rows)
        self.lp.rows.add(1)
        row = self.lp.rows[count]

        try:
            #can it take names with spaces?
            row.name = eq[1]
            eq = eq[0]
        except:
            row.name = None

        row.bounds = -eq.constant, -eq.constant
        for col in self.lp.cols:
            if col.name in eq:
                self._const_matrix.append(eq[col.name])
            else:
                self._const_matrix.append(0)

    def _add_priority(self, eq):
        if isinstance(eq, LinearVariable):
            eq = LinearEquation(eq)
        self._priorities.append(eq)
        obj_row = []
        for col in self.lp.cols:
            if col.name in eq:
                obj_row.append(eq[col.name])
            else:
                obj_row.append(0)


        self._pri_matrix.append(obj_row)

    def _copy_matrices(self):
        self.lp.matrix = self._const_matrix
        self.lp.obj[:] = self._pri_matrix[0]


    def variable(self, name, lower=None, upper=None):
        count = len(self.lp.cols)
        self.lp.cols.add(1)
        col = self.lp.cols[count]
        col.name = name
        col.bounds = lower, upper
        var = LinearVariable(name, lower, upper)
        return var

    
    def solve(self):
        if self.objective == 'min':
            self.lp.obj.maximize = False
        else:
            self.lp.obj.maximize = True
        for pri in self._priorities:
            self._copy_matrices()
            self.lp.simplex()
            count = len(self.lp.rows)
            self.lp.rows.add(1)
            objval = self.lp.obj.value
            self.lp.rows[count].bounds = objval, objval
            for n in self._pri_matrix[0]:
                self._const_matrix.append(n)
            del self._pri_matrix[0]
            del self._priorities[0]
    
    def display(self):
        print '; '.join('%s = %g' % (c.name, c.primal) for c in self.lp.cols)
                      




class LinearVariable(object):
    def __init__(self, name, lower=None, upper=None):
        self.name = name
        self.lower = lower
        self.upper = upper
    
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
    def __init__(self, e=None, cons=0):
        if isinstance(e, LinearEquation):
            self.constant = e.constant
            dict.__init__(self, e)
        elif isinstance(e, LinearVariable):
            self.constant = 0
            dict.__init__(self, {e.name:1})
        else:
            self.constant = 0
            dict.__init__(self)

    def __add__(self, other):
        e = LinearEquation(self)
        if other is 0: return e
        if isinstance(other, int):
            e.constant += other
        elif isinstance(other, LinearVariable):
            e._addterm(other.name, 1)
        elif isinstance(other, LinearEquation):
            e.constant += other.constant
            for v,x in other.iteritems():
                e._addterm(v, x)
        return e


    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        e = LinearEquation()
        if isinstance(other, int):
            if other != 0:
                e.constant = self.constant * other
                for v,x in self.iteritems():
                        e[v] = x * other
        elif isinstance(other, LinearVariable):
            return self * LinearEquation(other)
        elif isinstance(other, LinearEquation):
            raise TypeError, "Non-constant expressions cannot be multiplied in LP"
        return e
    
    def __rmul__(self, other):
        return (self * other)
    
    def __eq__(self, other):
        return LinearEquation(self - other)
       

    def __pos__(self):
        return self
        
    def __neg__(self):
        e = LinearEquation(self)
        return e * -1
    
    def _addterm(self, key, value):
        y = self.get(key, 0)
        if y:
            y += value
            if y: self[key] = y
            else: del self[key]
        else:
            self[key] = value



