# calculu_machine
#
# Description: automatically calculates total derivatives from system of equations and then solve
# Version: 1.2.0
# Author: Tomio Kobayashi
# Last Update: 2024/3/31

import sympy as sp
import numpy as np
from itertools import combinations

class calculu_machine:
    
    def __init__(self, equations_str, targets, variables, is_silent=False):
        self.variables = variables
        self.targets = targets
        self.equations_str = equations_str
        self.equations = [sp.Eq(sp.sympify(eq), sp.sympify(targets[i])) for i, eq in enumerate(self.equations_str)]
        self.is_silent = is_silent
        if not self.is_silent:
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
        eqs = [sp.Eq(v, sp.sympify(k)) for k, v in knowns.items()]
        equations = self.equations + eqs
        if not self.is_silent:
            print("*")
            print("Calculated System of Equations:", equations)
        unknowns = [t for t in self.variables if t not in knowns]
        
        try:
#             print("Solving for", self.variables)
            solution = sp.solve(equations, self.variables)
            if len(solution) == 0:
                print("No solution found")
            elif isinstance(solution, dict):
                derivs = [k for k, v in solution.items() if "_" in str(k)]
                if len(derivs) > 0:
                    pair_combinations = list(combinations(derivs, 2))
                    for p in [pair for pair in pair_combinations if str(pair[0]).split("_")[len(str(pair[0]).split("_"))-1] == str(pair[1]).split("_")[len(str(pair[1]).split("_"))-1]]:
                        solution[calculu_machine.chop_after_last_underscore(str(p[0])) + "_" + calculu_machine.chop_after_last_underscore(str(p[1]))] = solution[p[0]]/solution[p[1]]
                solution = [solution]
            elif len(self.variables) == len(solution[0]):
                sols = []
                for ss in solution:
                    sol = {}
                    for i, s in enumerate(ss):
                        sol[self.variables[i]] = s
                    sols.append(sol)
                solution = sols
                
            return solution
        
        except NotImplementedError as e:
            print(f"Caught an error: {e}")
            return None
   
     
 
    def derive_derivatives(self, tot_deriv_input=[]):

        variables = sp.symbols(self.variables)
        num_knowns = len(self.variables) - len(self.equations)
        if len(tot_deriv_input) != 0 and len(tot_deriv_input) != num_knowns:
            print("Number of derived input params must be", num_knowns)

        function_sets = [(tuple(f), tuple([v for v in variables if v not in f])) for f in list(combinations(variables, num_knowns))]
        
        total_notyet = True
        for i, func in enumerate(function_sets):
            new_variables = []
            new_equations = []
            add_equation = any([str(f) in tot_deriv_input for f in func[0]])
            
            solution = sp.solve(self.equations, func[1]) 
            str_sol = str(solution).replace("[", "").replace("]", "")
            gradiants = {}
            not_too_complex = True
            if str_sol != "":
                for inp in func[0]:
                    if str_sol == "":
                        continue
                    else:
                        fff = sp.sympify(str_sol)
                        if isinstance(fff, dict):
                            for k, v in fff.items():
                                p = sp.diff(v, inp)
                                if not self.is_silent:
                                    print("partial derivative d" + str(k) + "/d" + str(inp) +"|f" + (str(func[0]) if len(func[0]) > 1 else "(" + str(func[0][0]) + ")"), ":", p)
                                if str(k) not in gradiants:
                                    gradiants[str(k)] = {}
                                gradiants[str(k)][str(inp)] = p
                        else:
                            if isinstance(fff[0], tuple):
                                not_too_complex = False
                            for i, k in enumerate(func[1]):
                                ff_val = fff[0][i] if isinstance(fff[0], tuple) else fff[i]
                                p = sp.diff(ff_val, inp)
                                if not self.is_silent:
                                    print("partial derivative d" + str(k) + "/d" + str(inp) +"|f" + (str(func[0]) if len(func[0]) > 1 else "(" + str(func[0][0]) + ")"), ":", p)
                                if str(k) not in gradiants:
                                    gradiants[str(k)] = {}
                                gradiants[str(k)][str(inp)] = p  
                            
            for k, v in gradiants.items():
                tot = ""
                base = ""
                for kk, vv in v.items():
                    if base == "":
                        base = str(kk)
                        tot = "(" + str(vv) + ")"
                    else:
                        tot = tot + " + (" + str(vv) + ")*" + str(kk) + "_" + base
                        if (len(tot_deriv_input) == 0 and total_notyet) or add_equation:
                            new_variables.append(str(kk) + "_" + base)
                if (len(tot_deriv_input) == 0 and total_notyet) or add_equation:
                    tot2 = (k + "_" + base, tot)
                tot = k + "_" + base + " = " + tot
                if not self.is_silent:
                    print("TOTAL DERIVATIVE", tot)
                if (len(tot_deriv_input) == 0 and total_notyet) or add_equation:
                    new_equations.append(tot2)
                    new_variables.append(k + "_" + base)

            if (len(tot_deriv_input) == 0 and total_notyet) or (add_equation and total_notyet):
                if not_too_complex:
                    for n in new_variables:
                        if n not in self.variables:
                            self.variables.append(n)
                    variables = sp.symbols(self.variables)
                    for ne in new_equations:
                        new_eq = sp.Eq(sp.sympify(ne[1]), sp.sympify(ne[0]))
                        if sp.solve(self.equations) != sp.solve(self.equations+[new_eq]) and all([sp.solve(new_eq) != sp.solve(e) for e in self.equations]):
                            self.equations.append(new_eq)
                            total_notyet = False
                            if not self.is_silent:
                                print("*")
                                print("New Equation:", new_eq)
                                print("*")
                else:
                    print("Cannot be added to system as too complex", new_equations)
            not_too_complex = True


is_silent = False          

# Linear
print("===== 3 + 1 =========")
# equations = ["a * x + b"]
equations = ["3 * a + 4 * x + 5 * b"]
# equations = ["3 * a + 4 * x + 5 * b**2"]
targets = ["y"]
calc = calculu_machine(equations, targets, ["a", "b", "x", "y"], is_silent=is_silent) 
s = calc.solve_function({"a": 3, "x": 3, "y":5})
print("Solution:", s)
calc.derive_derivatives("a")
# calc.derive_derivatives("a")
# calc.derive_derivatives("a")
# s = calc.solve_function({"a": 3, "x": 3, "y":5, "x": 3, "y":5})
# print("Solution with Derivatives:", s)


print("===== 1 + 3 =========")
equations = ["a * x + b", 
             "3 * b", 
             "a + x"]
targets = ["y", "x", "b"]
calc = calculu_machine(equations, targets, ["a", "b", "x", "y"], is_silent=is_silent) 
s = calc.solve_function({"a": 3})
print("Solution:", s)
calc.derive_derivatives()
s = calc.solve_function({"a": 3})
print("Solution with Derivatives:", s)


print("===== 2 + 2 =========")
# equations = ["a * x + b", 
#              "2 * a + 3 * b*2 + 4 * y"]
equations = ["a + x + b", 
             "2 * a + 3 * b + 4 * y"]
targets = ["y", "x"]
calc = calculu_machine(equations, targets, ["a", "b", "x", "y"], is_silent=is_silent) 
s = calc.solve_function({"a": 3, "x": 3})
print("Solution:", s)
calc.derive_derivatives()
s = calc.solve_function({"a": 3, "x": 3, "x_a": 1})
print("Solution with Derivatives:", s)
            