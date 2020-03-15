# The following is a list of assumptions about the CSV file that this Python script can process
# CSV has 10 columns (9 if you don't include the space between task optimization and layout)
# the very first row has titles "Task Optimization" and "Layout"
# there are no empty rows
# the column names are the same as in HeaderInput.csv
# the information corresponding to the column names is in the same order as in HeaderInput.csv
# values entered into Process (#) are numbers
# values entered in Process (name) are strings
# values entered in Cycle Time (s) are numbers
# values entered in Automated (Y/N) are: Y or y or N or n
# values entered in Capacity (# of ports) are:  N/A or space or numbers
# values entered in Immediate Predecessor (# from Col. 1) are: N/A or space or number
# value entered in Takt is on the first row (after the title) and is a positive number
# values entered in X/Y Distance (m) are numbers

import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
from math import ceil #ceil used in finding number of workers and in humanCap
from math import isnan #used in several functions to check if certain values are not numbers

df = pd.read_csv('CM1100Header.csv', skiprows =1) #reads in the CSV file you're going to work with and gets rid of the title row
#df.dropna = df  #check to see if this actually does what i want it to do 
df.columns = df.columns.str.strip().str.lower().str.replace('[^a-zA-Z]', '') # only keeps the characters that are letters

#original method of renaming the columns, proved to be more limiting since the columns needed to be in exactly the same order as original CSV template
#df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('#', '_').str.replace('(', '').str.replace(')', '')
#df.columns =['Process', 'ProcessName', 'CycleTime', 'Automated', 'Ports', 'Predecessor', 'Takt', '', 'X.Distance', 'Y.Distance']

# note: currently creating things individually for ease of reading, but faster if combine things in loops

M = 100 #a "big" number necessary for setting upper and lower bounds of certain constraints in the math model
takt = df.takt[0] #the takt time is equal to the only value entered in the takt column in the CSV
# count number of jobs to get numJobs and numStations
numJobs = len(df.process)
numStations = numJobs
# count number of types = # of automated +1
numTypes = 1
for i in range(numJobs):
    if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y':   #uncomment these lines once the model can account for pairing a human to a computer job
        numTypes += 1
    else:
       pass
# create list of types and computer types, list of stations
types = list(range(0,numTypes))
compTypes = list(range(1,numTypes))
stations = list(range(0,numStations))
# create list of cycle times
cycleTime = []
for i in range(numJobs):
    cycleTime.append(df.cycletimes[i])
cap = [4] # start with max number of human operators at a station
for i in range(numJobs):
    if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y':
        cap.append(df.capacityofports[i])
pred = [ [] for i in range(numJobs) ]
for i in range(1,numJobs):
    pred[i].append(int(df.immediatepredecessorfromcol[i]))
jobs = [ [] for i in range(numTypes) ]
temp = 1
for i in range(numJobs):
    if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y':
        jobs[temp].append(i)
        temp += 1
    else:
        jobs[0].append(i)

# def cycleTimehuman(jobIsComputer,cycleTime):
# #gives you the cycle times corresponding to human jobs
#     humanindex = humanJobs(jobIsComputer)          #runs humanJobs to get indices of human jobs
#     cycletimesH = []
#     for i in range(len(humanindex)):
#         cycletimesH += [cycleTime[humanindex[i]]]   #add the cycle time of human jobs to empty array
#     return(cycletimesH)
#
# humanCap = ceil(max(cycleTimehuman(jobIsComputer,cycleTime))/takt)  # maximum number of human workers allowed at each workstation
#                                                                     # is equal to number of human workers
#                                                                     # needed to complete the longest human task





thisdict =	{}


print(thisdict)

cycleTime = [5, 5, 10]

for i in range(len(cycleTime)):

	thisdict[i] = cycleTime[i]
    
print(thisdict)    