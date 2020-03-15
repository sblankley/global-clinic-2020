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
    Pred[i].append(int(df.immediatepredecessorfromcol[i]))    
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