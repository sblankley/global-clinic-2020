from CSVReader import *
from numpy import zeros
from math import ceil
# Warm start - Assumption: jobs occur serially
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
def canAddAnotherJob(j,s,numJobs,jobDict,takt, cycletimeDict,c): #function to check if station can take on another job 
    answer = 0 #default answer is no, cannot add next job to current station
    if j+1 > numJobs: #if there is no "next job" (i.e already added the last job)
        answer = 0     #cannot add another job to current station
    if j+1 < numJobs: #if there is a next job, check:
        if sum(c.values())+ cycleTime[j+1] >= takt: #if the next job will not allow the station to complete tasks under the cycle time 
            return 0                                #cannot add next job to current station
        if jobType(j+1,jobDict) == 0: #if next job is a human job
            if (numWorkers[0][s]+ ceil(cycleTime[j+1]/takt)) <= cap[0]: #check if it won't violate human cap constraint
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
c = {} #cycle time tracker dictionary 
while j < numJobs:  #continue filling until all jobs are assigned
    ifJobAtStation[j][s] = 1     #assign current job j to current station s
    t = jobType(j,jobs)          #use jobType function to get what type of job j is
    if cycleTime[j] > takt:      #if the cycle time is greater than the takt time, 
        numWorkers[t][s] += ceil(cycleTime[j]/takt) #assign the number of workers based on cycletime/takt
        c[t] = takt
    else:                        #if cycle time < takt time
        if c.get(t,takt) + cycleTime[j] > takt: #check if the sum of cycle times of job of type t at station s is greater than the takt time
            numWorkers[t][s] += 1  # if yes, add another worker of type t 
            c[t] = c.get(t,takt) - takt + cycleTime[j] #reset value in cycle time tracker dictionary
        else:  #if the sum of cycle times of jobs of type t is less than the takt time
            c[t] += cycleTime[j] #do not add another worker, but update the cycle time tracker dictionary
    if canAddAnotherJob(j,s,numJobs,jobs,takt,cycleTime,c) == 1:  #check to see if station can take on another job
        j += 1                #if yes, add next job to current station
    else:
        j += 1                #if no, go onto next job and next station, restart cycle time tracker dictionary
        s += 1
        c={}
print(ifJobAtStation)
print(numWorkers)
