from math import ceil 

# SETS
workers = 5
jobs = 3 # number of jobs to assign
stations = 3 # number of available workstations

# PARAMETERS
takt = 5 # takt time of line
cycleTime = [5,10,5] # cycle time of each job
# pred is true if job j1 is an immediate predecessor of job j2
# pred = m.Array(m.Param,(jobs,jobs),lb=0,ub=1,integer=True)
jobIsComputer = [0,1,0]

#gives you the indices of human jobs in an array
def humanJobs(jobIsComputer):
    humanj = []
    for i in range(len(jobIsComputer)):
        #checks to see if job is a human job
        if jobIsComputer[i] == 0:     #if it is a human job, add it to humanj array
            humanj += [i]
        else:                         #if it is not a human job, don't change anything about humanj array
            humanj = humanj
    return humanj

#gives you the cycle times corresponding to human jobs
def cycleTimehuman(jobIsComputer,cycleTime):
    humanindex = humanJobs(jobIsComputer)          #runs humanJobs to get indices of human jobs
    cycletimesH = []
    for i in range(len(humanindex)):
        cycletimesH += [cycleTime[humanindex[i]]]   #add the cycle time of human jobs to empty array
    return(cycletimesH)

humanCap = ceil(max(cycleTimehuman(jobIsComputer,cycleTime))/takt)  # maximum number of human workers allowed at each workstation
 
                                                                    # is equal to number of human workers
                                                                     # needed to complete the longest human task

pred = [[0, 1, 0],
        [0, 0, 1],
        [0, 0, 0]]
ifQual = [ [0,1,0],
[0,1,0],
[1,0,1],
[1,0,1],
[1,0,1]
]
M = 100

