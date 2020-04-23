import backend.settings as settings
import math

def splitIndex(n):
    """will return the list index"""
    return [(x+1) for x,y in zip(n, n[1:]) if y-x != 1]

def splitList(inputList):
    """will split the list base on the index"""
    index = splitIndex(inputList)
    splitList = list()
    prev = 0
    for i in index:
        consecList = [ x for x in inputList[prev:] if x < i]
        splitList.append(consecList)
        prev += len(consecList)
    splitList.append([ x for x in inputList[prev:]])
    return splitList

def run_stationPl():
	# import global variables
	stations = settings.myList['stations']
	types = settings.myList['types']
	jobs = settings.myList['jobs']
	pred = settings.myList['pred']
	numJobs = settings.myList['numJobs']
	cycleTime = settings.myList['cycleTime']
	takt = settings.myList['takt']
	cap = settings.myList['cap']
	real_stations = settings.myList['real_stations']
	op_dist = settings.myList['op_dist']
	task_dist = settings.myList['task_dist']
	task_Dist = settings.myList['task_Dist']
	length = settings.myList['length']
	width = settings.myList['width']
	# jobNames = settings.myList['jobNames']


	# dict with new stations as keys and jobs as values
	tasks =	{}
	for i in range(len(real_stations)):
		tasks[i] = task_Dist[i]

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

	placement = [[0,0,0,0] for i in range(len(real_stations))]
	# for each newstation
	for s in range(len(real_stations)):
		currLength = 0
		currWidth = 0
		for t in types[1:]:
			if (len(assignedJobs[s][t])!=0):
				# currLength += op_dist[s][t]*length[jobs[t][0]] # uncomment this line if reducing ports from full capacity
				currLength += cap[t]*length[jobs[t][0]]
				if (width[jobs[t][0]] > currWidth):
						currWidth = width[jobs[t][0]]
		# now let's handle human jobs -- we can combine space if consecutive
		splitJobs = splitList(assignedJobs[s][0])
		group = 0
		while (group < len(splitJobs) ):
    		maxLength = 0
			maxWidth = 0
			for j in splitJobs[group]:
    			if (length[j] > maxLength):
    				maxLength = length[j]
				if (width[j] > maxWidth):
					maxWidth = width[j]
			if (op_dist[s][0] > 1): # if num human ops is greater than one
    			currLength += ceil(op_dist[s][0]/2)*maxLength
				if (2*maxWidth > currWidth):
					currWidth = 2*maxWidth
			else: # if num human ops is 1
    			currLength += maxLength
				if (maxWidth > currWidth):
    				currWidth = maxWidth
			group += 1
		placement[s][0] = currLength
		placement[s][1] = currWidth

		# for j in assignedJobs[s][0]:
		#     # if number of operators is greater than one and is a human
		# 	if (op_dist[s][t] > 1):
		#         # take number of operators and divide by two
		#         # temp will add that # times the length total length, and twice the width
		# 		currLength += ceil(op_dist[s][t]/2)*maxLength
		# 		currWidth[1] += 2*maxWidth
		# 	else:
		#         # temp will add that length and that width
		# 		currLength += maxLength
		# 		if (maxWidth > currWidth):
		# 				currWidth = maxWidth
		# station gets dimensions of temp

		# lastJob = -1
		# maxLength = 0
		# maxWidth = 0
		# index = 0
		# while (index < len(assignedJobs[s][0])-1):
		# 	maxLength = 0
		# 	maxWidth = 0
		# 	while (assignedJobs[s][0][index]==lastJob+1):
		# 		if (length[j] > maxLength):
		# 			maxLength = length[j]
		# 		if (width[j] > maxWidth):
		# 			maxWidth = width[j]
		# 		lastJob = j
		# 		index += 1
		# 	# print(op_dist[s][0])
		# 	# print(op_dist[s][1])
		# 	if (op_dist[s][0] > 1):
		# 		currLength += math.ceil(op_dist[s][0]/2)*maxLength
		# 		if (2*maxWidth > currWidth):
		# 			currWidth = 2*maxWidth
		# 	else:
		# 		currLength += maxLength
		# 		if (maxWidth > currWidth):
		# 			currWidth = maxWidth	
		# 	lastJob = assignedJobs[s][0][index]
		# 	index += 1
		# placement[s][0] = currLength
		# placement[s][1] = currWidth





	# now we also want the bottom left corner of each new station in a line
	# assign a spacer between stations

	spacer = 1
	placement[0][2] = spacer
	placement[0][3] = -placement[0][1]/2 + spacer
	
	xoffset = 0
	# for each newstation s (minus the last one)
	for s in range(len(real_stations)-1):
		# xoffset += the length of the newstation + spacer
		xoffset += placement[s][0] + spacer
		placement[s+1][2] = xoffset
		placement[s+1][3] = -placement[s+1][1]/2 + spacer
	# placement is length (x), width (y), x of bottom left, y of bottom left

	for s in range(len(real_stations)):
		for dim in range(4):
			if placement[s][dim] < 0:
				placement[s][dim] = abs(placement[s][dim]) + 1

	# global variables
	settings.myList['placement'] = placement




    