# calcu_machine
#
# Description: automatically calculates total derivatives from system of equations and then solve
# Version: 1.1.7
# Author: Tomio Kobayashi
# Last Update: 2024/3/28

import sympy as sp
import numpy as np
from itertools import combinations

class calcu_machine:
    
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
            print("Solving for", self.variables)
            solution = sp.solve(equations, self.variables)
            if isinstance(solution, dict):
                derivs = [k for k, v in solution.items() if "_" in str(k)]
                if len(derivs) > 0:
                    pair_combinations = list(combinations(derivs, 2))
                    for p in [pair for pair in pair_combinations if str(pair[0]).split("_")[len(str(pair[0]).split("_"))-1] == str(pair[1]).split("_")[len(str(pair[1]).split("_"))-1]]:
                        solution[calcu_machine.chop_after_last_underscore(str(p[0])) + "_" + calcu_machine.chop_after_last_underscore(str(p[1]))] = solution[p[0]]/solution[p[1]]
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
#         print(function_sets)
        
        total_notyet = True
        new_variables = []
        new_equations = []
        for i, func in enumerate(function_sets):
            
            add_equation = all([str(f) in tot_deriv_input for f in func[0]])
            
            solution = sp.solve(self.equations, func[1]) 
            str_sol = str(solution).replace("[", "").replace("]", "")
            gradiants = {}
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
                            print("No equation found for each of output", func[1])
                            print(fff)
                            continue
                            
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

            if (len(tot_deriv_input) == 0 and total_notyet) or add_equation:
                for n in new_variables:
                    self.variables.append(n)
                variables = sp.symbols(self.variables)
                for ne in new_equations:
                    new_eq = sp.Eq(sp.sympify(ne[1]), sp.sympify(ne[0]))
                    self.equations.append(new_eq)
                    total_notyet = False
                    if not self.is_silent:
                        print("*")
                        print("New Equation:", new_eq)


is_silent = False          

# Linear
print("===== Linear =========")
equations = ["2 * x + 3 * y + 1 * z", "4 * x + 1 * y + 8 * z"]
targets = [20, 30]
calc = calcu_machine(equations, targets, ["x", "y", "z"], is_silent=is_silent) 
# s = calc.solve_function({"z": 3})
# print("Solution:", s)
calc.derive_derivatives(["y"])
# s = calc.solve_function({"z": 3})
# print("Solution with Derivatives:", s)
