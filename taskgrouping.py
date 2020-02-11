from gekko import GEKKO
m = GEKKO()           # create GEKKO model

# SETS
numWorkers = 14
numJobs = 3 # number of jobs to assign
numStations = 3 # number of available workstations

# PARAMETERS
takt = m.Param(value=5) # takt time of line
cycleTime = [5,50,10] # cycle time of each job
# pred is true if job j1 is an immediate predecessor of job j2
# pred = m.Array(m.Param,(numJobs,numJobs),lb=0,ub=1,integer=True)
pred = [[0, 1, 0],
        [0, 0, 1],
        [0, 0, 0]]
qual = [ [0,1,0],
[0,1,0],
[0,1,0],
[0,1,0],
[0,1,0],
[0,1,0],
[0,1,0],
[0,1,0],
[0,1,0],
[0,1,0],
[1,0,1],
[1,0,1],
[1,0,1],
[1,0,1]
]

# DECISION VARIABLES
# x is true if job j is assigned to workstation w
x = m.Array(m.Var,(numWorkers,numJobs,numStations),lb=0,ub=1,integer=True)
# numOps is number of operators at workstation w
numOps = m.Array(m.Var,(numStations),lb=0,integer=True)
# can give a warm start by providing initial values
# for w in range(numWorkstations):
#     for j in range(numJobs):
#         if (w==j):
#             x[j,w].value = 1
#     numOps[w,0].value = 1

# OBJECTIVE FUNCTION
m.Obj(sum(numOps[s] for s in range(numStations)))

# CONSTRAINTS
# assign each job to exactly one workstation
for j in range(numJobs):
    m.Equation(sum(sum(x[w,j,s] for s in range(numStations)) for w in range(numWorkers))==1)
# each workstation has enough operators to complete assigned jobs under takt time
for s in range(numStations):
    m.Equation(sum(sum(x[w,j,s]*cycleTime[j] for j in range(numJobs)) for w in range(numWorkers))<=takt*numOps[s])
# calculate number of numWorkers
# for s in range(numStations):
#     print(numOps[s].value)
#     m.Equation(numOps[s].value == sum(sum(x[j,w,s] for j in range(numJobs)) for w in range(numWorkers)))
# predecessors of job j must be assigned at prior workstation, or
# if j1 precedes j2 AND j2 is assigned to w2, j1 must be assigned to w2 or before
# for s2 in range(numStations):
#     for j1 in range(numJobs):
#         for j2 in range(numJobs):
#             m.Equation(sum(x[w,j2,s2] for w in range(numWorkers))*pred[j1][j2]<=sum(sum(x[w,j1,s1] for s1 in range(s2+1))) for w in range(numWorkers))

# for w in range(numWorkers):
#     m.Equation(sum(sum(x[w,j,s] for j in range(numJobs)) for s in range(numStations)) <= qual[w][j])

# SOLVE
m.options.SOLVER=1    # change solver (1=APOPT,3=IPOPT)
m.solve(disp=True)
print('x:'+str(x))
print('numOps:'+str(numOps))
