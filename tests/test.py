from distutils.log import error
import unittest

from pathlib import Path
import sys
from sympy import abc
import sympy
from sympy.parsing.latex import parse_latex

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
import errorpp

Delta = sympy.Function("Delta")
class TestCases(unittest.TestCase):

    def test_multiplication(self):
        eq = abc.a * abc.b * abc.c
        deq = errorpp.propagate(eq)
        teq = sympy.sqrt(Delta(abc.c)**2/abc.c**2 + Delta(abc.b)**2/abc.b**2 + Delta(abc.a)**2/abc.a**2)*sympy.Abs(abc.a*abc.b*abc.c)
        self.assertTrue(deq.equals(teq))

    def test_multiplication_absolute(self):
        eq = -2 * abc.a * abc.b * abc.c
        deq = errorpp.propagate(eq, absolute=False)
        print(deq)
        teq = 2 * sympy.sqrt(Delta(abc.c)**2/abc.c**2 + Delta(abc.b)**2/abc.b**2 + Delta(abc.a)**2/abc.a**2)*sympy.abc.a*abc.b*abc.c 
        self.assertTrue(deq.equals(teq)) 

if __name__ == '__main__':
    unittest.main()

