from pulp import *
# change solver to cplex
from csvReader import *
import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
from math import ceil #ceil used in finding number of workers and in humanCap
from math import isnan #used in several functions to check if certain values are not numbers
import csv

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


# OUTPUT MGMT

for s in stations:
    print("\nStation %s:" % (s))
    for j in range(numJobs):
        if (value(ifJobAtStation[j][s]) != 0):
            print ("ifJobAtStation(%s,%s)=%s" % (j,s,value(ifJobAtStation[j][s])))
    for t in types:
        if (value(numWorkers[t][s]) != 0):
            print ("numWorkers(%s,%s)=%s" % (t,s,value(numWorkers[t][s])))

# eliminate null stations
new_out = {}
check = 0.0
newstation=0

for s in stations:
    for j in range(numJobs):
        check += value(ifJobAtStation[j][s])
        #print(check)
    if (check != 0.0):
        new_out[newstation] = ifJobAtStation[s]
        newstation += 1
        print('\nadded non-zero station!')
    check = 0.0

print('\n')
print(new_out)

# Format Optimization Output for CSVWrite

real_stations = len(new_out)

task_dist = []
for station_index in range(0,real_stations):
    task_dist.append([])
print('task_dist is', task_dist)


op_dist = []
for ops in types:
    op_dist.append([])
print('op_dist is', op_dist)

for s in range(0,real_stations):
    print("\nStation %s:" % (s))
    for j in range(numJobs):
        if (value(ifJobAtStation[j][s]) != 0):
           task_dist[s].append(j)
           print('task_dist is', task_dist)

    for t in types:
        if (value(numWorkers[t][s]) != 0):
            op = value(numWorkers[t][s])
            op_dist[t].append(op)
            print('op_dist is', op_dist)

# CSVWrite

## create fieldnames for CSVwrite, add the proper number of computer operators, indicated by capacity
column_names = ['Station', 'Tasks', 'Human Ops.']
for comp_ops in (types[1:]):
    column_names.append('Comp. Ops. (Cap=' + str(value(cap[comp_ops])) + ')')


## Use csv.DictWriter to format csv output and write to specified csv file

with open('pLineOpt.csv', 'w', newline='') as csvfile:
    fieldnames = column_names
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

## Create row format and write to CSV

    row_dict = {}
    count = 0

    for s in range(0,real_stations):
        for name in fieldnames:
            if name == 'Station':
                row_dict[name] = str(s+1)
            elif name == 'Tasks':
                row_dict[name] = task_dist[s]
            elif name == 'Human Ops.':
                row_dict[name] = op_dist[0]
            else:
                
                for ops in range(1,(len(op_dist))):
                    row_dict[name] = op_dist[ops]   
        print('row_dict is', row_dict)
        writer.writerow( row_dict )
