# This script converts the csv data into dictionaries as inputs for the PuLP model

import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
df = pd.read_csv('HeaderInput.csv', skiprows =1) #reads in the CSV file you're going to work with and gets rid of the title row
df.columns = df.columns.str.strip().str.lower().str.replace('[^a-zA-Z]', '') # only keeps the characters that are letters

M = 100 #a "big" number necessary for setting upper and lower bounds of certain constraints in the math model
takt = df.takt[0] #the takt time is equal to the only value entered in the takt column in the CSV
# count number of jobs to get numJobs and numStations
numJobs = len(df.process)
numStations = numJobs
Cap = [4] # start with max number of human operators at a station, will later pull directly from the CSV like takt time
cycletime = []
for i in range(numJobs):
    cycletime.append(df.cycletimes[i]) #create list of cycle times
    if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y': # check for computer jobs to create capacitity list
        if df.capacityofports[i] not in Cap[1:]:  #check if the capacity has not been added before, and disregard human cap value
            Cap.append(int(df.capacityofports[i]))  #add capcacity of each type of computer job
numTypes = len(Cap)
# create list of types and computer types, list of stations
types = list(range(0,numTypes))
compTypes = list(range(1,numTypes))
stations = list(range(0,numStations))
# create list of jobs that are of each type
Jobs = [ [] for i in range(numTypes) ]
for i in range(numJobs):
    if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y': # check for computer jobs
        for j in range(numTypes-1):
            if df.capacityofports[i] == Cap[j+1]:   #the +1/ -1 indices are to skip over the first value (human) in capacity
                Jobs[j+1].append(i)
    else:
        Jobs[0].append(i)
#create list of pred
Pred = [ [] for i in range(numJobs) ]
for i in range(1,numJobs):
    Pred[i].append(int(df.immediatepredecessorfromcol[i]-1))
# pred dictionary - keys: job index, values: preceeding job
pred =	{}
for i in range(numJobs):
	pred[i] = Pred[i]
# cycleTime dictionary - keys: job index, values: cycle time of corresponding job
cycleTime =	{}
for i in range(len(cycletime)):
	cycleTime[i] = cycletime[i]
# capacity dictionary - keys: job type, values: capacity value, arbirary value assigned to human job
#job dictionary - keys: job type, values: jobs of that type
cap =	{}
jobs = {}
for i in range(numTypes):
    jobs[i] = Jobs[i]
    cap[i] = Cap[i]
