[![Python Test](https://github.com/DE0CH/errorpp/actions/workflows/test.yml/badge.svg)](https://github.com/DE0CH/errorpp/actions/workflows/test.yml)
[![codecov Badge](https://codecov.io/gh/de0ch/errorpp/branch/master/graph/badge.svg)](https://codecov.io/gh/de0ch/errorpp)

# Automatic Error Propagation

When there are uncertainties in physics, you might need to deal with error propagation, which gets really annoying really really fast as the equation gets longer, especially if you need to write down the expression using variables for a school test or something. This package automates the process of propagating the error. 

## Installation

```bash
$ pip install errorpp
```

## Function and Scope 
As this is still being developed, the error propagation only supports expanding addition, multiplication, division and power of a real number. If you input anything else such as `sin(x)`, it will throw an error. If you want see more functions implemented, open an issue, or better yet, make a pull request!

## Usage
In its core, it uses `sympy` to process the expression. the `errorpp.propagate` function will take a `sympy` expression as the argument return the `sympy` expression with the error propagated. If your variables are all positive, you can pass in `absolute=False` to prevent the program from wrapping variables in absolute signs, which makes a cleaner output as `sympy` can cancel variables more easily.

You can also use the counterpart `errorpp.propagate_latex` which takes a string of latex expression as the argument and output the latex expression with the error propagated. 

Alternatively, you directly call this module from the terminal, which takes an latex equation as its first argument and print the latex expression with the error propagated to standard output. Use `--no-absolute` to prevent the program from wrapping variables in absolute sign.

Since the code base is quite small, I won't make a website with the documentation, but instead I will write the explanation in the docstring in the source code. 

## Code Example

You can use this directly in terminal
```bash
$ errorpp '\\frac{- c_{w} m_{1} \\left(- T_{1} + T_{f}\\right) + c_{w} m_{2} \\left(T_{2} - T_{f}\\right)}{- T_{1} + T_{f}}' --no-absolute
# output
# \frac{\sqrt{\frac{c_{w}^{2} m_{1}^{2} \left(- T_{1} + T_{f}\right)^{2} \left(\frac{\Delta^{2}{\left(T_{1} \right)} + \Delta^{2}{\left(T_{f} \right)}}{\left(- T_{1} + T_{f}\right)^{2}} + \frac{\Delta^{2}{\left(m_{1} \right)}}{m_{1}^{2}} + \frac{\Delta^{2}{\left(c_{w} \right)}}{c_{w}^{2}}\right) + c_{w}^{2} m_{2}^{2} \left(T_{2} - T_{f}\right)^{2} \left(\frac{\Delta^{2}{\left(T_{2} \right)} + \Delta^{2}{\left(T_{f} \right)}}{\left(T_{2} - T_{f}\right)^{2}} + \frac{\Delta^{2}{\left(m_{2} \right)}}{m_{2}^{2}} + \frac{\Delta^{2}{\left(c_{w} \right)}}{c_{w}^{2}}\right)}{\left(- c_{w} m_{1} \left(- T_{1} + T_{f}\right) + c_{w} m_{2} \left(T_{2} - T_{f}\right)\right)^{2}} + \frac{\Delta^{2}{\left(T_{1} \right)} + \Delta^{2}{\left(T_{f} \right)}}{\left(- T_{1} + T_{f}\right)^{2}}} \left(- c_{w} m_{1} \left(- T_{1} + T_{f}\right) + c_{w} m_{2} \left(T_{2} - T_{f}\right)\right)}{- T_{1} + T_{f}}
```

Or import this as a module
```python 
import errorpp
import sympy

eq = sympy.parse_latex('\\frac{- c_{w} m_{1} \\left(- T_{1} + T_{f}\\right) + c_{w} m_{2} \\left(T_{2} - T_{f}\\right)}{- T_{1} + T_{f}}')
p = errorpp.propagate(eq, absolute=False)
print(pretty(eq, use_unicode=False))

# Output
#          _____________________________________________________________________
#         /                         /     2             2             2         
#        /     2    2             2 |Delta (T_1) + Delta (T_f)   Delta (m_1)   D
#       /   c_w *m_1 *(-T_1 + T_f) *|------------------------- + ----------- + -
#      /                            |                  2                2       
#     /                             \      (-T_1 + T_f)              m_1        
#    /      --------------------------------------------------------------------
#   /                                                                           
# \/                                                                 (-c_w*m_1*(
# ------------------------------------------------------------------------------
#                                                                               
# 
# ______________________________________________________________________________
#     2     \                          /     2             2             2      
# elta (c_w)|      2    2            2 |Delta (T_2) + Delta (T_f)   Delta (m_2) 
# ----------| + c_w *m_2 *(T_2 - T_f) *|------------------------- + ----------- 
#       2   |                          |                  2                2    
#    c_w    /                          \       (T_2 - T_f)              m_2     
# ------------------------------------------------------------------------------
#                                   2                                           
# -T_1 + T_f) + c_w*m_2*(T_2 - T_f))                                            
# ------------------------------------------------------------------------------
#                                         -T_1 + T_f                            
# 
# ___________________________________________                                   
#        2     \                                                                
#   Delta (c_w)|                                                                
# + -----------|                                                                
#          2   |        2             2                                         
#       c_w    /   Delta (T_1) + Delta (T_f)                                    
# -------------- + ------------------------- *(-c_w*m_1*(-T_1 + T_f) + c_w*m_2*(
#                                    2                                          
#                        (-T_1 + T_f)                                           
# ------------------------------------------------------------------------------
#                                                                               
# 
#            
#            
#            
#            
#            
#            
# T_2 - T_f))
#            
#            
# -----------
# 
```