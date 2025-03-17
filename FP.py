import gurobipy as gp
from gurobipy import GRB

from relaxation import solve_relaxation_with_time_limit as solve_relaxation
from solutionfile import compute_quadratic_objective_value
from solutionfile import isFeasible
from solutionfile import write_solution_file

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
    proj_model=proj_model.relax()

    proj_model.setParam('OutputFlag', 0)
    obj=0
    for var in proj_model.getVars():
        if var.VType in [GRB.BINARY, GRB.INTEGER]:
            obj+=(var-candidate[var.VarName])
    proj_model.setObjective(obj, sense=GRB.MINIMIZE)
    proj_model.setParam('TimeLimit', 0.5)
    proj_model.optimize()
    if proj_model.status == GRB.OPTIMAL:
        sol = {v.VarName: v.X for v in proj_model.getVars()}
        return sol, proj_model.objVal
    return None, None

def feasibility_pump(model, max_iterations=200, relax_time_limit=0.5):
    candidate, _= solve_relaxation(model, relax_time_limit)
    for it in range(max_iterations):
        proj_sol, obj = projection(model, candidate)
        if proj_sol is None:
            break
        candidate = round_solution(proj_sol, model)
        if isFeasible(model, candidate):
            return candidate
        
    return None

if __name__ == "__main__":
    model = gp.read("Initial_problem_set\Test_prob_9.mps")
    solution = feasibility_pump(model)
    if solution:
        print(isFeasible(model,solution))
        print(compute_quadratic_objective_value(model, solution))
        write_solution_file(solution,3)
    else:
        print("No feasible solution found.")
