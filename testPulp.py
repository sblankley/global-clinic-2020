from pulp import *
# change solver to cplex
# from CSVReaderDict import *
import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
from math import ceil #ceil used in finding number of workers and in humanCap
from math import isnan #used in several functions to check if certain values are not numbers

df = pd.read_csv('CM1100Header.csv', skiprows =1) #reads in the CSV file you're going to work with and gets rid of the title row
#df.dropna = df  #check to see if this actually does what i want it to do
df.columns = df.columns.str.strip().str.lower().str.replace('[^a-zA-Z]', '') # only keeps the characters that are letters

# note: currently creating things individually for ease of reading, but faster if combine things in loops

M = 100 #a "big" number necessary for setting upper and lower bounds of certain constraints in the math model
takt = df.takt[0] #the takt time is equal to the only value entered in the takt column in the CSV
# count number of jobs to get numJobs and numStations
numJobs = len(df.process)
numStations = numJobs

Cap = [4] # start with max number of human operators at a station
for i in range(numJobs):
    if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y':  #check for computer jobs
        if df.capacityofports[i] not in Cap[1:]:  #check if the capacity has not been added before, and disregard human cap value
            Cap.append(int(df.capacityofports[i]))  #add capcacity of each type of computer job


numTypes = len(Cap)
# # count number of types = # of automated +1
# numTypes = 1
# for i in range(numJobs):
#     if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y':   #Need to fix this bc this adds a new type for EVERY computer job (not every unique computer job)
#         numTypes += 1
#     else:
#        pass

# create list of types and computer types, list of stations
types = list(range(0,numTypes))
compTypes = list(range(1,numTypes))
stations = list(range(0,numStations))
# create list of cycle times
cycletime = []
for i in range(numJobs):
    cycletime.append(df.cycletimes[i])
# cycleTime dictionary - keys: job index, values: cycle time of corresponding job
cycleTime =	{}
for i in range(len(cycletime)):
	cycleTime[i] = cycletime[i]
#create list of pred
Pred = [ [] for i in range(numJobs) ]
for i in range(1,numJobs):
    Pred[i].append(int(df.immediatepredecessorfromcol[i]-1))
# pred dictionary - keys: job index, values: preceeding job
pred =	{}
for i in range(numJobs):
	pred[i] = Pred[i]
# capacity dictionary - keys: job type, values: capacity value, arbirary value assigned to human job
cap =	{}
for i in range(numTypes):
	cap[i] = Cap[i]
#create list of jobs that are of each type
Jobs = [ [] for i in range(numTypes) ]
for i in range(numJobs):
    if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y':
        for j in range(numTypes-1):
            if df.capacityofports[i] == Cap[j+1]:   #the +1/ -1 indices are to skip over the first value (human) in capacity
                Jobs[j+1].append(i)
    else:
        Jobs[0].append(i)
#job dictionary - keys: job type, values: jobs of that type
jobs = {}
for i in range(numTypes):
    jobs[i] = Jobs[i]

prob = LpProblem("Assignment Problem",LpMinimize)

# DECISION VARIABLES
# assignWorkers = [(t,s) for t in types for s in stations]
# assignJobs = [(j,s) for j in list(range(numJobs)) for s in stations]
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
