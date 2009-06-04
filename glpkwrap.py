
import glpk

#TODO:


# fix decimals in tests
# new class names
# append does not work
# fix display


class LinearProblem(object):
    def __init__(self, name=None, obj_dir='min'):
        self.lp = glpk.LPX()        
        self.name = self.lp.name = name
        self.obj_dir = obj_dir
        self._objective = []
        self._obj_matrix = []
        self._constraints = []
        self._const_matrix = []
        self._vars = {}
    
    def get_constraints(self):
        return self._constraints

    def set_constraints(self, constraints):
        del self.constraints
        for const in constraints:
            self._add_constraint(const)
        
    def del_constraints(self):
        self._constraints = []
        

    constraints = property(get_constraints, 
                          set_constraints, 
                          del_constraints)

    def get_objective(self):
        return self._objective

    def set_objective(self, objective):
        if isinstance(objective, LinearVariable):
            objective = [objective]
        elif isinstance(objective, LinearEquation):
            objective = [objective]
        del self.objective
        for obj in objective:
            self._add_objective(obj)

    def del_objective(self):
        self._objective = []
        self._obj_matrix = []
        
    objective = property(get_objective, 
                          set_objective, 
                          del_objective)


    def _add_constraint(self, eq):
        if isinstance(eq, LinearVariable):
            eq = LinearConstraint(eq)
        self._constraints.append(eq)
        count = len(self.lp.rows)
        self.lp.rows.add(1)
        row = self.lp.rows[count]
        row.name, eq = self._get_name(eq)
        self._set_row_bounds(row, eq.rhseq, -eq.constant)
        for col in self.lp.cols:
            if col.name in eq:
                self._const_matrix.append(eq[col.name])
            else:
                self._const_matrix.append(0.0)

    
    def _add_objective(self, eq):
        if isinstance(eq, LinearVariable):
            eq = LinearEquation(eq)
        obj_row = []
        for col in self.lp.cols:
            if col.name in eq:
                obj_row.append(eq[col.name])
            else:
                obj_row.append(0.0)
        self._objective.append(eq)
        self._obj_matrix.append(obj_row)

    

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
        self.lp.matrix = self._const_matrix
        self.lp.obj[:] = self._obj_matrix[0]


    def _sync_results(self):
        for c in self.lp.cols:
            self._vars[c.name].result = c.primal
    
    def _sync_direction(self):
        if self.obj_dir == 'min':
            self.lp.obj.maximize = False
        else:
            self.lp.obj.maximize = True
        
    
    def _obj_to_constraint(self):
        """
        Make consraint out of last solved objective
        """
        count = len(self.lp.rows)
        self.lp.rows.add(1)
        objval = self.lp.obj.value
        self.lp.rows[count].bounds = objval, objval
        for n in self._obj_matrix[0]:
            self._const_matrix.append(n)
        del self._obj_matrix[0]
        del self._objective[0]
        
        
    
    def variable(self, name, lower=None, upper=None):
        count = len(self.lp.cols)
        self.lp.cols.add(1)
        col = self.lp.cols[count]
        col.name = name
        col.bounds = lower, upper
        var = LinearVariable(name, lower, upper)
        self._vars[name] = var
        return var

    def solve(self):
        self._sync_direction()
        mat = self._obj_matrix[:]
        obj = self._objective[:]
        for pri in self._objective:
            self._sync_matrices()
            self.lp.simplex()
            self._obj_to_constraint()
        self._sync_results()
        self._obj_matrix = mat
        self._objective = obj
        
            
    
    def display(self):
        print '; '.join('%s = %s' % (n, r.result) 
                        for n,r in self._vars.iteritems())
                      

class LinearVariable(object):
    def __init__(self, name, lower=None, upper=None):
        self.name = name
        self.result = None
        self._lower = lower
        self._upper = upper
        
    
    def get_lower(self):
        return self._lower

    def set_lower(self, val):
        self._lower = val
        self._sync_bounds()

    def del_lower(self):
        self.lower = None

       
    def get_upper(self):
        return self._upper

    def set_upper(self, val):
        self._upper = val
        self._sync_bounds()

    def del_upper(self):
        self.upper = None


    lower = property(get_lower,
                     set_lower,
                     del_lower)

   
    upper = property(get_upper,
                     set_upper,
                     del_upper)


    def _sync_bounds(self):
        for col in self.lp.cols:
            if col.name == self.name:
                col.bounds = self.lower, self.upper
                break
    
        
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
        if isinstance(other, int) or isinstance(other, float):
            eq.constant += other
        elif isinstance(other, LinearVariable):
            eq._addterm(other.name, 1)
        elif isinstance(other, LinearEquation):
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
        eq = LinearEquation()
        if isinstance(other, int) or isinstance(other, float):
            eq.constant = self.constant * other
            for var,val in self.iteritems():
                eq[var] = val * other
        elif isinstance(other, LinearVariable):
            return self * LinearEquation(other)
        elif isinstance(other, LinearEquation):
            raise TypeError, "Non-constants cannot be multiplied"
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
        y += value
        self[key] = y
        

