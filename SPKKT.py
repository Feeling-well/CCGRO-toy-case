from MP import *

# 添加变量
Mx = np.zeros((3, 3))
Mλ = np.zeros((3))
Mπ = np.zeros((3))
for i in range(3):
    for j in range(3):
        Mx[i][j] = min(D[j], z[i].x)
        Mλ[i] = max(C[i][0], C[i][1], C[i][2])
        Mπ[i] = max(C[0][i], C[1][i], C[2][i])
# 子问题求解kkt
x = SP.addVars(3, 3, lb=0, obj=np.array(C) * -1, vtype=GRB.CONTINUOUS, name='x')
g = SP.addVars(3, lb=0, ub=1.0, name='g')
d = [206 + 40 * g[0], 274 + 40 * g[1], 220 + 40 * g[2]]
α = SP.addVars(3, 3, vtype=GRB.BINARY, name='α')
β = SP.addVars(3, vtype=GRB.BINARY, name='β')
γ = SP.addVars(3, vtype=GRB.BINARY, name='γ')
λ = SP.addVars(3, vtype=GRB.CONTINUOUS, name='λ')
π = SP.addVars(3, vtype=GRB.CONTINUOUS, name='π')
A = [252, 0, 520]
S1 = SP.addConstrs(((quicksum(x[i, j] for j in range(3))) <= z[i].x for i in range(3)), name='SPcolumn1')
S2 = SP.addConstrs(((quicksum(x[i, j] for i in range(3))) >= d[j] for j in range(3)), name='SPcolumn2')
S3 = SP.addConstrs(((λ[j] - π[i]) <= C[i][j] for i in range(3) for j in range(3)), name='SPcolumn3')
S4 = SP.addConstrs((Mx[i][j] * α[i, j] >= x[i, j] for i in range(3) for j in range(3)), name='SPcolumn4')
S5 = SP.addConstrs(
    ((C[i][j] - λ[j] + π[i]) <= (C[i][j] + Mπ[i]) * (1 - α[i, j]) for i in range(3) for j in range(3)),
    name='SPcolumn5')
S6 = SP.addConstrs((λ[j] <= Mλ[j] * β[j] for j in range(3)), name='SPcolumn6')
S7 = SP.addConstrs(((quicksum(x[i, j] for i in range(3)) - d[j]) <= 40 * (1 - β[j]) for j in range(3)),
                   name='SPcolumn7')
S8 = SP.addConstrs((π[i] <= Mπ[i] * γ[i] for i in range(3)), name='SPcolumn8')
S9 = SP.addConstrs(((z[i].x - quicksum(x[i, j] for j in range(3))) <= (1 - γ[i]) * z[i].x for i in range(3)),
                   name='SPcolumn9')
SP.addConstr(quicksum(g[i] for i in range(2)) <= 1.2, name='SP10')
SP.addConstr(quicksum(g[i] for i in range(3)) <= 1.8, name='SP11')
SP.write("SP.lp")
SP.optimize()
d = [dl[i] + du[i] * g[i].x for i in range(3)]
Q = SP.objval
UB = LB - η.x - Q


print("0")

