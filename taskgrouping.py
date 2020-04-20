from pulp import *
import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
from math import ceil #ceil used in finding number of workers and in humanCap
from math import isnan #used in several functions to check if certain values are not numbers
import csv
import settings

def group():
    # import global variables
    stations = settings.myList['stations']
    types = settings.myList['types']
    jobs = settings.myList['jobs']
    pred = settings.myList['pred']
    numJobs = settings.myList['numJobs']
    cycleTime = settings.myList['cycleTime']
    takt = settings.myList['takt']
    cap = settings.myList['cap']
    jobNames = settings.myList['jobNames']


    M = 100

    # begin 
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
        if (sum(value(ifJobAtStation[j][s]) for j in range(numJobs))!=0):
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

    for s in stations:
        for j in range(numJobs):
            check += value(ifJobAtStation[j][s])
        if (check != 0.0):
            new_out[s] = ifJobAtStation[s]
        check = 0.0

    # Format Optimization Output for CSVWrite

    keys = new_out.keys()
    real_stations = list(keys)
    num_real_stations = len(real_stations)

    check = {}
    for s in range(0,num_real_stations):
        index = real_stations[s]
        check[s] = new_out[index]

    ## make new station and operator dictionaries for writing
    task_dist = []
    task_Dist = []
    for station_index in real_stations:
        task_dist.append([])
        task_Dist.append([])

    op_dist = []

    for station_index in range(0,num_real_stations):
        op_dist.append([])
        for ops in types:
            op_dist[station_index].append([])

    index = 0
    ## Add condensed format to new dictionaries
    for s in real_stations:
        for j in range(numJobs):
            if (value(ifJobAtStation[j][s]) != 0):
                task_dist[index].append(jobNames[j])
                task_Dist[index].append(j)
                
        for t in types:
            if (value(numWorkers[t][s]) != 0):
                op = value(numWorkers[t][s])
                op_dist[index][t] = op

            else:
                op_dist[index][t] = 0.0

        index += 1
    # CSVWrite

    ## create fieldnames for CSVwrite, add the proper number of computer operators, indicated by capacity
    column_names = ['Station', 'Tasks', 'Human Ops.']
    comp_names = []
    for comp_ops in (types[1:]):
        comp_names.append('Comp. Ops. (' +  str(jobNames[jobs[comp_ops][0]])+ ')')
    column_names.extend(comp_names)

    ## Use csv.DictWriter to format csv output and write to specified csv file

    with open('pLineOpt.csv', 'w', newline='') as csvfile:
        fieldnames = column_names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    ## Create row format and write to CSV

        # row_dict = {}
        count = len(types) - 1
        num = 0
        saved = [[] for i in range (0,num_real_stations)]
        for s in range(0,num_real_stations):
            row_dict = {}
            for name in fieldnames:
                if name == 'Station':
                    row_dict[name] = str(num+1)
                    num += 1
                elif name == 'Tasks':
                    row_dict[name] = str(task_dist[s])[1:-1].replace("'", "") 
                elif name == 'Human Ops.':
                    row_dict[name] = op_dist[0][0]
                else:        
                    for comp_name in comp_names:
                        ps = comp_names.index(comp_name)
                        row_dict[comp_name] = op_dist[s][ps+1]
            saved[s] = row_dict
            writer.writerow( row_dict )

    # add global variables
    settings.myList['real_stations'] = real_stations
    settings.myList['op_dist'] = op_dist
    settings.myList['task_dist'] = task_dist
    settings.myList['task_Dist'] = task_Dist