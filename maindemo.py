import gurobipy as gp
from gurobipy import GRB

model = gp.read("Initial_problem_set\Test_prob_91.mps")
from solutionfile import Solution
from relaxation import solve_relaxation_with_time_limit
sol, obj= solve_relaxation_with_time_limit(model, 5)

sol=Solution(obj,sol)
sol.write_solution_file(1)

model.optimize()
variable_values = {var.VarName: var.X for var in model.getVars()}
best_obj = model.ObjVal
 
sol=(Solution(best_obj, variable_values))
sol.write_solution_file(2)


    
   
