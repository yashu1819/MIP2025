class Solution:
   
    def __init__(self, objective_value, variable_values):
    
        self.objective_value = objective_value
        self.variable_values = variable_values
    
            
    def write_solution_file(self, solution_index):
       
        file_name = f"SolutionFile{solution_index}.txt"
        
        with open(file_name, "w") as f:
            f.write(f"Variable_name\tVariable_value\n")            
            for var_name, var_value in self.variable_values.items():
                f.write(f"{var_name}\t{var_value}\n")

vars_assignment = {
    "x0": 1.1234567891111325,
    "x1": 0.7111901117715214,
    "x2": 1.0000004178984544
}

sol = Solution(objective_value=10.5, variable_values=vars_assignment)

sol.write_solution_file(solution_index=1)


import gurobipy as gp

def get_objective_terms(model):
    obj_expr = model.getObjective()  # QuadExpr
    quad_terms = []
    for i in range(obj_expr.size()):
        v1 = obj_expr.getVar1(i)
        v2 = obj_expr.getVar2(i)
        coeff = obj_expr.getCoeff(i)
        if coeff != 0:
            quad_terms.append((v1.VarName, v2.VarName, coeff))
    return  quad_terms

def compute_quadratic_objective_value(model, solution):
    quad_terms= get_objective_terms(model)
    # Linear part
    lin_val = sum(var.Obj * solution[var.VarName] for var in model.getVars())
    # Quadratic part: quad_terms is a list of (varname1, varname2, coef)
    quad_val = sum(coef * solution[v1] * solution[v2] for v1, v2, coef in quad_terms)
    return   lin_val + quad_val
