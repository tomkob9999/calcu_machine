# calcu_machine
#
# Description: automatically calculates total derivatives from system of equations and then solve
# Version: 1.1.2
# Author: Tomio Kobayashi
# Last Update: 2024/3/27

import sympy as sp
import numpy as np
from itertools import combinations

class calcu_machine:
    def __init__(self, equations_str, targets, variables, is_silent=False):
        self.variables = variables
        self.targets = targets
        self.equations_str = equations_str
        self.equations = [sp.Eq(sp.sympify(eq), targets[i]) for i, eq in enumerate(self.equations_str)]
        self.is_silent = is_silent
        if not self.is_silent:
#             print("**************************")
            print("Given System of Equations:", self.equations)

    def chop_after_last_underscore(string):
        # Find the index of the last "_"
        last_underscore_index = string.rfind("_")

        # If no "_" found or it's the last character, return the original string
        if last_underscore_index == -1 or last_underscore_index == len(string) - 1:
            return string

        # Otherwise, chop the string after the last "_"
        chopped_string = string[:last_underscore_index]
        return chopped_string


    def solve_function(self, knowns):
        if len(knowns) != len(self.variables) - len(self.equations):
            print("Number of variables:", len(self.variables))
            print("Number of equations:", len(self.equations))
            print("Required number of known variables:", len(self.variables) - len(self.equations))
            return
        
        variables = sp.symbols(self.variables)
        eqs = [sp.Eq(sp.sympify(k), v) for k, v in knowns.items()]
        equations = self.equations + eqs
        if not self.is_silent:
            print("*")
            print("Calculated System of Equations:", equations)
        unknowns = [t for t in self.variables if t not in knowns]
        solution = sp.solve(equations, self.variables)
        
        if isinstance(solution, dict):
            derivs = [k for k, v in solution.items() if "_" in str(k)]
            if len(derivs) > 0:
                pair_combinations = list(combinations(derivs, 2))
                for p in [pair for pair in pair_combinations if str(pair[0]).split("_")[len(str(pair[0]).split("_"))-1] == str(pair[1]).split("_")[len(str(pair[1]).split("_"))-1]]:
                    solution[calcu_machine.chop_after_last_underscore(str(p[0])) + "_" + calcu_machine.chop_after_last_underscore(str(p[1]))] = solution[p[0]]/solution[p[1]]
                
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
            new_eq = sp.Eq(sp.sympify(new_equation), sp.sympify(der_target))
            self.equations.append(new_eq)
            if not self.is_silent:
                print("*")
                print("New Equation:", new_eq)
            self.targets.append(der_target)
