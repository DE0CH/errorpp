from email.generator import Generator
import sympy
import sympy.parsing.latex
import functools
from typing import Generator

Delta = sympy.Function("Delta")

def delta_factory(absolute: int=True, depth: int=1) -> sympy.Function:
    """
    Creates a subclass of `sympy.Function` that implements the delta function with the recursive error propagation.

    Parameters
    ==========
    eq: sympy.Expr
        The expression for which to propagate the error.
    absolute: bool, optional 
        If set to False, it will will assume all the symbols are positive and skip wrapping them with absolute sign which makes simplification simpler. 
    depth: int, optional
        The depth for the recursion, when the recursion depth is matched, the expression will be wrapped in a placeholder Delta function and returned. This is useful for showing the steps of the propagation.


    Examples
    ========
    >>> eq = ...
    >>> Delta = sympy.Function("Delta")
    >>> deq = errorpp.propagate(eq)
    >>> teq = Delta(eq).replace(Delta, errorpp.delta_factory(depth=float('inf')))
    >>> deq == teq
    # True
    """

    class ImplementedDeltaNoAbsolute(sympy.Function):
        @classmethod
        def eval(cls, x):
            return _propagate(x, absolute=absolute, depth=depth)
    return ImplementedDeltaNoAbsolute
    

def propagate(eq: sympy.Expr, absolute: bool=True) -> sympy.Expr:
    """
    Propagate the error in the expression, assuming every variable has an error. 
    
    Parameters
    ==========
    eq: sympy.Expr
        The expression for which to propagate the error.
    absolute: bool, optional 
        If set to False, it will will assume all the symbols are positive and skip wrapping them with absolute sign which makes simplification simpler. 
    
    """
    return _propagate(eq, absolute=absolute)

def _propagate(eq: sympy.Expr, absolute: bool=True, depth: int=float('inf')) -> sympy.Expr:
    """
    Internal Recursive Function to handle propagation. `propagate` is more userfriendly. 

    Parameters
    ==========
    eq: sympy.Expr
        The expression for which to propagate the error.
    absolute: bool, optional 
        If set to False, it will will assume all the symbols are positive and skip wrapping them with absolute sign which makes simplification simpler. 
    depth: int, optional
        The depth for the recursion, when the recursion depth is matched, the expression will be wrapped in a placeholder Delta function and returned. This is useful for showing the steps of the propagation.
    
    """
    if depth <= 0: 
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
        raise NotImplementedError(f'Function {eq} is not suppored')

def propagate_latex(eq: str, absolute = True) -> str:
    """
    Propagate the error in the expression, assuming every variable has an error. 
    
    Parameters
    ==========
    eq: str
        The expression for which to propagate the error, written in latex.
    absolute: bool, optional 
        If set to False, it will will assume all the symbols are positive and skip wrapping them with absolute sign which makes simplification simpler. 
        """
    
    eq = sympy.parsing.latex.parse_latex(eq)
    deq = propagate(eq)
    return sympy.latex(deq)

def propagate_steps(eq: sympy.Expr, absolute: bool=True, step: int=1) -> Generator[sympy.Expr, None, None]:
    """
    Propagate the error one `step` at time. This is useful for showing the steps of error propagation. 

    Parameters 
    ==========
    eq: sympy.Expr
        The expression for which to propagate the error.
    absolute: bool, optional 
        If set to False, it will will assume all the symbols are positive and skip wrapping them with absolute sign which makes simplification simpler. 
    step: int, optional
        The number of steps to carry out in each iteration. 
    
    Examples
    ========
    >>> eq == ..
    >>> for t in errorpp.propagate_steps(eq):
    ...     print(t) # This is the expression for the step
    
    """

    prev = None
    eq = Delta(eq)
    while True:
        eq = eq.replace(Delta, delta_factory(absolute=absolute, depth=step))
        if eq != prev:
            yield eq
            prev = eq
        else:
            break
        

