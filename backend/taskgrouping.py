from pulp import *
from pathlib import Path
import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
from math import ceil #ceil used in finding number of workers and in humanCap
from math import isnan #used in several functions to check if certain values are not numbers
import csv
import backend.settings as settings

def splitIndex(n):
    """will return the list index"""
    return [(x+1) for x,y in zip(n, n[1:]) if y-x != 1]

def splitList(inputList):
    """will split the list base on the index"""
    index = splitIndex(inputList)
    splitList = list()
    prev = 0
    for i in index:
        consecList = [ x for x in inputList[prev:] if x < i]
        splitList.append(consecList)
        prev += len(consecList)
    splitList.append([ x for x in inputList[prev:]])
    return splitList

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
    length = settings.myList['length']
    width = settings.myList['width']

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
    #prob.solve()
    filePath = Path().absolute()
    fileStr = str(filePath)
    fileStr += r"\backend\cbc.exe"
    prob.solve(COIN_CMD(path = fileStr))

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
#############################################################################################################
# dict with new stations as keys and jobs as values
    tasks =	{}
    for i in range(len(real_stations)):
        tasks[i] = task_Dist[i]

    operators = {}
    for i in range(len(real_stations)):
        operators[i] = op_dist[i]

    jobs  #original dictionary with types as keys as jobs as values from csv reader

    assignedJobs = [[[] for k in types] for i in range(len(real_stations))]
    for s in range(len(real_stations)):
        for t in types:
            for j in jobs[t]:
                if (j in tasks[s]):
                    assignedJobs[s][t].append(j)

	# assignedJobs = {{}}
	# for s in range(len(real_stations)):
	# 	for t in types:
	# 		temp = []
	# 		for j in jobs[t]:
	# 			if (j in tasks[s]):
	# 				temp.append(j)
	# 		assignedJobs[s][t] = temp

    #uncomment these lines for CSVs with size data
    length # dict with jobs as keys as length as values, from csv reader
    width # dict with jobs as keys and widths as values, from csv reader

    # results are indexed by station and have job # and number of each type of operator
    # we want to calculate the length and width of each station
    # for each type, we calc the max space required
    # if it's a human type, double the width and multiply the length by (# ops / 2)
    # some computer jobs MUST be all next to each other -- will contemplate that

    placement = [[0,0,0,0] for i in range(len(real_stations))]
    # for each newstation
    for s in range(len(real_stations)):
        currLength = 0
        currWidth = 0
        for t in types[1:]:
            if (len(assignedJobs[s][t])!=0):
                # currLength += op_dist[s][t]*length[jobs[t][0]] # uncomment this line if reducing ports from full capacity
                currLength += cap[t]*length[jobs[t][0]]
                if (width[jobs[t][0]] > currWidth):
                        currWidth = width[jobs[t][0]]
        # now let's handle human jobs -- we can combine space if consecutive
        splitJobs = splitList(assignedJobs[s][0])
        group = 0
        while (group < len(splitJobs) ):
            maxLength = 0
            maxWidth = 0
            for j in splitJobs[group]:
                if (length[j] > maxLength):
                    maxLength = length[j]
                if (width[j] > maxWidth):
                    maxWidth = width[j]
            if (op_dist[s][0] > 1): # if num human ops is greater than one
                currLength += ceil(op_dist[s][0]/2)*maxLength
                if (2*maxWidth > currWidth):
                    currWidth = 2*maxWidth
            else: # if num human ops is 1
                currLength += maxLength
                if (maxWidth > currWidth):
                    currWidth = maxWidth
            group += 1
        placement[s][0] = currLength
        placement[s][1] = currWidth

    # now we also want the bottom left corner of each new station in a line
    # assign a spacer between stations
    spacer = 1
    # assigns a 1 meter offset from the x axis
    xoffset = 1
    # assigns an offset from the y axis that is half the width (y) of the first station plus a spacer
    yoffset = placement[0][1]/2+spacer
    # sets the x, y coordinates to plot at (1,1)
    placement[0][2] = spacer
    placement[0][3] = spacer

    # assigns maximum yoffset given the width of the stations:
    for s in range(len(real_stations)):
        if  yoffset < placement[s][1]/2 + spacer:
            yoffset = placement[s][1]/2 + spacer

    # for each newstation s (minus the last one)
    for s in range(len(real_stations)-1):
        # offset += the length of the newstation + spacer
        xoffset += placement[s][0] + spacer
        placement[s+1][2] = xoffset
        placement[s+1][3] = yoffset-placement[s+1][1]/2 + spacer
	# placement is length (x), width (y), x of bottom left, y of bottom left


##############################################################################################################
    # CSVWrite

    ## create fieldnames for CSVwrite, add the proper number of computer operators, indicated by capacity
    column_names = ['Station (#)', 'Length (m)', 'Width (m)','Process (Name)', 'Human Ops.(#)']
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
                if name == 'Station (#)':
                    row_dict[name] = str(num+1)
                    num += 1
                elif name == 'Length (m)':
                    # row_dict[name] = 1
                    row_dict[name] = ceil(placement[s][0]*100.0)/100.00
                elif name == 'Width (m)':
                    # row_dict[name] = 2
                    row_dict[name] = ceil(placement[s][1]*100.0)/100.00
                elif name == 'Process (Name)':
                    row_dict[name] = str(task_dist[s])[1:-1].replace("'", "") 
                elif name == 'Human Ops.(#)':
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
    settings.myList['placement'] = placement