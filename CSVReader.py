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

df = pd.read_csv('HeaderInput.csv', skiprows =1) #reads in the CSV file you're going to work with and gets rid of the title row
df.columns = df.columns.str.strip().str.lower().str.replace('[^a-zA-Z]', '') # only keeps the characters that are letters

#original method of renaming the columns, proved to be more limiting since the columns needed to be in exactly the same order as original CSV template
#df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('#', '_').str.replace('(', '').str.replace(')', '')
#df.columns =['Process', 'ProcessName', 'CycleTime', 'Automated', 'Ports', 'Predecessor', 'Takt', '', 'X.Distance', 'Y.Distance'] 


M = 100 #a "big" number necessary for setting upper and lower bounds of certain constraints in the math model

def jobCounter(process):
# purpose: given the Process (#) column, this function returns the number of jobs
    job = 0
    for i in range(len(process)):
        if isnan(process[i]) == True: 
            pass    
        else: 
            job += 1        
    return(int(job))

jobs = jobCounter(df.process) # uses the jobCounter function above to find the number of jobs 
stations = jobs #set the number of stations equal to the number of jobs
takt = df.takt[0] #the takt time is equal to the only value entered in the takt column in the CSV 

def cycleT(jobs):
# Purpose: returns the Cycle Time (s) column into a format that the math model can interpret
    cycleTime = []
    for i in range(jobs):
        cycleTime += [df.cycletimes[i]]
    return(cycleTime)

cycleTime = cycleT(jobs) #uses cycleT function to get cycle times array

def work(cycleTimes,takt,automated): 
# function returns the number of workers given the cycle times, the takt time, and whether or not the job is a computer job
    workers = 0 
    for i in range(len(cycleTimes)):
        workers += ceil(cycleTimes[i]/takt)  #to find the number of workers needed to perform job i, divide the cycle time of job i by the takt time
                                             # use the ceiling function to ensure whole numbers of workers 
        #if automated[i] == 'Y' or automated[i] == 'y':   #uncomment these lines once the model can account for pairing a human to a computer job
        #    workers += 1
    return workers 

workers = work(df.cycletimes,takt,df.automatedyn) #uses work function to find number of workers 

def computerjob(automated):
# this function returns the jobIsComputer array by checking to see if there is a Y or N in the Automated (Y/N) column
    jobIsComputer = []
    for i in range(jobs):
        if automated[i] == 'Y' or automated[i] == 'y':
            jobIsComputer.append(1)                         #if there is a yes, then add a 1 to signify a computer job
        if automated[i] == 'N' or automated[i] == 'n':
            jobIsComputer.append(0)                         #if there is a no, then add a 0 to signify a non computer job
    return(jobIsComputer)

jobIsComputer = computerjob(df.automatedyn) #uses computerjob function to get jobIsComputer array


def buildpredecessors(jobs, Predecessor): 
# function creates the predecessor matrix based on the information provided in the Immediate Predecessor column
    pred = [[0 for col in range(jobs)] for row in range(jobs)] #initializes predecessor matrix (nested arrays) by filling everything with 0
    for i in range(jobs):
        if isnan(Predecessor[i]) == True: 
            pass                                # if there is no predecessors, dont change anything (keep a 0 there)
        else: 
            pred[int(Predecessor[i]-1)][int(i)]= 1    #if JOB is a predecessor to other job, set the column corresponding to other job equal to 1
                                                      #in the row corresponding to JOB
    return(pred)

pred = buildpredecessors(jobs,df.immediatepredecessorfromcol) #uses buildprecessors function to get pred nested array


def numPorts(ports):
#sums the numbers in the Capacity (# ports) column
    port = 0
    for i in range(jobs):
        if isnan(ports[i]) == True: #if there is no number in the cell, ignore it
            pass    
        else: 
            port = port+ports[i]   #add numbers together 
    return(int(port)) 

def jobIsHuman(jobIsComputer): 
# make a jobIsHuman array by turning all 0s to 1s and 1s to 0s in the jobIsComputer array
    jobIsHuman = [0]*len(jobIsComputer) #jobIsHuman array has to be the same length as jobIsComputer array (also equal to the number of jobs)
    for i in range(len(jobIsComputer)):
        if jobIsComputer[i] == 1:
            jobIsHuman[i] = 0
        if jobIsComputer[i] == 0:
            jobIsHuman[i] = 1
    return jobIsHuman   


def buildQual (workers,ports,jobIsComputer): 
#build the qualified matrix by multiplying the jobIsComputer array by the number of ports and the jobIsHuman array by the number of workers
    numComputers = numPorts(ports)
    ifQual = numComputers* [jobIsComputer] + [jobIsHuman(jobIsComputer)] * (workers-numComputers)
    return(ifQual)

ifQual = buildQual(workers,df.capacityofports,jobIsComputer) #use the buildQual function to get ifQual matrix


def humanJobs(jobIsComputer):
#gives you the indices of human jobs in an array
    humanj = []
    for i in range(len(jobIsComputer)):
        #checks to see if job is a human job
        if jobIsComputer[i] == 0:     #if it is a human job, add it to humanj array
            humanj += [i]
        else:                         #if it is not a human job, don't change anything about humanj array
            humanj = humanj
    return humanj


def cycleTimehuman(jobIsComputer,cycleTime):
#gives you the cycle times corresponding to human jobs
    humanindex = humanJobs(jobIsComputer)          #runs humanJobs to get indices of human jobs
    cycletimesH = []
    for i in range(len(humanindex)):
        cycletimesH += [cycleTime[humanindex[i]]]   #add the cycle time of human jobs to empty array
    return(cycletimesH)

humanCap = ceil(max(cycleTimehuman(jobIsComputer,cycleTime))/takt)  # maximum number of human workers allowed at each workstation
                                                                    # is equal to number of human workers
                                                                    # needed to complete the longest human task