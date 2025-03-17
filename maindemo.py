import gurobipy as gp
from gurobipy import GRB

model = gp.read("Initial_problem_set\Test_prob_9.mps")

from relaxation import solve_relaxation_with_time_limit
from solutionfile import write_solution_file
from solutionfile import compute_quadratic_objective_value

sol, obj= solve_relaxation_with_time_limit(model, 0.5)
print(obj)
write_solution_file(sol, 1)


model.setParam("OutputFlag", 0)
model.optimize()
sol = {var.VarName: var.X for var in model.getVars()}
best_obj = compute_quadratic_objective_value(model, sol)
print(best_obj)
write_solution_file(sol,2)


    
   
