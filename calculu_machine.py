# calculu_machine
#
# Description: build system of non-linear differential equations and then solve
# Version: 1.3.2
# Author: Tomio Kobayashi
# Last Update: 2024/4/13

import sympy as sp
import numpy as np
from itertools import combinations
    
import re

class calculu_machine:

    def find_variables(e):

        v_set = set()
        variable_pattern = r'\b(?!\d)(?!sin\b|log\b|cos\b|exp\b)[a-zA-Z_]\w*'
        for equation in e:
            v_set.update(set(re.findall(variable_pattern, equation)))

        v_list = list(v_set)
        for v in list(v_list):
            vv = v.split("_")
            if len(vv) > 0:
                v_set.update(set(vv))

        return list(v_set)
    
    # equations_str: equations that contain derivatives should be in the form of ["4*y_x + 3"] = ["z_x"]
    
#     def __init__(self, equations_str, targets, variables, is_silent=False):
    def __init__(self, equations_str, targets, variables=[], is_silent=False):
        
        
        self.variables = variables if len(variables) > 0 else calculu_machine.find_variables(equations_str+targets)
#         print("self.variables", self.variables)
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

    def chop_before_last_underscore(string):
        # Find the index of the last "_"
        last_underscore_index = string.rfind("_")

        # If no "_" found or it's the last character, return the original string
        if last_underscore_index == -1 or last_underscore_index == len(string) - 1:
            return string

        # Otherwise, chop the string after the last "_"
        chopped_string = string[last_underscore_index+1:]
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
                
            return [{k: v for k, v in s.items() if str(k) not in [str(k) for k in knowns]} for s in solution]
        
        except NotImplementedError as e:
            print(f"Caught an error: {e}")
            return None

        
#         Old codes but kept until stable
#      def derive(self, tot_deriv_input=[], skip_if_multiple_solutions=False):

#         variables = sp.symbols(self.variables)
#         num_knowns = len(self.variables) - len(self.equations)
#         if len(tot_deriv_input) != 0 and len(tot_deriv_input) != num_knowns:
#             print("Number of derived input params must be", num_knowns)

#         function_sets = [(tuple(f), tuple([v for v in variables if v not in f])) for f in list(combinations(variables, num_knowns))]
        
#         total_notyet = True
#         for i, func in enumerate(function_sets):
#             new_variables = []
#             new_equations = []
#             add_equation = any([str(f) in tot_deriv_input for f in func[0]])
            
#             solution = sp.solve(self.equations, func[1]) 
#             str_sol = str(solution).replace("[", "").replace("]", "")
#             gradiants = {}
#             not_too_complex = True
#             if str_sol != "":
#                 for inp in func[0]:
#                     if str_sol == "":
#                         continue
#                     else:
#                         fff = sp.sympify(str_sol)
#                         if isinstance(fff, dict):
#                             for k, v in fff.items():
#                                 p = sp.diff(v, inp)
#                                 if not self.is_silent:
#                                     print("partial derivative d" + str(k) + "/d" + str(inp) +"|f" + (str(func[0]) if len(func[0]) > 1 else "(" + str(func[0][0]) + ")"), ":", p)
#                                 if str(k) not in gradiants:
#                                     gradiants[str(k)] = {}
#                                 gradiants[str(k)][str(inp)] = p
#                         else:
#                             if isinstance(fff[0], tuple):
#                                 not_too_complex = False
#                                 print("Multiple equations generated by the function. Only one is used to find derivatives.")
#                                 print("input:", inp)
#                                 print("equations:", fff)
#                             for i, k in enumerate(func[1]):
#                                 ff_val = fff[0][i] if isinstance(fff[0], tuple) else fff[i]
#                                 p = sp.diff(ff_val, inp)
#                                 if not self.is_silent:
#                                     print("partial derivative d" + str(k) + "/d" + str(inp) +"|f" + (str(func[0]) if len(func[0]) > 1 else "(" + str(func[0][0]) + ")"), ":", p)
#                                 if str(k) not in gradiants:
#                                     gradiants[str(k)] = {}
#                                 gradiants[str(k)][str(inp)] = p  
                            
#             for k, v in gradiants.items():
#                 tot = ""
#                 base = ""
#                 for kk, vv in v.items():
#                     if base == "":
#                         base = str(kk)
#                         tot = "(" + str(vv) + ")"
#                     else:
#                         tot = tot + " + (" + str(vv) + ")*" + str(kk) + "_" + base
#                         if (len(tot_deriv_input) == 0 and total_notyet) or add_equation:
#                             new_variables.append(str(kk) + "_" + base)
#                 if (len(tot_deriv_input) == 0 and total_notyet) or add_equation:
#                     tot2 = (k + "_" + base, tot)
#                 tot = k + "_" + base + " = " + tot
#                 if not self.is_silent:
#                     print("TOTAL DERIVATIVE", tot)
#                 if (len(tot_deriv_input) == 0 and total_notyet) or add_equation:
#                     new_equations.append(tot2)
#                     new_variables.append(k + "_" + base)

#             if (len(tot_deriv_input) == 0 and total_notyet) or (add_equation and total_notyet):
#                 if not_too_complex or not skip_if_multiple_solutions:
#                     for n in new_variables:
#                         if n not in self.variables:
#                             self.variables.append(n)
#                     variables = sp.symbols(self.variables)
#                     for ne in new_equations:
#                         new_eq = sp.Eq(sp.sympify(ne[1]), sp.sympify(ne[0]))
#                         if sp.solve(self.equations) != sp.solve(self.equations+[new_eq]) and all([sp.solve(new_eq) != sp.solve(e) for e in self.equations]):
#                             self.equations.append(new_eq)
#                             total_notyet = False
#                             if not self.is_silent:
#                                 print("*")
#                                 print("New Equation:", new_eq)
#                                 print("*")
#                 else:
#                     print("total derivative equations be added to system as the derived equations had multiple solutions", new_equations)
#             not_too_complex = True
            
            
    def derive(self, tot_deriv_input=[], skip_if_multiple_solutions=False):

        variables = sp.symbols(self.variables)
        num_eqs = len(self.equations)
        eqs_added = 0
        
        num_knowns = len(self.variables) - len(self.equations)
        if len(tot_deriv_input) != 0 and len(tot_deriv_input) != num_knowns:
            print("Number of derived input params must be", num_knowns)

        function_sets = [(tuple(f), tuple([v for v in variables if v not in f])) for f in list(combinations(variables, num_knowns))]
        
        for i, func in enumerate(function_sets):
            new_variables = []
            new_equations = []
            
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
                                print("Multiple equations generated by the function. Only one is used to find derivatives.")
                                print("input:", inp)
                                print("equations:", fff)
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
                        new_variables.append(str(kk) + "_" + base)
                tot2 = (k + "_" + base, tot)
                tot = k + "_" + base + " = " + tot
                new_equations.append(tot2)
                if k + "_" + base not in new_variables:
                    new_variables.append(k + "_" + base)

            if not_too_complex or not skip_if_multiple_solutions:
                for n in new_variables:
                    if n not in self.variables:
                        if eqs_added < num_eqs:
                            self.variables.append(n)
                variables = sp.symbols(self.variables)
                for ne in new_equations:
                    new_eq = sp.Eq(sp.sympify(ne[1]), sp.sympify(ne[0]))
                    new_eq_str = str(new_eq.rhs) + " = " + str(new_eq.lhs)
                    print("TOTAL DERIVATIVE:", new_eq_str)
                    if eqs_added < num_eqs:
                        if sp.solve(self.equations) != sp.solve(self.equations+[new_eq]) and all([sp.solve(new_eq) != sp.solve(e) for e in self.equations]):
                            if len(tot_deriv_input) == 0 or calculu_machine.chop_before_last_underscore(ne[0]) in tot_deriv_input:
                                self.equations.append(new_eq)
                                eqs_added += 1
                                if not self.is_silent:
                                    print("*")
                                    print("New Equation:", new_eq_str)
                                    print("*")
                            
            else:
                print("total derivative equations cannot be added to system as the derived equations had multiple solutions", new_equations)
            not_too_complex = True
            
            
        if not self.is_silent:
            print("Variable set", self.variables)
            print("Equations set", self.equations)
            
    def anti_derive(self, num_order=1):

        num_eqs = len(self.equations)
        eqs_added = 0
        varvars = list(set([vv for v in self.variables for vv in v.split("_")]))
        self.variables = list(set(self.variables + varvars))
        variables = sp.symbols(self.variables)
        num_vars = len(varvars)
        num_knowns = num_vars - len(self.equations)
        derivs = list(set([v for v in variables if "_" in str(v)]))
        function_sets = [(tuple(f), tuple([v for v in derivs if v not in f])) for f in list(combinations(derivs, num_knowns-1))]

        total_notyet = True
        for i, func in enumerate(function_sets):
            solution = sp.solve(self.equations, func[1]) 
            str_sol = str(solution).replace("[", "").replace("]", "")
            if str_sol != "":
                fff = sp.sympify(str_sol)
                if isinstance(fff, dict):
                    for k, v in fff.items():
                        sol = sp.Eq(v, k)
                        rhs = sol.rhs
                        terms_r = rhs.as_ordered_terms()
                        higher_order_found = False
                        for term in terms_r:
                            t = str(term)
                            if t.count("_") > num_order:
                                higher_order_found = True
                                break
                        if higher_order_found:
                            continue
                        lhs = sol.lhs
                        terms = lhs.as_ordered_terms()
                        integs = []
                        for term in terms:
                            t = str(term)
                            if t.count("_") > num_order:
                                break
                            eqs = []
                            this_var = calculu_machine.chop_before_last_underscore(str(k))

                            for d in derivs:
                                if str(d) in t and str(d).count("_") == num_order:
                                    this_var = calculu_machine.chop_after_last_underscore(str(d))
                                    t = str(t).replace(str(d), "1")
                                    break
                            integs.append(str(sp.integrate(sp.sympify(t), sp.sympify(this_var))))

                        try:
                            integs = list(set(integs))
                            integ_str = "+".join(integs)
                            self.equations_str.append(integ_str)
                            new_eq = sp.Eq(sp.sympify(integ_str), sp.sympify(calculu_machine.chop_after_last_underscore(str(k))))
                            new_eq_str = str(new_eq.rhs) + " = " + str(new_eq.lhs)
                            if not self.is_silent:
                                print("ANTI-DERIVATED EQUATION:", new_eq_str)
                            if eqs_added < num_eqs:
                                if all([sp.solve(new_eq) != sp.solve(e) for e in self.equations]) and sp.solve(self.equations) != sp.solve(self.equations+[new_eq]):
                                    if not self.is_silent:
                                        print("*")
                                        print("New equation added to the system:", new_eq_str)
                                        print("*")
                                    self.equations.append(new_eq)
                                    eqs_added += 1

                        except NotImplementedError as e:
                            pass
  
        if not self.is_silent:
            print("Variable set", self.variables)
            print("Equations set", self.equations)
            
        
        
is_silent = False          

print("===== 2 + 2 =========")
equations = ["a + x + b", 
             "2 * a + 3 * b + 4 * y"]
targets = ["y", "x"]
# calc = calculu_machine(equations, targets, ["a", "b", "x", "y"], is_silent=is_silent) 
calc = calculu_machine(equations, targets, is_silent=is_silent) 
s = calc.solve_function({"a": 3, "x": 3})
print("Solution:", s)
calc.derive(["a"])
# calc.derive()
s = calc.solve_function({"a": 3, "x": 3, "x_a": 1})
print("Solution with Derivatives:", s)

print("===== 2 + 2 =========")
# equations = ["a + x + b", 
#              "2 * a + 3 * b + 4 * y"]
# targets = ["y", "x"]
equations = ["-7*b_a/3 - 2", 
             "-4*b_a/3 - 1"]
targets = ["x_a", "y_a"]
# calc = calculu_machine(equations, targets, ["a", "b", "x", "b_a", "x_a", "y_a"], is_silent=is_silent) 
calc = calculu_machine(equations, targets, is_silent=is_silent) 
calc.anti_derive()
s = calc.solve_function({"a": 3, "x": 3, "x_a": 1})
print("Solution with Derivatives:", s)

# print("===== 2 + 2 =========")
# # equations = ["a + x + b", 
# #              "2 * a + 3 * b + 4 * y"]
# # targets = ["y", "x"]
# equations = ["-7*b_a_a/3 - 2", 
#              "-4*b_a_a/3 - 1"]
# targets = ["x_a_a", "y_a_a"]
# calc = calculu_machine(equations, targets, ["a", "b", "x", "b_a", "x_a", "y_a", "b_a_a", "x_a_a", "y_a_a"], is_silent=is_silent) 
# calc.anti_derive(num_order=2)
# s = calc.solve_function({"a": 3, "x": 3, "x_a": 1})
# print("Solution with Derivatives:", s)


# # Linear
# print("===== 3 + 1 =========")
# # equations = ["a * x + b"]
# equations = ["3 * a + 4 * x + 5 * b"]
# # equations = ["3 * a + 4 * x + 5 * b**2"]
# targets = ["y"]
# calc = calculu_machine(equations, targets, ["a", "b", "x", "y"], is_silent=is_silent) 
# s = calc.solve_function({"a": 3, "x": 3, "y":5})
# print("Solution:", s)
# calc.derive("a")
# # calc.derive_derivatives("a")
# # calc.derive_derivatives("a")
# # s = calc.solve_function({"a": 3, "x": 3, "y":5, "x": 3, "y":5})
# s = calc.solve_function({"a": 3, "x": 3, "y":5})
# print("Solution with Derivatives:", s)

# # Linear
# print("===== 2 + 1 =========")
# equations = ["3 * x + 4 * y"]
# targets = ["z"]
# calc = calculu_machine(equations, targets, ["x", "y", "z"], is_silent=is_silent) 
# s = calc.solve_function({"x": 3, "y":5})
# print("Solution:", s)
# calc.derive()
# s = calc.solve_function({"x": 3, "y":5, "y_x":2})
# print("Solution with Derivatives:", s)

# # Eq(4*y_x + 3, z_x)

# # Linear
# print("===== 2 + 1 =========")
# equations = ["4*y_x + 3"]
# targets = ["z_x"]
# calc = calculu_machine(equations, targets, ["x", "y", "z", "z_x", "y_x"], is_silent=is_silent) 
# calc.anti_derive()
# print("calc.equations", calc.equations)
# print("calc.variables", calc.variables)
# s = calc.solve_function({"x": 3, "y":5, "y_x":2})
# print("Solution with Derivatives:", s)


# # Linear
# print("===== 2 + 1 =========")
# equations = ["2 * x + 3 * y_x"]
# targets = ["z_x"]
# calc = calculu_machine(equations, targets, ["x", "y", "z", "z_x", "y_x"], is_silent=is_silent) 
# calc.anti_derive()
# print("calc.equations", calc.equations)
# print("calc.variables", calc.variables)
# s = calc.solve_function({"y": 3, "y_x": 2, "z_x": 6})
# print("Solution with Derivatives:", s)

# # Linear
# print("===== 2 + 2 =========")
# # equations = ["2 * x + 3 * y_x"]
# equations = ["2 * x + 3 * y_x", "5 * z + 4 * z_x"]
# targets = ["z_x", "a_x"]
# calc = calculu_machine(equations, targets, ["x", "y", "z", "z_x", "y_x", "a", "a_x"], is_silent=is_silent) 
# calc.anti_derive()
# print("calc.equations", calc.equations)
# print("calc.variables", calc.variables)
# # s = calc.solve_function({"y_x": 2, "a_x": 6, "z": 5})
# # print("Solution with Derivatives:", s)
