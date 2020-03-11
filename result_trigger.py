import csv
from gekko import GEKKO
from math import ceil
import numpy as np
from CSVReader import *

def run_optimization():
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

    # SOLVE
    m.options.SOLVER=1    # change solver (1=APOPT,3=IPOPT)
    m.solve(disp=True)

    return x, ifJobAtStation
    #print('x:'+str(x))
    #print('ifJobAtStation:'+str(ifJobAtStation))

#
# Output translation begins below
#
def translate_to_csv():

    # Initial variable to manipulate optimization output
    result  = run_optimization()
    opDist  = result[0] # distribution of operators, equivalent to "x" above
    jobDist = result[1] # distribution of tasks amongst stations, equivalent to "ifJobAtStation" above
    opList = []
    #opDist = opDist.tolist() # strip dtype from end of opDist
    print(opDist)
    print(jobDist)

    # Loop to Populate Workers from "x"
    num_ops = len(opDist)         # number of different types of workers
    num_stations = len(opDist[0]) # look at first type of worker to see how many stations there are

    for op_type in range(0,num_ops):
        op_type_matrix = opDist[op_type] # shows how many operators of each type are distributed amongst stations
        #print(op_type_matrix)

        for station in range(0,num_stations):
            num_assigned = op_type_matrix[station].value # number of assigned worker at each station, per type
            #print(num_assigned)
            opList.append(num_assigned)

    print(opList)

    # Loop to Populate Stations with Tasks from "ifJobAtStation"

    # Create empty list of lists for .csv output
    joblist = []
    for station_index in range(0,num_stations):
        joblist.append([])

    # 
    num_Jobs = len(jobDist[0])
    job_matrix = []
    for job_index in range(0,num_Jobs):
        job = jobDist[job_index]
        for station_index in range(0,num_stations):
            if job[station_index].value == [1.0]:
                joblist[station_index].append((int(job_index+1)))

    print(joblist)
                
    # check for unused stations

    # idk how to python tbh

    # out = [[0.0], [1.0], [1.0], [0.0], [2.0], [0.0]]
    # check = []
    # for index in range(0, num_stations):
    #     for nextrow in range(0, num_ops):
    #         check += out[index + nextrow]
    #     num_empty = np.count_nonzero(check)
    #     if num_empty == num_ops:
    #         for nextrow in range(0, num_ops):
    #             del out[index + nextrow]

    # Create .csv writing function from csv.writer
    num_ops = 2
    num_stations = 3
    
    # convert to strings
    #workers_assigned = [[0.0], [1.0], [1.0], [0.0], [2.0], [0.0]]
    
    workers_assigned = 

    for index in range(0,len(opList)):
        for sub_val in range(0,len(opList[index])):
            workers_assigned.append(str(opList[index][sub_val]))

    stations_assigned = [[], [1, 2], [3]]

    with open('pLineOpt.csv', 'w', newline='') as csvfile:
        fieldnames = ['Station', 'Tasks', 'Human Ops.', 'Computer Ops.']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in range(0,num_stations):
            writer.writerow( { 'Station' : row+1 , 'Tasks': joblist[row], 'Human Ops.': opList[row], 'Computer Ops.' : opList[row+num_stations] } )

    # Use our populated output to write 


    return True 

#x = run_optimization()
#y = translate_to_csv()