import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
from math import ceil 
df = pd.read_csv('CM1100Header-dims.csv') #reads in the CSV file you're going to work with and gets rid of the title row
df.columns = df.columns.str.strip().str.lower().str.replace('[^a-zA-Z]', '') # only keeps the characters that are letters

M = 100 #a "big" number necessary for setting upper and lower bounds of certain constraints in the math model
takt = df.takts[0] #the takt time is equal to the only value entered in the takt column in the CSV
# count number of jobs to get numJobs and numStations
numJobs = len(df.process)
numStations = numJobs
Cap = [df.humancapacityoperators[0]] # start with max number of human operators at a station, will later pull directly from the CSV like takt time
cycletime = []
jobnames = []
for i in range(numJobs):
    cycletime.append(df.cycletimes[i]) #create list of cycle times
    jobnames.append(df.processname[i]) #create list of job names
    if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y': # check for computer jobs to create capacitity list 
        Cap.append(int(df.capacityofports[i]))  #add capcacity of each type of computer job
numTypes = len(Cap)
#check to make sure manual human cap will not break
if Cap[0]<ceil(max(cycletime)/takt):
    Cap[0] =  max(cycletime)/takt
# create list of types and computer types, list of stations
types = list(range(0,numTypes))
compTypes = list(range(1,numTypes))
stations = list(range(0,numStations))
# create list of jobs that are of each type
Jobs = [ [] for i in range(numTypes) ]
compCounter = 0
for i in range(numJobs):
    if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y': # check for computer jobs
        compCounter += 1
        Jobs[compCounter].append(i)
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
#job names dictionary - keys: job index, values: job name (strings)
jobNames = {}
for i in range(len(jobnames)):
    jobNames[i] = jobnames[i]
# capacity dictionary - keys: job type, values: capacity value, arbirary value assigned to human job
#job dictionary - keys: job type, values: jobs of that type
cap =	{}
jobs = {}
for i in range(numTypes):
    jobs[i] = Jobs[i]
    cap[i] = Cap[i]
#list of x and y distances 
lengthdist = []
widthdist = []
for i in range(len(df.lengthm)): 
    lengthdist.append(df.lengthm[i])
    widthdist.append(df.widthm[i])
#dictionaries from those lists 
length = {}
width = {}
for i in range(len(lengthdist)): 
    length[i] = lengthdist[i]
    width[i] = widthdist[i]
