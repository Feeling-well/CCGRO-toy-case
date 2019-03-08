"""
learn from Paper named:
Solving two-stage robust optimization problems using a column-and-constraint generation method
Author:Su XY
Time:2019-3-1
Place of creation:iPso

"""

from SPKKT import *
while UB - LB > 10e-4:
    xx = MP.addVars(3, 3, lb=0, vtype=GRB.CONTINUOUS, name='x')
    Column2 = MP.addConstrs(((quicksum(xx[i, j] for j in range(3))) <= z[i] for i in range(3)), name='column2')
    Column3 = MP.addConstrs(((quicksum(xx[i, j] for i in range(3))) >= d[j] for j in range(3)), name='column3')
    Column7 = MP.addConstr(quicksum(C[i][j] * xx[i, j] for i in range(3) for j in range(3)) <= η)
    MP.optimize()
    LB = MP.objval
    SP.remove(SP.getConstrs()[0:6])
    SP.remove(SP.getConstrs()[15:23])
    SP.remove(SP.getConstrs()[36:39])
    SP.remove(SP.getConstrs()[42:45])
    S1 = SP.addConstrs(((quicksum(x[i, j] for j in range(3))) <= z[i].x for i in range(3)), name='SPcolumn1')
    S2 = SP.addConstrs(((quicksum(x[i, j] for i in range(3))) >= d[j] for j in range(3)), name='SPcolumn2')
    S7 = SP.addConstrs(((quicksum(x[i, j] for i in range(3)) - d[j]) <= 40 * (1 - β[j]) for j in range(3)),
                       name='SPcolumn7')
    S9 = SP.addConstrs(((z[i].x - quicksum(x[i, j] for j in range(3))) <= (1 - γ[i]) * z[i].x for i in range(3)),
                       name='SPcolumn9')
    for i in range(3):
        for j in range(3):
            Mx[i][j] = min(D[j], z[i].x)
    S4 = SP.addConstrs((Mx[i][j] * α[i, j] >= x[i, j] for i in range(3) for j in range(3)), name='SPcolumn4')
    SP.write('SP.lp')
    SP.optimize()
    UB = LB - η.x - SP.objval
    k = k + 1
print(LB)
