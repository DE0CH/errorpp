from re import L
import sympy
import sympy.parsing.latex
import functools
from sympy import abc

Delta = sympy.Function("Delta")


def delta_factory(absolute=True, depth=1):
    class ImplementedDeltaNoAbsolute(sympy.Function):
        @classmethod
        def eval(cls, x):
            return _propagate(x, absolute=absolute, depth=depth)
    return ImplementedDeltaNoAbsolute
    

def propagate(eq, absolute = True):
    return _propagate(eq, absolute=absolute)

def _propagate(eq, absolute = True, depth=float('inf')):
    if depth == 0: 
        return Delta(eq)
    depth -= 1
    if isinstance(eq, sympy.core.add.Add):
        return sympy.sqrt(functools.reduce(lambda a, b: a+b, map(lambda x: _propagate(x, absolute=absolute, depth=depth)**2, eq.args)))
    elif isinstance(eq, sympy.core.mul.Mul):
        numbers = tuple(filter(lambda x: x.is_number, eq.args))
        if len(numbers):
            number = functools.reduce(lambda a, b: a*b, numbers)
        else:
            number = 1

        number = abs(number)
        others = tuple(filter(lambda x: not x.is_number, eq.args))
        if len(others) == 1:
            two = _propagate(others[0], absolute=absolute, depth=depth)

        else:
            two = sympy.sqrt(sum(map(lambda x: _propagate(x, absolute=absolute, depth=depth)**2/x**2, others)))
            three = functools.reduce(lambda a, b: a*b, others)
            if absolute:
                three = abs(three)
            two *= three
        
        return number*two

    elif isinstance(eq, sympy.core.power.Pow):
        return eq.args[1]*eq.args[0]**(eq.args[1]-1)*_propagate(eq.args[0], absolute=absolute)


    elif isinstance(eq, sympy.core.symbol.Symbol):
        return Delta(eq)
    elif eq.is_number:
        return 0
    else:
        raise NotImplementedError(f'Function {eq} not suppored')

def propagate_latex(eq, absolute = True):
    eq = sympy.parsing.latex.parse_latex(eq)
    deq = propagate(eq)
    return sympy.latex(deq)

def propagate_steps(eq, absolute = True, step=1):
    prev = None
    eq = Delta(eq)
    while True:
        eq = eq.replace(Delta, delta_factory(absolute=absolute, depth=step))
        if eq != prev:
            yield eq
            prev = eq
        else:
            break
        

