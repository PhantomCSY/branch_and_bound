def branch_and_bound(c, int_x, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
    import numpy as np
    from scipy.optimize import linprog
    import copy
    
    NF = [0]
    N = len(int_x)
    x_opt = []
    fun = []
    # upper bound of c.T*x
    F_u = float('inf')
    # lower bound of c.T*x
    F_l = float('inf')
    
    while len(NF) != 0:
        # Save whether the solution satisfies interger requirement, 1 for yes, 0 for no
        int_satisfy = [1] * N

        # 1. Solve relaxtion problem
        if NF[0] == 0:
            # This is the relaxtion of original problem
            res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, options=dict(bland=True, tol=1e-8))
        else:
            # Read additional bounds for sub-problem from NF
            num_of_bounds = len(NF[0][0])
            bounds_list = tuple2list(bounds)
            for i in range(num_of_bounds):
                index = NF[0][0][i]
                if NF[0][1][i][0] == 1:
                    if bounds_list[index][0] is None or NF[0][1][i][1] > bounds_list[index][0]:
                        bounds_list[index][0] = NF[0][1][i][1]
                else:
                    if bounds_list[index][1] is None or NF[0][1][i][1] < bounds_list[index][1]:
                        bounds_list[index][1] = NF[0][1][i][1]

            try:
                res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=list2tuple(bounds_list), options=dict(bland=True, tol=1e-8))
            except ValueError:
                NF.pop(0)
                if len(NF) == 0:
                    if len(x_opt) == 0:
                        print('No optimal solution')
                    else:
                        fun = np.dot(c.reshape([1, N]), x_opt.reshape([N, 1]))[0][0]
                        print('Optimal solution is: ', x_opt, 'Function value = ', fun)
                continue
                
        # 2. Check whether there exists a relaxed solution

        if res.status == 0:
            # Optimization successfully
            x_tmp = res.x
            F_l = res.fun
        else:
            F_l = float('inf')

        # 3. Branch and Bound
        if F_l < F_u:
            # Test whether the solution satisfies integer requirement
            for i in range(N):
                if int_x[i] == 1:
                    if abs(x_tmp[i]-round(x_tmp[i])) <= 1e-8:
                        x_tmp[i] = round(x_tmp[i])
                    else:
                        int_satisfy[i] = 0

            if sum(int_satisfy) != N:
                # When there exist variable that does not satisfy integer requirement
                index = int_satisfy.index(0)
                if NF[0] == 0:
                    NF.append([[index], [[-1, int(x_tmp[index])]]])
                    NF.append([[index], [[1, int(x_tmp[index])+1]]])
                else:
                    NF[0][0].append(index)
                    NF.append(copy.deepcopy(NF[0]))
                    NF.append(copy.deepcopy(NF[0]))
                    NF[-1][1].append([-1, int(x_tmp[index])])
                    NF[-2][1].append([1, int(x_tmp[index])+1])
            else:
                F_u = F_l
                x_opt = x_tmp

        # 4. Remove the solved relaxed sub-problem. Check if there remains sub-problems
        NF.pop(0)
        if len(NF) == 0:
            if len(x_opt) == 0:
#                 print('No optimal solution')
                pass
            else:
                fun = np.dot(c.reshape([1, N]), x_opt.reshape([N, 1]))[0][0]
#                 print('Optimal solution is: ', x_opt, 'Function value = ', fun)
                
    return (x_opt, fun)

def tuple2list(bounds):
    N = len(bounds)
    bounds_list = [None] * N
    for i in range(N):
        bounds_list[i] = list(bounds[i])
    return bounds_list

def list2tuple(bounds_list):
    N = len(bounds_list)
    bounds = [None] * N
    for i in range(N):
        bounds[i] = tuple(bounds_list[i])
    bounds = tuple(bounds)
    return bounds
