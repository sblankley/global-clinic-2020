from CSVReaderDict import *
from numpy import zeros
from math import ceil 
# Warm start - Assumption: jobs occur serially, no cycle time is greater than the takt time
# pseudo code using dictionaries 
ifJobAtStation = zeros((numJobs, numStations))
numWorkers = zeros((numTypes, numStations))
def jobType(j,jobDict): # function needed to figure out what type job j is 
    T = 0 
    for TYPE in range(len(jobDict)):
        if j in jobs[TYPE]:
            T = TYPE            
        else: 
            pass
    return T 
def canAddAnotherJob(j,s,numJobs,jobDict,takt, cycletimeDict): #function for 
    answer = 0 #default answer is no, cannot add next job to current station
    if j+1 > numJobs: #if there is no "next job" (i.e already added the last job)
        answer = 0     #cannot add another job to current station
    if j+1 < numJobs: #if there is a next job, check:
        if jobType(j+1,jobDict) == 0: #if next job is a human job
            if (numWorkers[0][s]+ ceil(cycleTime[j+1]/takt)) <= cap[0]: #check if it won't violate human cap constraint,
                answer = 1   #current station can handle adding the next job
            else:           #if it will violate human cap constraint, cannot add another job to current station
                answer = 0 
        if jobType(j+1,jobDict)!= 0: #if next job is not human job
            if numWorkers[0][s] <= cap[0]: #check if there is enough space at current station
                answer = 1 #if station has not reached its human cap, can add next job to current station
            else: 
                answer = 0 #if station has reached its human cap, cannot add next job to current station
    return answer
#Actual heuristic starts here 
j = 0 #current job
s = 0 #current station 
while j < numJobs:  #continue filling until all jobs are assigned
    ifJobAtStation[j][s] = 1     #assign current job j to current station s
    t = jobType(j,jobs)          #use jobType function to get what type of job j is 
    numWorkers[t][s] += ceil (cycleTime[j]/takt)  # assign appropriate number of workers to perform job j
    if canAddAnotherJob(j,s,numJobs,jobs,takt, cycleTime) == 1:  #check to see if station can take on another job 
        j += 1                #if yes, add next job to current station 
    else:
        j += 1                #if no, go onto next job and next station 
        s += 1
print(ifJobAtStation)
print(numWorkers)