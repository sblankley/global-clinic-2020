# from csvReader import * # input data
from taskgrouping import * 
# import results csv

tasks =	{}
for i in range(len(real_stations)):
	tasks[i] = task_dist[i]

operators = {}
for i in range(len(real_stations)): # this should actually be indexed over types
    operators[i] = op_dist[i]

types  #original dictionary with types as keys as jobs as values from csv reader

#uncomment these lines for CSVs with size data 
length # dict with jobs as keys as length as values, from csv reader
width # dict with jobs as keys and widths as values, from csv reader

saved
 

# NEED THE FOLLOWING:
# dict with jobs as keys as length as values
# dict with jobs as keys and widths as values
# dict with new stations as keys and jobs as values
# dict with type as keys and jobs as values

# results are indexed by station and have job # and number of each type of operator
# we want to calculate the length and width of each station
# for each type, we calc the max space required
# if it's a human type, double the width and multiply the length by (# ops / 2)
# some computer jobs MUST be all next to each other -- will contemplate that

# for each newstation
for s in range(len(real_stations)):
    # initialize temp demensions
    temp = [] 
    # for each type
    #for t in range(len(op_dist[0])):
        # get max length and width of the assigned tasks
        
        # if number of operators is greater than one
            # take number of operators and divide by two
            # temp will add that # times the length total length, and twice the width
        # else (if number of operators is one or zero)
            # temp will add that length and that width
    # station gets dimensions of temp

# now we also want the bottom left corner of each new station in a line
# assigne a buffer space between stations

# stationCorner[0] = [0, 0]
# offset = 0
# for each newstation s (minus the last one)
    # offset += the length of the newstation + buffer
    # stationCorner[s+1] = offset
# now for each station we should have a length, width, x of bottom left, y of bottom left