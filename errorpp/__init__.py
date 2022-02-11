import sympy
import sympy.parsing.latex
import functools

delta = sympy.Function("Delta")

def propagate(eq, absolute = True):
    eq = sympy.simplify(eq)
    return _propagate(eq, absolute=absolute)

def _propagate(eq, absolute = True):
    if isinstance(eq, sympy.core.add.Add):
        return sympy.sqrt(functools.reduce(lambda a, b: a+_propagate(b, absolute=absolute)**2, (0,)+eq.args))
    elif isinstance(eq, sympy.core.mul.Mul):
        numbers = tuple(filter(lambda x: x.is_number, eq.args))
        if len(numbers):
            number = functools.reduce(lambda a, b: a*b, numbers)
        else:
            number = 1

        number = abs(number)
        print(number)
        others = tuple(filter(lambda x: not x.is_number, eq.args))
        if len(others) == 1:
            two = _propagate(others[0])

        else:
            two = sympy.sqrt(sum(map(lambda x: _propagate(x, absolute=absolute)**2/x**2, others)))
            three = functools.reduce(lambda a, b: a*b, others)
            if absolute:
                three = abs(three)
            two *= three
        
        return number*two

    elif isinstance(eq, sympy.core.power.Pow):
        return eq.args[1]*eq.args[0]**(eq.args[1]-1)*_propagate(eq.args[0], absolute=absolute)


    elif isinstance(eq, sympy.core.symbol.Symbol):
        return delta(eq)
    elif eq.is_number:
        return 0
    else:
        raise NotImplementedError(f'Function {eq} not suppored')

def propagate_latex(eq, absolute = True):
   
   pass

def proprate_steps(eq, absolute = True):
   # TODO
   pass

