from CSVReaderDict import *
from numpy import zeros
from math import ceil 
# Warm start 
# pseudo code using dictionaries 
ifJobAtStation = zeros((numJobs, numStations))
numWorkers = zeros((numTypes, numStations))
j = 0 #current job
s = 0 #current station 
t = 0 
while j < numJobs:  #continue filling until all jobs are assigned
    ifJobAtStation[j][s] = 1     #assign current job j to current station s
    for TYPE in range(len(jobs)):
        if j in jobs[TYPE]:
            t = TYPE            # figure out what type job j is 
        else: 
            pass
    numWorkers[t][s] = ceil (cycleTime[j]/takt)  # assign appropriate number of workers to perform job j 
    if cycleTime[j] <= takt:  #check to see if station can take on another job - THIS IS THE PART THATS INCORRECT 
        j += 1                #if yes, add next job to current station 
    else:
        j += 1                #if no, go onto next job and next station 
        s += 1