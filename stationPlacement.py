# from csvReader import * # input data
from taskgrouping import *
# import results csv

# dict with new stations as keys and jobs as values
tasks =	{}
for i in range(len(real_stations)):
	tasks[i] = task_dist[i]

operators = {}
for i in range(len(real_stations)):
    operators[i] = op_dist[i]

jobs  #original dictionary with types as keys as jobs as values from csv reader

assignedJobs = [[[] for k in types] for i in range(len(real_stations))]
for s in range(len(real_stations)):
	for t in types:
		for j in jobs[t]:
			if (j in tasks[s]):
				assignedJobs[s][t].append(j)

# assignedJobs = {{}}
# for s in range(len(real_stations)):
# 	for t in types:
# 		temp = []
# 		for j in jobs[t]:
# 			if (j in tasks[s]):
# 				temp.append(j)
# 		assignedJobs[s][t] = temp

#uncomment these lines for CSVs with size data
length # dict with jobs as keys as length as values, from csv reader
width # dict with jobs as keys and widths as values, from csv reader

# results are indexed by station and have job # and number of each type of operator
# we want to calculate the length and width of each station
# for each type, we calc the max space required
# if it's a human type, double the width and multiply the length by (# ops / 2)
# some computer jobs MUST be all next to each other -- will contemplate that

placement = [[] for i in range(len(real_stations))]
# for each newstation
for s in range(len(real_stations)):
    # initialize temp demensions
    temp = []
    # for each type
    for t in types:
		maxLength = 0
		maxWidth = 0
		for j in assignedJobs[s][t]:
			if (length[j] > maxLength):
				maxLength = length[j]
			if (width[j] > maxWidth):
				maxWidth = width[j]
        # if number of operators is greater than one
		if (op_dist[s][t] > 1):
            # take number of operators and divide by two
            # temp will add that # times the length total length, and twice the width
			temp[0] += ceil(op_dist[s][t]/2)*maxLength
			temp[1] += 2*maxWidth
        # else (if number of operators is one or zero)
		else:
            # temp will add that length and that width
			temp[0] += maxLength
			temp[1] += maxWidth
    # station gets dimensions of temp
	placement[s] = temp

# now we also want the bottom left corner of each new station in a line
# assigne a buffer space between stations

# stationCorner[0] = [0, 0]
# offset = 0
# for each newstation s (minus the last one)
    # offset += the length of the newstation + buffer
    # stationCorner[s+1] = offset
# now for each station we should have a length, width, x of bottom left, y of bottom left
