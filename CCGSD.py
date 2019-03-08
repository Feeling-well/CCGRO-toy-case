from SDSP import *
while UB - LB > 10e-4:
    # create varibales and add the following constraints
    xx = MP.addVars(3, 3, lb=0, vtype=GRB.CONTINUOUS, name='x')
    d = [dl[i] + du[i] * g[i].x for i in range(3)]
    Column2 = MP.addConstrs(((quicksum(xx[i, j] for j in range(3))) <= z[i] for i in range(3)), name='column2')
    Column3 = MP.addConstrs(((quicksum(xx[i, j] for i in range(3))) >= d[j] for j in range(3)), name='column3')
    Column7 = MP.addConstr(quicksum(C[i][j] * xx[i, j] for i in range(3) for j in range(3)) <= η)
    MP.optimize()
    LB = MP.objval  # update LB

    obj = quicksum(dl[i] * r[i] + du[i] * w[i] - z[i].x * t[i] for i in range(3))  # update SDSP's obj
    SDSP.setObjective(obj, GRB.MAXIMIZE)
    SDSP.optimize()
    UB = min(UB, LB - η.x + SDSP.objval)  # update UB
    k = k + 1  # Iterative counting
print(LB)
