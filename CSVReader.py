# This script converts the csv data into dictionaries as inputs for the PuLP model

import pandas as pd #install using pip install pandas, necessary to translate CSV into a dataframe we can work with
import settings
from math import ceil 

def read(fileName):
    df = pd.read_csv(fileName, skiprows =0) #reads in the CSV file you're going to work with and gets rid of the title row
    df.columns = df.columns.str.strip().str.lower().str.replace('[^a-zA-Z]', '') # only keeps the characters that are letters

    M = 100 #a "big" number necessary for setting upper and lower bounds of certain constraints in the math model
    takt = df.takt[0] #the takt time is equal to the only value entered in the takt column in the CSV
    # count number of jobs to get numJobs and numStations
    numJobs = len(df.process)
    numStations = numJobs
    Cap = [df.humancapacity[0]] # start with max number of human operators at a station
    cycletime = []
    jobnames = []
    for i in range(numJobs):
        cycletime.append(df.cycletimes[i]) #create list of cycle times
        jobnames.append(df.processname[i]) #create list of job names
        if df.automatedyn[i] == 'Y' or df.automatedyn[i] == 'y': # check for computer jobs to create capacitity list
            #if df.capacityofports[i] not in Cap[1:]:  #check if the capacity has not been added before, and disregard human cap value
            Cap.append(int(df.capacityofports[i]))  #add capcacity of each type of computer job
    numTypes = len(Cap)
    #check to make sure manual human cap will not break
    if Cap[0]<ceil(max(cycletime)/takt):
        Cap[0] = int(ceil(max(cycletime)/takt))
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
            # for j in range(numTypes-1):
            #     if df.capacityofports[i] == Cap[j+1]:   #the +1/ -1 indices are to skip over the first value (human) in capacity
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

    #Uncomment these lines for CSVs with sizing data 
    #list of x and y distances 
    lengthdist = []
    widthdist = []
    for i in range(len(df.lengthm)):  #would there ever be a situation where x distance != y distances input
        lengthdist.append(df.lengthm[i])
        widthdist.append(df.widthm[i])
    #dictionaries from those lists 
    length = {}
    width = {}
    for i in range(len(lengthdist)): 
        length[i] = lengthdist[i]
        width[i] = widthdist[i]
    
    # set global variables
    # settings.myList['stations'] = stations
    # settings.myList['types'] = types
    # settings.myList['jobs'] = jobs
    # settings.myList['pred'] = pred
    # settings.myList['numJobs'] = numJobs
    # settings.myList['cycleTime'] = cycleTime
    # settings.myList['takt'] = takt
    # settings.myList['cap'] = cap
    # settings.myList['length'] = length
    # settings.myList['width'] = width
    # settings.myList['jobNames'] = jobNames




