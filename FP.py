import gurobipy as gp
from gurobipy import GRB

from relaxation import solve_relaxation_with_time_limit as solve_relaxation
from solutionfile import Solution
from solutionfile import compute_quadratic_objective_value
def round_solution(frac_sol, model):
    # Round integer variables; leave continuous as is.
    candidate = {}
    for var in model.getVars():
        val = frac_sol[var.VarName]
        if var.VType in [GRB.BINARY, GRB.INTEGER, GRB.SEMIINT]:
            candidate[var.VarName] = round(val)
        else:
            candidate[var.VarName] = val
    return candidate
                                                                                                                         
def projection(model, candidate):
    # Fix integer variables to candidate values and solve LP.
    proj_model = model.copy()
    proj_model.setParam('OutputFlag', 0)
    for var in proj_model.getVars():
        if var.VType in [GRB.BINARY, GRB.INTEGER, GRB.SEMIINT]:
            val = candidate[var.VarName]
            var.lb = val
            var.ub = val
    proj_model.optimize()
    if proj_model.status == GRB.OPTIMAL:
        sol = {v.VarName: v.X for v in proj_model.getVars()}
        return sol, proj_model.objVal
    return None, None

def feasibility_pump(model, max_iterations=10, relax_time_limit=0.5):
    for it in range(max_iterations):
        frac_sol, _ = solve_relaxation(model, relax_time_limit)
        if frac_sol is None:
            print("No relaxation solution.")
            return None, None
        candidate = round_solution(frac_sol, model)
        proj_sol, obj = projection(model, candidate)
        if proj_sol is not None:
            return proj_sol, obj
    return None, None

if __name__ == "__main__":
    model = gp.read("Initial_problem_set\Test_prob_19.mps")
    solution, obj_val = feasibility_pump(model)
    if solution:
        solutio= Solution(obj_val, solution)
        print(obj_val)
        print(compute_quadratic_objective_value(model, solution))
        solutio.write_solution_file(3)
    else:
        print("No feasible solution found.")
