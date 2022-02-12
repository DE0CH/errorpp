from distutils.log import error
from itertools import tee
import unittest
import random 
from pathlib import Path
import sys
from sympy import abc
import sympy
from sympy.parsing.latex import parse_latex

try:
    path_root = Path(__file__).parents[1]
    sys.path.append(str(path_root))
except IndexError:
    # Running tests for the package on pypi
    pass
import errorpp

Delta = sympy.Function("Delta")
class TestPropagate(unittest.TestCase):

    def test_multiplication(self):
        eq = 2 * abc.a * abc.b * abc.c
        deq = errorpp.propagate(eq, absolute=True)
        teq = sympy.sqrt(Delta(abc.c)**2/abc.c**2 + Delta(abc.b)**2/abc.b**2 + Delta(abc.a)**2/abc.a**2)*sympy.Abs(2*abc.a*abc.b*abc.c)
        self.assertEqual(deq, teq)

    def test_singleton(self):
        n = sympy.parse_expr('1')
        eq = sympy.Mul(n, abc.a, evaluate=False)
        deq = errorpp._propagate(eq, absolute=True)
        teq = Delta(abc.a)
        self.assertEqual(deq, teq)

    def test_singleton_absolute(self):
        n = sympy.parse_expr('1')
        eq = sympy.Mul(n, abc.a, evaluate=False)
        deq = errorpp.propagate(eq, absolute=False)
        teq = Delta(abc.a)
        self.assertEqual(deq, teq)

    def test_multiplication_absolute(self):
        eq = -2 * abc.a * abc.b * -abc.c
        deq = errorpp.propagate(eq, absolute=False)
        teq = 2 * sympy.sqrt(Delta(abc.c)**2/abc.c**2 + Delta(abc.b)**2/abc.b**2 + Delta(abc.a)**2/abc.a**2)*sympy.abc.a*abc.b*abc.c 
        self.assertEqual(deq, teq)

    def test_multiplication_absolute2(self):
        eq = eq = 2 * abc.a * abc.b * -abc.c
        deq = errorpp.propagate(eq, absolute=False)
        teq = 2 * sympy.sqrt(Delta(abc.c)**2/abc.c**2 + Delta(abc.b)**2/abc.b**2 + Delta(abc.a)**2/abc.a**2)*sympy.abc.a*abc.b*abc.c 
        self.assertEqual(deq, teq)

    def test_division(self):
        eq = -12 * abc.a * abc.b / abc.c / abc.d
        deq = errorpp.propagate(eq, absolute=True)
        teq = sympy.sqrt(Delta(abc.c)**2/abc.c**2 + Delta(abc.b)**2/abc.b**2 + Delta(abc.a)**2/abc.a**2 + Delta(abc.d)**2/abc.d**2) * sympy.Abs(-12 * abc.a * abc.b / abc.c / abc.d)
        self.assertEqual(deq, teq)

    def test_devision_absolute(self):
        eq = -12 * abc.a * -abc.b / abc.c / -abc.d
        deq = errorpp.propagate(eq, absolute=False)
        teq = 12 * sympy.sqrt(Delta(abc.c)**2/abc.c**2 + Delta(abc.b)**2/abc.b**2 + Delta(abc.a)**2/abc.a**2 + Delta(abc.d)**2/abc.d**2) * -12 * abc.a * abc.b / abc.c / abc.d 
        
    def test_addition(self): 
        eq = 1 + 2 + abc.a + abc.b + abc.c
        deq1 = errorpp.propagate(eq, absolute=True)
        deq2 = errorpp.propagate(eq, absolute=True) 
        teq = sympy.sqrt(Delta(abc.a)**2 + Delta(abc.b)**2 + Delta(abc.c)**2)
        self.assertEqual(deq1, teq)
        self.assertEqual(deq2, teq)

    def test_addition_absolute(self): 
        eq = -10 + abc.a - abc.b + abc.c
        deq1 = errorpp.propagate(eq, absolute=False)
        deq2 = errorpp.propagate(eq, absolute=False) 
        teq = sympy.sqrt(Delta(abc.a)**2 + Delta(abc.b)**2 + Delta(abc.c)**2)
        self.assertEqual(deq1, teq)
        self.assertEqual(deq2, teq)

    def test_power(self):
        eq = -17* abc.a**12
        deq = errorpp.propagate(eq, absolute=True)
        teq = 17*12*abc.a**11*Delta(abc.a)
        self.assertEqual(deq, teq)

    def test_power2(self):
        eq = 13 * abc.a**11.2
        deq = errorpp.propagate(eq, absolute=True)
        teq = 13*11.2*abc.a**10.2*Delta(abc.a)
        self.assertEqual(deq, teq)

    def test_power_absolute(self):
        eq = -17* abc.a**12
        deq = errorpp.propagate(eq, absolute=False)
        teq = 17*12*abc.a**11*Delta(abc.a)
        self.assertEqual(deq, teq)

    def test_power2_absolute(self):
        eq = 13 * abc.a**11.2
        deq = errorpp.propagate(eq, absolute=False)
        teq = 13*11.2*abc.a**10.2*Delta(abc.a)
        self.assertEqual(deq, teq)


    def sub(self, eq):
        a = abc.a
        b = abc.b
        c = abc.c
        d = abc.d
        eq = eq.subs(Delta(a), 13)
        eq = eq.subs(Delta(b), 17)
        eq = eq.subs(Delta(c), 23)
        eq = eq.subs(Delta(d), 27)
        eq = eq.subs(a, 3)
        eq = eq.subs(b, 5)
        eq = eq.subs(c, 7)
        eq = eq.subs(d, 11)
        return eq

    def sub2(self, eq):
        a = abc.a
        b = abc.b
        c = abc.c
        d = abc.d
        eq = eq.subs(Delta(a), -13)
        eq = eq.subs(Delta(b), -17)
        eq = eq.subs(Delta(c), -23)
        eq = eq.subs(Delta(d), -27)
        eq = eq.subs(a, -3)
        eq = eq.subs(b, -5)
        eq = eq.subs(c, -7)
        eq = eq.subs(d, -11)

    def sub3(self, eq):
        a = abc.a
        b = abc.b
        c = abc.c
        d = abc.d
        eq = eq.subs(Delta(a), -8.94510561376186)
        eq = eq.subs(Delta(b), 4.079451074836893)
        eq = eq.subs(Delta(c), 9.614255160251382)
        eq = eq.subs(Delta(d), -6.463977362260131)
        eq = eq.subs(a, 3.2731278704164097)
        eq = eq.subs(b, 9.221035394978145)
        eq = eq.subs(c, -1.069023616440468)
        eq = eq.subs(d, -0.3152866361678459)

    def test_complex(self):
        eq = ((abc.a+abc.b)*abc.c/abc.d)**3
        deq = errorpp.propagate(eq, absolute=False)
        teq = 3 * ((abc.a+abc.b)*abc.c/abc.d)**2 * errorpp.propagate((abc.a+abc.b)*abc.c/abc.d)

        self.assertAlmostEqual(self.sub(deq), self.sub(teq))

    def test_complex2(self):

        eq = (abc.c+abc.d)**3
        deq = errorpp.propagate(eq, absolute=False)
        teq = 3 * (abc.c+abc.d)**2 * errorpp.propagate(abc.c+abc.d)
    
        self.assertAlmostEqual(self.sub(deq), self.sub(teq))

    def test_complex3(self):
        eq = ((abc.a + abc.b)*abc.c/abc.d)
        deq = errorpp.propagate(eq, absolute=False)
        teq = sympy.sqrt(Delta(abc.d)**2/abc.d**2+Delta(abc.c)**2/abc.c**2+errorpp.propagate(abc.a+abc.b)**2/(abc.a+abc.b)**2)*eq
        self.assertAlmostEqual(self.sub(deq), self.sub(teq))

    def test_complex4(self):
        eq = ((abc.a+abc.b)*abc.c/abc.d)**3
        deq = errorpp.propagate(eq, absolute=True)
        teq = 3 * ((abc.a+abc.b)*abc.c/abc.d)**2 * errorpp.propagate((abc.a+abc.b)*abc.c/abc.d)

        self.assertAlmostEqual(self.sub2(deq), self.sub2(teq))
        self.assertAlmostEqual(self.sub3(deq), self.sub3(teq))

    def test_complex5(self):

        eq = (abc.c+abc.d)**3
        deq = errorpp.propagate(eq, absolute=True)
        teq = 3 * (abc.c+abc.d)**2 * errorpp.propagate(abc.c+abc.d)
    
        self.assertAlmostEqual(self.sub2(deq), self.sub2(teq))
        self.assertAlmostEqual(self.sub3(deq), self.sub3(teq))

    def test_complex6(self):
        eq = ((abc.a + abc.b)*abc.c/abc.d)
        deq = errorpp.propagate(eq, absolute=True)
        teq = sympy.sqrt(Delta(abc.d)**2/abc.d**2+Delta(abc.c)**2/abc.c**2+errorpp.propagate(abc.a+abc.b)**2/(abc.a+abc.b)**2)*eq
        self.assertAlmostEqual(self.sub2(deq), self.sub2(teq))
        self.assertAlmostEqual(self.sub3(deq), self.sub3(teq))

    def test_latex(self):
        deq = errorpp.propagate_latex('a + b')
        teq = r"\sqrt{\Delta^{2}{\left(a \right)} + \Delta^{2}{\left(b \right)}}"
        self.assertEqual(deq, teq)

    def test_steps(self):
        eq = ((abc.a+abc.b)*abc.c/abc.d)**3
        deq = None 
        for t in errorpp.propagate_steps(eq):
            deq = t
        teq = errorpp.propagate(eq)
        self.assertEqual(deq, teq)
    
    def test_steps2(self):
        """
        Does not have to pass, depending on the step implementation. 
        """
        eq = (abc.a+abc.b)*abc.c/abc.d
        deq = None
        for t in errorpp.propagate_steps(eq):
            deq = t
            break
        teq = sympy.sqrt(Delta(1/abc.d)**2*abc.d**2 + Delta(abc.c)**2/abc.c**2 + Delta(abc.a+abc.b)**2/(abc.a+abc.b)**2)*sympy.Abs(eq)
        self.assertEqual(deq, teq) 

    def test_step3(self):
        eq =((((abc.a+abc.b)*abc.c/abc.d)**3)+abc.d)*abc.a
        i = 3
        a = None
        for t in errorpp.propagate_steps(eq, step=1):
            if not i:
                break
            a = t
            i -= 1
        b = None 
        for t in errorpp.propagate_steps(eq, step=3):
            b = t
            break
        self.assertEqual(a, b)

    def test_delta_factory(self):
        eq = ((((abc.a+abc.b)*abc.c/abc.d)**3)+abc.d)*abc.a
        deq = None
        for i in errorpp.propagate_steps(eq):
            deq = i
            break
        deq = deq.replace(Delta, errorpp.delta_factory(depth=float('inf')))

        teq = errorpp.propagate(eq)
        self.assertEqual(deq, teq)

if __name__ == '__main__':
    unittest.main()

