from gekko import GEKKO
m = GEKKO()           # create GEKKO model

# Sets
numJobs = 3 # number of tasks
numWorkstations = 3 # number of available workstations (max n)

# Parameters
Takt = m.Param(value=10)
procTime = [5,5,10]

# Decision Variables
x = m.Array(m.Var,(numJobs,numWorkstations),lb=0,ub=1,integer=True)
numOps = m.Array(m.Var,(numWorkstations,1),lb=0,integer=True)
for w in range(numWorkstations):
    for j in range(numJobs):
        if (w==j):
            x[j,w].value = 1
    numOps[w,0].value = 100

# Objective Function
m.Obj(sum(numOps[w,0] for w in range(numWorkstations)))

# Constraints
for j in range(numJobs):
    m.Equation(sum(x[j,w] for w in range(numWorkstations))==1)
for w in range(numWorkstations):
    m.Equation(sum(x[j,w]*procTime[j] for j in range(numJobs))<=Takt*numOps[w,0])

# Solve
m.options.SOLVER=1    # change solver (1=APOPT,3=IPOPT)
m.solve(disp=True)
print('x:'+str(x))
print('numOps:'+str(numOps))
