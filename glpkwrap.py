
import glpk


class GoalProblem(object):
    def __init__(self, name):
        self.lp = glpk.LPX()        
        self.lp.name = name     
        self.lp.obj.maximize = False
        self.matrix = []
        self.prios = []
        self.pri_matrix = []
    
    def variable(self, name, lower=None, upper=None):
        count = len(self.lp.cols)
        self.lp.cols.add(1)
        col = self.lp.cols[count]
        col.name = name
        col.bounds = lower, upper
        var = GoalVariable(name, lower, upper)
        return var
    
    def objective(self, eq):
        if isinstance(eq, GoalVariable):
            eq = GoalExpresion(eq)
        count = len(self.lp.rows)
        self.lp.rows.add(1)
        row = self.lp.rows[count]
        
        try:
            row.name = eq[1]
            eq = eq[0]
        except:
            pass
            
        
        row.bounds = -eq.constant, -eq.constant

        for col in self.lp.cols:
            if col.name in eq:
                self.matrix.append(eq[col.name])
            else:
                self.matrix.append(0)

    def priority(self, eq):
        if isinstance(eq, GoalVariable):
            eq = GoalExpresion(eq)
        self.prios.append(eq)
        obj_row = []
        for col in self.lp.cols:
            if col.name in eq:
                obj_row.append(eq[col.name])
            else:
                obj_row.append(0)
        self.pri_matrix.append(obj_row)

    def __copy_matrices__(self):
        self.lp.matrix = self.matrix
        self.lp.obj[:] = self.pri_matrix[0]
    
    def solve(self):
        for pri in self.prios:
            self.__copy_matrices__()
            self.lp.simplex()
            count = len(self.lp.rows)
            self.lp.rows.add(1)
            objval = self.lp.obj.value
            self.lp.rows[count].bounds = objval, objval
            for n in self.pri_matrix[0]:
                self.matrix.append(n)
            del self.pri_matrix[0]
            del self.prios[0]
    
    def display(self):
        print 'Z = %g;' % self.lp.obj.value
        print '; '.join('%s = %g' % (c.name, c.primal) for c in self.lp.cols)
                      




class GoalVariable(object):
    def __init__(self, name, lower=None, upper=None):
        self.name = name
        self.lower = lower
        self.upper = upper
    
    def __add__(self, other):
        return GoalExpresion(self) + other
    
    def __radd__(self, other):
        return GoalExpresion(self) + other
    
    def __sub__(self, other):
        return GoalExpresion(self) - other
    
    def __rsub__(self, other):
        return other - GoalExpresion(self)
    
    def __mul__(self, other):
        return GoalExpresion(self) * other
    
    def __rmul__(self, other):
        return GoalExpresion(self) * other
    
    def __pos__(self):
        return self
    
    def __neg__(self):
        return GoalExpresion(self) * -1
    
    def __eq__(self, other):
        return GoalExpresion(self) == other



class GoalExpresion(dict):
    def __init__(self, e=None, cons=0):
        if isinstance(e, GoalExpresion):
            self.constant = e.constant
            dict.__init__(self, e)
        elif isinstance(e, GoalVariable):
            self.constant = 0
            dict.__init__(self, {e.name:1})
        else:
            self.constant = 0
            dict.__init__(self)
    
    def __neg__(self):
        e = GoalExpresion(self)
        return e * -1

    def __add__(self, other):
        return self.addop(other)
    
    def __radd__(self, other):
        return self.addop(other)
    
    def __sub__(self, other):
        return self.addop(-other)
    
    def __rsub__(self, other):
        return (-self).addop(other)

    def __mul__(self, other):
        e = GoalExpresion()
        if isinstance(other, int):
            if other != 0:
                e.constant = self.constant * other
                for v,x in self.iteritems():
                        e[v] = x * other
        elif isinstance(other, GoalVariable):
            return self * GoalExpresion(other)
        elif isinstance(other, GoalExpresion):
            raise TypeError, "Non-constant expressions cannot be multiplied in LP"
        return e
    
    def __rmul__(self, other):
        return (self * other)
    
    def __eq__(self, other):
        return GoalObjective(self - other)
    
    def addop(self, other):
        e = GoalExpresion(self)
        if other is 0: return e
        if isinstance(other, int):
            e.constant += other
        elif isinstance(other, GoalVariable):
            e.addterm(other.name, 1)
        elif isinstance(other, GoalExpresion):
            e.constant += other.constant
            for v,x in other.iteritems():
                e.addterm(v, x)
        return e
    
    def addterm(self, key, value):
        y = self.get(key, 0)
        if y:
            y += value
            if y: self[key] = y
            else: del self[key]
        else:
            self[key] = value



class GoalObjective(GoalExpresion):
    def __init__(self, e=None):
        GoalExpresion.__init__(self, e)
    
    


class GoalPriority(object):
    pass



