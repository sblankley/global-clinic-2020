from gekko import GEKKO
m = GEKKO()           # create GEKKO model

# SETS
numJobs = 3 # number of jobs to assign
numWorkstations = 3 # number of available workstations

# PARAMETERS
takt = m.Param(value=10) # takt time of line
cycleTime = [5,5,10] # cycle time of each job
# pred is true if job j1 is an immediate predecessor of job j2
# pred = m.Array(m.Param,(numJobs,numJobs),lb=0,ub=1,integer=True)
pred = [[0, 1, 0],
        [0, 0, 1],
        [0, 0, 0]]

# DECISION VARIABLES
# x is true if job j is assigned to workstation w
x = m.Array(m.Var,(numJobs,numWorkstations),lb=0,ub=1,integer=True)
# numOps is number of operators at workstation w
numOps = m.Array(m.Var,(numWorkstations,1),lb=0,integer=True)
# can give a warm start by providing initial values
# for w in range(numWorkstations):
#     for j in range(numJobs):
#         if (w==j):
#             x[j,w].value = 1
#     numOps[w,0].value = 1

# OBJECTIVE FUNCTION
m.Obj(sum(numOps[w,0] for w in range(numWorkstations)))

# CONSTRAINTS
# assign each job to exactly one workstation
for j in range(numJobs):
    m.Equation(sum(x[j,w] for w in range(numWorkstations))==1)
# each workstation has enough operators to complete assigned jobs under takt time
for w in range(numWorkstations):
    m.Equation(sum(x[j,w]*cycleTime[j] for j in range(numJobs))<=takt*numOps[w,0])
# predecessors of job j must be assigned at prior workstation, or
# if j1 precedes j2 AND j2 is assigned to w1, j1 must be assigned to w1 or before
for w1 in range(numWorkstations):
    for j1 in range(numJobs):
        for j2 in range(numJobs):
            m.Equation(x[j2,w1]*pred[j1][j2]<=sum(x[j1,w2] for w2 in range(w1+1)))

# SOLVE
m.options.SOLVER=1    # change solver (1=APOPT,3=IPOPT)
m.solve(disp=True)
print('x:'+str(x))
print('numOps:'+str(numOps))
