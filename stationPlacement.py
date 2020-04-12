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
	temp = []
	for t in types:
		maxLength = 0
		maxWidth = 0
		for j in assignedJobs[s][t]:
			if (length[j] > maxLength):
				maxLength = length[j]
			if (width[j] > maxWidth):
				maxWidth = width[j]
        # if number of operators is greater than one and is a human
		if (op_dist[s][t] > 1) and (t==0):
            # take number of operators and divide by two
            # temp will add that # times the length total length, and twice the width
			temp[0] += ceil(op_dist[s][t]/2)*maxLength
			temp[1] += 2*maxWidth
		elif (t!=0):
    			temp[0] += op_dist[s][t]*maxLength
        # else (if number of operators is one or zero)
		else:
            # temp will add that length and that width
			temp[0] += maxLength
			temp[1] += maxWidth
    # station gets dimensions of temp
	placement[s][0] = temp[0]
	placement[s][1] = temp[1]

# now we also want the bottom left corner of each new station in a line
# assign a spacer between stations

placement[0][3] = 0
placement[0][4] = -placement[0][1]/2
spacer = 1
offset = 0
# for each newstation s (minus the last one)
for s in range(len(real_stations)-1):
    # offset += the length of the newstation + spacer
	offset += placement[s][0]
	placement[s+1][2] = offset
	placement[s+1][3] = -placement[s+1][1]/2
# placement is x of bottom left, y of bottom left, length, width
