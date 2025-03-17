
# We will always have solution in the form of dictionary like
# Example:
vars_assignment = {
    "x0": 1.1234567891111325,
    "x1": 0.7111901117715214,
    "x2": 1.0000004178984544
}   
def write_solution_file(solution,  solution_index):
    
    file_name = f"SolutionFile{solution_index}.txt"
    
    with open(file_name, "w") as f:
        f.write(f"Variable_name\tVariable_value\n")            
        for var_name, var_value in solution.items():
            f.write(f"{var_name}\t{var_value}\n")




write_solution_file(vars_assignment,solution_index=1)


import gurobipy as gp

def get_objective_terms(model):
    obj_expr = model.getObjective()  # QuadExpr
    quad_terms = []
    for i in range(obj_expr.size()):
        if isinstance(obj_expr, gp.QuadExpr):

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

import gurobipy as gp


import gurobipy as gp

def isFeasible(model, solution, tol=1e-6):
    # Check linear constraints
    for constr in model.getConstrs():
        row = model.getRow(constr)
        lhs = 0.0
        for j in range(row.size()):
            var = row.getVar(j)
            coeff = row.getCoeff(j)
            lhs += coeff * solution.get(var.VarName, 0)
        if constr.Sense == gp.GRB.LESS_EQUAL and lhs > constr.RHS + tol:
            return False
        if constr.Sense == gp.GRB.GREATER_EQUAL and lhs < constr.RHS - tol:
            return False
        if constr.Sense == gp.GRB.EQUAL and abs(lhs - constr.RHS) > tol:
            return False

    # Check quadratic constraints
    for qconstr in model.getQConstrs():
        qexpr = qconstr.QCExpr
        lhs = 0.0
        for i in range(qexpr.size()):
            v1 = qexpr.getVar1(i)
            v2 = qexpr.getVar2(i)
            coeff = qexpr.getCoeff(i)
            lhs += coeff * solution.get(v1.VarName, 0) * solution.get(v2.VarName, 0)
        row = model.getRow(qconstr)
        for j in range(row.size()):
            var = row.getVar(j)
            coeff = row.getCoeff(j)
            lhs += coeff * solution.get(var.VarName, 0)
        if qconstr.QCSense == gp.GRB.LESS_EQUAL and lhs > qconstr.QCRHS + tol:
            return False
        if qconstr.QCSense == gp.GRB.GREATER_EQUAL and lhs < qconstr.QCRHS - tol:
            return False
        if qconstr.QCSense == gp.GRB.EQUAL and abs(lhs - qconstr.QCRHS) > tol:
            return False

    return True
