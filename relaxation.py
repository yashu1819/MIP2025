import gurobipy as gp
from gurobipy import GRB

def solve_relaxation_with_time_limit(original_model, time_limit):
  
    relaxed_model = original_model.relax()
    
    relaxed_model.setParam('TimeLimit', time_limit)
    
    relaxed_model.optimize()
    
    if relaxed_model.SolCount == 0:
        print("No solution found in the relaxation within the time limit.")
        return None, None
    
    fractional_solution = {var.VarName: var.X for var in relaxed_model.getVars()}
    relaxation_obj = relaxed_model.objVal
    
    return fractional_solution, relaxation_obj