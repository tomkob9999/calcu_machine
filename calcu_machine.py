# calcu_machine
#
# Description: automatically calculates total derivatives from system of equations and then solve
# Version: 1.1.0
# Author: Tomio Kobayashi
# Last Update: 2024/3/27

import sympy as sp
import numpy as np

class calcu_machine:
    def __init__(self, equations_str, targets, variables):
        self.variables = variables
        self.targets = targets
        self.equations_str = equations_str
        self.equations = [sp.Eq(sp.sympify(eq), targets[i]) for i, eq in enumerate(self.equations_str)]
    def solve_function(self, knowns):
        if len(knowns) != len(self.variables) - len(self.equations):
            print("Number of variables:", len(self.variables))
            print("Number of equations:", len(self.equations))
            print("Required number of known variables:", len(self.variables) - len(self.equations))
            return
        
        variables = sp.symbols(self.variables)
        eqs = [sp.Eq(sp.sympify(k), v) for k, v in knowns.items()]
        equations = eqs + self.equations 
        unknowns = [t for t in self.variables if t not in knowns]
        solution = sp.solve(equations, self.variables)
        return solution
    
    def derive_derivatives(self):
        variables = sp.symbols(self.variables)
        num_knowns = len(self.variables) - len(self.equations)
        
        f = sp.sympify(self.equations_str[0])
        inputs = [self.variables[i] for i in range(num_knowns)]
        for v in variables:
            if str(v) in inputs:
                continue
            grads = []
            for inp in inputs:
                solution = sp.solve(f, v)
                str_sol = str(solution).replace("[", "").replace("]", "")
                fff = sp.sympify(str_sol)
                partial_derivative = sp.diff(fff, inp) 
                grads.append(partial_derivative)
            
            new_target_vars = []
            new_vars = []
            new_equation = ""
            for i, inp in enumerate(inputs):
                if i == 0:
                    der_target = str(v) + "_" + str(inp)
                    new_target_vars.append(der_target)
                    new_equation += str(grads[i])
                else:
                    der1 = str(v) + "_" + str(inp)
                    new_vars.append(der1)
                    new_equation += " + " + str(grads[i]) + "*" + der1
                    
                for n in new_target_vars:
                    self.variables.append(n)
                for n in new_vars:
                    self.variables.append(n)
                variables = sp.symbols(self.variables)
                self.equations.append(sp.Eq(sp.sympify(new_equation), sp.sympify(der_target)))
                self.targets.append(der_target)
        
equations = ["2 * x + 3 * y + 1 * z", "4 * x + 1 * y + 8 * z"]
targets = [20, 30]
calc = calcu_machine(equations, targets, ["x", "y", "z"]) 

s = calc.solve_function({"z": 3})
print(s)
calc.derive_derivatives()
s = calc.solve_function({"z": 5})
print(s)
s = calc.solve_function({"x": 15})
print(s)
s = calc.solve_function({"y": 33})
print(s)

    