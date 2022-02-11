import sympy
import functools

delta = sympy.Function("Delta")

def propagate(eq, absolute = True):
    if isinstance(eq, sympy.core.add.Add):
        return sympy.sqrt(functools.reduce(lambda a, b: a+propagate(b, absolute=absolute)**2, (0,)+eq.args))
    elif isinstance(eq, sympy.core.mul.Mul):
        return sympy.sqrt(functools.reduce(lambda a, b: a+(propagate(b, absolute=absolute)/b)**2, (0,)+eq.args))*(abs(eq) if absolute or eq.is_number else eq)
    elif isinstance(eq, sympy.core.power.Pow):
        return eq.args[1]*eq.args[0]**(eq.args[1]-1)*propagate(eq.args[0], absolute=absolute)
    elif isinstance(eq, sympy.core.symbol.Symbol):
        return delta(eq)
    elif eq.is_number:
        return 0
    else:
        raise NotImplementedError(f'Function {eq} not suppored')
def propagate_latex(eq, absolute = True):
   # TODO
   pass

def proprate_steps(eq, absolute = True):
   # TODO
   pass

