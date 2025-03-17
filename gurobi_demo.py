from gurobipy import read
model = read("Initial_problem_set\Test_prob_19.mps")

# model.setParam("PartitionPlace", 31)
# model.setParam("Heuristics",1)
# model.setParam("NoRelHeurTime", 20)
# model.setParam("NonConvex",2)
# model.setParam("MIQCPMethod",1)
# model.setParam("RINS",1)
# model.setParam("SolFiles","a")
# model.setParam("PreQLinearize",0)
          
model.optimize()
              
if model.status == 2:  # 2 corresponds to 'OPTIMAL'
    print("Optimal Objective Value:", model.objVal)
    # for var in model.getVars():
    #     if var.VarName[0]=='b':
    #         print(f"{var.varName}: {var.x}")
else:
    print(f"Optimization ended with status {model.status}")
    for var in model.getVars():
        if var.VarName[0]=='i' and var.x!=0 and var.x!=1:
            print(f"{var.varName}: {var.x}")
