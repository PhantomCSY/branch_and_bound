# branch_and_bound
This program aims at applying branch &amp; bound algorithm to solve ILP problem in Python. 

Please note the function is built on Python 3.x and rely on SciPy and Numpy.

To use the function, simply import it from the file:
import branch_and_bound from branch_and_bound

Usage:
(x, fun) = branch_and_bound(c, int_x, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None)

int_x: Array-like, an array with 0-1 elements, where 1 represents the variable is integer, and 0 represents no integer constraint. Ex: [1, 1, 0] states the first 2 variables must be integer, but the third variable can be either integer or continuous.

c, A_ub, b_ub, A_eq, b_eq, bounds share the same defination as SciPy.optimize.linprog, which can be viewed here: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
