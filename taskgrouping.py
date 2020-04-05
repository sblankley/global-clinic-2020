from pulp import *
# change solver to cplex
from csvReader import *
import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
from math import ceil #ceil used in finding number of workers and in humanCap
from math import isnan #used in several functions to check if certain values are not numbers

prob = LpProblem("Assignment Problem",LpMinimize)

# DECISION VARIABLES
numWorkers = LpVariable.dicts(name="numWorkers", indexs=(types,stations), lowBound=0, cat=LpInteger)
ifJobAtStation = LpVariable.dicts(name="ifJobAtStation",indexs=(range(numJobs),stations), cat=LpBinary)

# OBJECTIVE
prob += lpSum(numWorkers[0][s] for s in stations) # total number of human operators

# CONSTRAINTS
# assign each job to exactly one workstation
for t in types:
    for j in jobs[t]:
        prob += lpSum(ifJobAtStation[j][s] for s in stations) == 1
# no workers of type t if no jobs of type t assigned
for s in stations:
    for t in types:
        prob += numWorkers[t][s] <= lpSum(ifJobAtStation[j][s] for j in jobs[t]) * M
# station has capacity to complete assignments under takt time
for s in stations:
    for t in types:
        prob += lpSum(ifJobAtStation[j][s]*cycleTime[j] for j in jobs[t]) <= takt * numWorkers[t][s]
# no overcrowding of human operators
for s in stations:
    for t in types:
        prob += numWorkers[t][s] <= cap[t]
# precedence
for s in stations:
    for t in types:
        for j in jobs[t]:
            for g in pred[j]:
                prob += ifJobAtStation[j][s] <= lpSum(ifJobAtStation[g][k] for k in range(s+1))
# no unmanned stations - only use for larger datasets
# for s in stations:
#     prob += lpSum(numWorkers[(t,s)] for t in compTypes) <= numWorkers[(0,s)] * M

# SOLVE
prob.solve()
for s in stations:
    print("Station %s:" % (s))
    for j in range(numJobs):
        if (value(ifJobAtStation[j][s]) != 0):
            print ("ifJobAtStation(%s,%s)=%s" % (j,s,value(ifJobAtStation[j][s])))
    for t in types:
        if (value(numWorkers[t][s]) != 0):
            print ("numWorkers(%s,%s)=%s" % (t,s,value(numWorkers[t][s])))


# for s in stations:
#     print ("Station ", s, " is assigned: ",)
#     print ([j for j in range(numJobs) if ifJobAtStation[j][s].varValue == 1])
    # print [j for j in types if numWorkers[(t,s)]]

# print('numWorkers:'+str(numWorkers))
# print('ifJobAtStation:'+str(ifJobAtStation))
# output = []
# for s in stations:
#     if numWorkers[t,s]
#     output += []

# csv.writer(csvfile, dialect='excel', **fmtparams)
# spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
