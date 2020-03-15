from gekko import GEKKO
from math import ceil
from CSVReader import *
m = GEKKO()           # create GEKKO model

m.solver_options = ['minlp_gap_tol 1.0e-2',\
                    'minlp_maximum_iterations 1000000']

import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
from math import ceil #ceil used in finding number of workers and in humanCap
from math import isnan #used in several functions to check if certain values are not numbers

# DECISION VARIABLES
x = m.Array(m.Var,(numTypes,numStations),lb=0,integer=True) # number of workers of type t at station s
ifJobAtStation = m.Array(m.Var,(numJobs,numStations),lb=0,ub=1,integer=True) # binary if job j is assigned to station s
# warm start by providing initial values
for t in types:
    for j in jobs[t]:
        for s in stations:
            if (j==s):
                ifJobAtStation[j,s].value = 1
            else:
                ifJobAtStation[j,s].value = 0
            x[t,s].value = ceil(cycleTime[j]/takt)

# OBJECTIVE FUNCTION
m.Obj(sum(x[0,s] for s in stations)) # total number of human operators

# CONSTRAINTS

# assign each job to exactly one workstation
for t in types:
    for j in jobs[t]:
        m.Equation(sum(ifJobAtStation[j,s] for s in stations) == 1)
# no workers of type t if no jobs of type t assigned
for s in stations:
    for t in types:
        m.Equation(x[t,s] <= sum(ifJobAtStation[j,s] for j in jobs[t]) * M)
# station has capacity to complete assignments under takt time
for s in stations:
    for t in types:
        m.Equation(sum(ifJobAtStation[j,s]*cycleTime[j] for j in jobs[t]) <= takt * x[t,s])
# no overcrowding of human operators
for s in stations:
    for t in types:
        m.Equation(x[t,s] <= cap[t])
# precedence
for s in stations:
    for t in types:
        for j in jobs[t]:
            for g in pred[j]:
                m.Equation(ifJobAtStation[j,s] <= sum(ifJobAtStation[g,k] for k in range(s+1)))
# no unmanned stations - only use for larger datasets
# for s in stations:
#     m.Equation(sum(x[t,s] for t in compTypes) <= x[0,s] * M)

# SOLVE
m.options.SOLVER=1    # change solver (1=APOPT,3=IPOPT)
m.solve(disp=True)

print('x:'+str(x))
print('ifJobAtStation:'+str(ifJobAtStation))
# output = []
# for s in stations:
#     if x[t,s]
#     output += []