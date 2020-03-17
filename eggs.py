import csv

num_ops = 2
num_stations = 3
workers_assigned = [[0.0], [1.0], [1.0], [0.0], [2.0], [0.0]]
stations_assigned = [[], [1, 2], [3]]

with open('eggs.csv', 'w', newline='') as csvfile:
    fieldnames = ['Station', 'Tasks', 'Human Ops.', 'Computer Ops.']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #writer.writeheader()
    
    for row in range(0,num_stations):
        writer.writerow( { 'Station' : row , 'Tasks': int(stations_assigned[row]), 'Human Ops.': workers_assigned[row], 'Computer Ops.' : workers_assigned[row+num_stations] } )