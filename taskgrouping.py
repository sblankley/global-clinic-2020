from gekko import GEKKO
from math import ceil 
from CSVReader import *
m = GEKKO()           # create GEKKO model


# DECISION VARIABLES
# x is true if job j is assigned to workstation w
x = m.Array(m.Var,(workers,jobs,stations),lb=0,ub=1,integer=True)
ifJobAtStation = m.Array(m.Var,(jobs,stations),lb=0,ub=1,integer=True)
ifWorkerAtStation = m.Array(m.Var,(workers,stations),lb=0,ub=1,integer=True)
ifWorkerAtJob = m.Array(m.Var,(workers,jobs),lb=0,ub=1,integer=True)
# numOps is number of operators at workstation w
numWorkersAssigned = m.Array(m.Var,(stations),lb=0,integer=True)
# # can give a warm start by providing initial values
# for w in range(workers):
#     for j in range(jobs):
#         for s in range(stations):
#             if (w==j):
#             x[j,w].value = 1
#     numOps[w,0].value = 1

# OBJECTIVE FUNCTION
m.Obj(sum(numWorkersAssigned[s] for s in range(stations)))

# CONSTRAINTS

for j in range(jobs):
    for s in range(stations):
        m.Equation(sum(x[w,j,s] for w in range(workers)) >= 1 - M * (1-ifJobAtStation[j,s]))
        m.Equation(sum(x[w,j,s] for w in range(workers)) <= 0.5 + M * ifJobAtStation[j,s])

for w in range(workers):
    for s in range(stations):
        m.Equation(sum(x[w,j,s] for j in range(jobs)) >= 1 - M * (1-ifWorkerAtStation[w,s]))
        m.Equation(sum(x[w,j,s] for j in range(jobs)) <= 0.5 + M * ifWorkerAtStation[w,s])

for w in range(workers):
    for j in range(jobs):
        m.Equation(sum(x[w,j,s] for s in range(stations)) >= 1 - M * (1-ifWorkerAtJob[w,j]))
        m.Equation(sum(x[w,j,s] for s in range(stations)) <= 0.5 + M * ifWorkerAtJob[w,j])

# assign each job to exactly one workstation
for j in range(jobs):
    m.Equation(sum(ifJobAtStation[j,s] for s in range(stations)) == 1)
# assign each worker to at max one workstation
for w in range(workers):
    m.Equation(sum(ifWorkerAtStation[w,s] for s in range(stations)) <= 1)
# each workstation has enough operators to complete assigned jobs under takt time
for s in range(stations):
    m.Equation(sum(ifJobAtStation[j,s]*cycleTime[j] for j in range(jobs)) <=takt*numWorkersAssigned[s])
# link workers at stations
for s in range(stations):
    m.Equation(sum(ifWorkerAtStation[w,s] for w in range(workers)) == numWorkersAssigned[s])
# qualified workers
for w in range(workers):
    for j in range(jobs):
        m.Equation(ifWorkerAtJob[w,j] <= ifQual[w][j])
# keep from overcrowding
for s in range(stations):
    m.Equation(sum(sum(x[w,j,s] * (1-jobIsComputer[j]) for j in range(jobs)) for w in range(workers)) <= humanCap)

for j1 in range(jobs):
    for j2 in range(jobs):
        for s2 in range(stations):
            m.Equation(ifJobAtStation[j2,s2]*pred[j1][j2] <= sum(ifJobAtStation[j1,s1] for s1 in range(s2)))

# SOLVE
m.options.SOLVER=1    # change solver (1=APOPT,3=IPOPT)
m.solve(disp=True)

print('x:'+str(x))
print('ifJobAtStation:'+str(ifJobAtStation))
print('ifWorkerAtStation:'+str(ifWorkerAtStation))
print('ifWorkerAtJob:'+str(ifWorkerAtJob))
print('numWorkersAssigned:'+str(numWorkersAssigned))


