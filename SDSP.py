from MP import *

# Constant creation
f = [400, 414, 326]
a = [18, 25, 20]
C = [[22, 33, 24],
     [33, 23, 30],
     [20, 25, 27], ]
D = [206 + 40, 274 + 40, 220 + 40]
dl = [206, 274, 220]
du = [40, 40, 40]

d = [dl[i] + du[i] * g[i].x for i in range(3)]
# zupd = []
# zupd.append([z[i].x for i in range(3)])
SDSP = Model()
# Construction of Sub-problem (strong duality)
# addVars
r = SDSP.addVars(3, lb=0, name='labm')
w = SDSP.addVars(3, lb=0, name='w')
t = SDSP.addVars(3, lb=0, name='pi')
g = SDSP.addVars(3, lb=0, ub=1.0, vtype=GRB.INTEGER, name='g')
M = 1e5
# addConstrs
SD1 = SDSP.addConstrs(((r[j] - t[i]) <= C[i][j] for i in range(3) for j in range(3)), name='SDSP1')
SD2 = SDSP.addConstr(quicksum(g[i] for i in range(2)) <= 1.2, name='SDSP2')
SD3 = SDSP.addConstr(quicksum(g[i] for i in range(3)) <= 1.8, name='SDSP3')
SD4 = SDSP.addConstrs((w[j] <= r[j] for j in range(3)), name='SDSP4')
SD5 = SDSP.addConstrs((w[j] <= g[j] * M for j in range(3)), name='SDSP5')
SD6 = SDSP.addConstrs((w[j] >= (r[j] - (1 - g[j]) * M) for j in range(3)), name='SDSP6')
obj = quicksum(dl[i] * r[i] + du[i] * w[i] - z[i].x * t[i] for i in range(3))

SDSP.setObjective(obj, GRB.MAXIMIZE)  # set Objective is max
SDSP.optimize()  # Solve Model
UB = LB - η.x + SDSP.objval
