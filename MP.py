from gurobipy import *
import numpy as np

# Constant creation
f = [400, 414, 326]
a = [18, 25, 20]
C = [[22, 33, 24],
     [33, 23, 30],
     [20, 25, 27], ]
D = [206 + 40, 274 + 40, 220 + 40]
dl = [206, 274, 220]
du = [40, 40, 40]
k = 0  # Iterative counting

# Create model
MP = Model()  # Master-problem
SP = Model()  # Sub-problem(KKT)
SDSP = Model()  # Sub-problem (strong duality)
# Construction of Master-problem
# addVars
y = MP.addVars(len(f), lb=0, ub=1, obj=f, vtype=GRB.INTEGER, name='y')
z = MP.addVars(len(a), lb=0, obj=a, vtype=GRB.CONTINUOUS, name='z')
g = MP.addVars(3, lb=0, ub=1.0, name='g')
η = MP.addVar(obj=1.0, name='η')

# addConstrs
Column1 = MP.addConstrs((z[i] <= 800 * y[i] for i in range(3)), name='column1')
Column4 = MP.addConstr(quicksum(z[i] for i in range(3)) >= 772, name='z')
Column5 = MP.addConstr(quicksum(g[i] for i in range(2)) <= 1.2, name='column5')
Column6 = MP.addConstr(quicksum(g[i] for i in range(3)) <= 1.8, name='column6')

MP.write("MP.lp")  # model print and visual inspection model,can open it with Notepad++
MP.optimize()  # Solve Model
LB = MP.objval  # get optimum value of model

